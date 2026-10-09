#!/usr/bin/env python3
"""Avoid unrelated desktop seed downloads in the upstream minimal OCI profile."""
import pathlib
import re
import sys

path = pathlib.Path(sys.argv[1])
config = path.read_text()
profiles = re.findall(r'^[ \t]*(?:ubuntu-base\|)?ubuntu-oci\)[ \t]*\n'
                      r'(.*?)^[ \t]*;;[ \t]*$', config, re.M | re.S)
if (len(profiles) != 1 or '--bootstrap-flavour=minimal' not in profiles[0]
        or re.search(r'\b(?:add_task|inheritance|seed_from_task|list_packages_from_seed|'
                     r'snap_from_seed|germinate|case|esac)\b', profiles[0])):
    raise RuntimeError('Upstream ubuntu-oci profile is no longer a seed-free minimal build')

directory = 'mkdir -p config/germinate-output\n'
guard = 'if ! [ -e config/germinate-output/structure ]; then'
if config.count(directory) != 1 or config.count(guard) != 1 or config.index(directory) > config.index(guard):
    raise RuntimeError('Upstream germinate cache setup changed; review the OCI adapter')

# auto/config clears config first, so creating this marker before lb config
# loses it. Set it after upstream recreates the directory, only for our OCI
# profile. Debootstrap and all upstream OCI package/cleanup hooks stay intact.
marker = '''# The base OCI profile uses debootstrap's minimal set, without seed tasks.
if [ "${PROJECT:-}:${SUBPROJECT:-}" = ubuntu-oci: ]; then
    touch config/germinate-output/structure
    echo "Ubuntu OCI: using the official minimal profile without desktop seeds"
fi
'''
path.write_text(config.replace(directory, directory + marker, 1))
