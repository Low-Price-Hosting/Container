#!/usr/bin/env python3
"""Select the upstream OCI description without validating unrelated VM profiles."""
import pathlib
import sys
import xml.etree.ElementTree as ET

path = pathlib.Path(sys.argv[1])
architecture = sys.argv[2] if len(sys.argv) > 2 else ''
tree = ET.parse(path)
root = tree.getroot()
without_sig = architecture == 'riscv64' and int(root.findtext('preferences/release-version', '0')) >= 10
unrelated = ('cloud/', 'vagrant/', 'wsl/', 'live/', 'components/boot.xml', 'components/users.xml')
container_found = False
for include in list(root.findall('include')):
    source = include.get('from', '').removeprefix('this://').removeprefix('./')
    if source.startswith(unrelated):
        root.remove(include)
    elif without_sig and source == 'repositories/sig-core.xml':
        # Container-Base uses native Rocky packages. This SIG repository has no
        # riscv64 tools and its core-common URL is absent for this architecture.
        root.remove(include)
    elif source.startswith('container/'):
        container_found = True
if not container_found:
    raise RuntimeError('Upstream description does not include its container profiles')
tree.write(path, encoding='utf-8', xml_declaration=True)
