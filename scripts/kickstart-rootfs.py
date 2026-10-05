#!/usr/bin/env python3
"""Build only a container rootfs from the mirrored upstream kickstart.

Run inside an isolated privileged builder container. Package selections and
post scripts come from upstream; disk/boot/installer commands are not run.
"""
import os
import pathlib
import shutil
import subprocess
import sys

from pykickstart import constants
from pykickstart.parser import KickstartParser
from pykickstart.sections import NullSection
from pykickstart.version import makeVersion


class DisabledKdump(NullSection):
    def handleHeader(self, lineno, args):
        if args != ['%addon', 'com_redhat_kdump', '--disable']:
            raise RuntimeError('Unsupported installer addon: ' + ' '.join(args))

    def handleLine(self, line):
        if line.strip() and not line.lstrip().startswith('#'):
            raise RuntimeError('Unexpected instructions in disabled kdump addon')


def parse_recipe(recipe):
    handler = makeVersion()
    parser = KickstartParser(handler)
    parser.registerSection(DisabledKdump(handler, sectionOpen='%addon'))
    previous = os.getcwd()
    try:
        os.chdir(str(recipe.parent))
        parser.readKickstart(str(recipe))
    finally:
        os.chdir(previous)
    for script in handler.scripts:
        if script.type == constants.KS_SCRIPT_POST:
            continue
        # Rocky 8 starts Anaconda's installer bus here. A rootfs-only build
        # has no Anaconda process, so this particular installer setup is unused.
        if script.type == constants.KS_SCRIPT_PRE and script.script.strip() == 'dbus-broker-launch --scope=none':
            continue
        raise RuntimeError('New non-post script requires a container build adapter')
    p = handler.packages
    if not p.nocore or p.default or p.environment or p.groupList or p.excludedGroupList:
        raise RuntimeError('This adapter requires an explicit container package list with --nocore')
    if not p.packageList:
        raise RuntimeError('Empty container package list')
    return handler


def run(*args):
    subprocess.run(args, check=True)


def build(recipe, major, root):
    handler = parse_recipe(recipe)
    root.mkdir(parents=True)
    keydir = root / 'etc/pki/rpm-gpg'
    shutil.copytree('/etc/pki/rpm-gpg', str(keydir))
    p = handler.packages
    options = ['dnf', '-y', '--installroot=' + str(root), '--releasever=' + major,
               '--setopt=reposdir=/etc/yum.repos.d', '--setopt=varsdir=/etc/dnf/vars']
    if p.excludeDocs:
        options.append('--setopt=tsflags=nodocs')
    if p.excludeWeakdeps:
        options.append('--setopt=install_weak_deps=False')
    if p.instLangs:
        options.append('--setopt=override_install_langs=' + p.instLangs)
    options += ['--exclude=' + pkg.replace('\\*', '*') for pkg in p.excludedList]
    run(*(options + ['install'] + p.packageList))
    # Apply non-installer settings represented in the original recipe.
    if handler.lang.seen:
        (root / 'etc/locale.conf').write_text('LANG=' + handler.lang.lang + '\n')
    if handler.timezone.seen and handler.timezone.timezone:
        link = root / 'etc/localtime'
        if link.is_symlink() or link.exists():
            link.unlink()
        link.symlink_to('../usr/share/zoneinfo/' + handler.timezone.timezone)
    if handler.rootpw.seen:
        if not handler.rootpw.lock:
            raise RuntimeError('Container recipe must lock the root password')
        shadow = root / 'etc/shadow'
        rows = shadow.read_text().splitlines()
        for i, row in enumerate(rows):
            fields = row.split(':')
            if fields[0] == 'root':
                fields[1] = '!' + handler.rootpw.password.lstrip('!')
                rows[i] = ':'.join(fields)
        shadow.write_text('\n'.join(rows) + '\n')
    dns = root / 'etc/resolv.conf'
    if dns.is_symlink() or dns.exists():
        dns.unlink()
    shutil.copyfile('/etc/resolv.conf', str(dns))
    pathlib.Path('/mnt').mkdir(exist_ok=True)
    pathlib.Path('/mnt/sysimage').symlink_to(root, target_is_directory=True)
    mounted = []
    try:
        for name, args in [('proc', ['-t', 'proc', 'proc']),
                           ('sys', ['--rbind', '/sys']), ('dev', ['--rbind', '/dev']),
                           ('run', ['-t', 'tmpfs', 'tmpfs'])]:
            dest = root / name
            dest.mkdir(exist_ok=True)
            run('mount', *args, str(dest))
            run('mount', '--make-rprivate', str(dest))
            mounted.append(dest)
        for script in handler.scripts:
            if script.type != constants.KS_SCRIPT_POST:
                continue
            if script.inChroot:
                script_path = root / 'tmp/container-upstream-post.sh'
                script_path.parent.mkdir(exist_ok=True)
                script_path.write_text(script.script)
                args = ['chroot', str(root), script.interp, '/tmp/container-upstream-post.sh']
            else:
                script_path = pathlib.Path('/tmp/container-upstream-post.sh')
                script_path.write_text(script.script)
                args = [script.interp, str(script_path)]
            # A failed upstream post script always fails this image build.
            subprocess.run(args, check=True, env=dict(os.environ, INSTALL_ROOT=str(root)))
            if script_path.exists():
                script_path.unlink()
    finally:
        for dest in reversed(mounted):
            subprocess.run(['umount', '-R', str(dest)], check=False)
        pathlib.Path('/mnt/sysimage').unlink()
    run(*(options + ['clean', 'all']))
    dns.unlink(missing_ok=True) if sys.version_info >= (3, 8) else dns.unlink()
    if not (root / 'etc/os-release').is_file():
        raise RuntimeError('Original recipe did not produce an operating system rootfs')


if __name__ == '__main__':
    build(pathlib.Path(sys.argv[1]).resolve(), sys.argv[2], pathlib.Path(sys.argv[3]).resolve())
