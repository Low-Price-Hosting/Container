#!/usr/bin/env python3
"""Use a GitHub-supported token that can write the requested GHCR packages."""
import base64
import json
import os
import pathlib
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

DISTRIBUTIONS = {'Ubuntu', 'Debian', 'Centos', 'Alpine', 'Fedora', 'AlmaLinux', 'ArchLinux', 'RockyLinux'}


def request(url, method='GET', authorization=None):
    headers = {'Authorization': authorization, 'User-Agent': 'Low-Price-Hosting/Container'}
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers, method=method), timeout=30) as response:
        return response.status, dict(response.headers), response.read()


def can_write(token, username, repository):
    credential = base64.b64encode((username + ':' + token).encode()).decode()
    query = urllib.parse.urlencode({'service': 'ghcr.io', 'scope': 'repository:' + repository + ':pull,push'})
    _, _, body = request('https://ghcr.io/token?' + query, authorization='Basic ' + credential)
    registry_token = json.loads(body).get('token') or json.loads(body).get('access_token')
    if not registry_token:
        raise RuntimeError('Registry did not issue an access token')
    authorization = 'Bearer ' + registry_token
    # Start and cancel an empty upload. No image or tag is published by this check.
    status, headers, _ = request('https://ghcr.io/v2/' + repository + '/blobs/uploads/', 'POST', authorization)
    if status != 202:
        raise RuntimeError('Registry did not allow an upload')
    location = headers.get('Location') or headers.get('location')
    if not location:
        raise RuntimeError('Registry did not provide an upload location')
    location = urllib.parse.urljoin('https://ghcr.io', location)
    parsed = urllib.parse.urlparse(location)
    if parsed.scheme != 'https' or parsed.netloc != 'ghcr.io' or not parsed.path.startswith('/v2/' + repository + '/blobs/uploads/'):
        raise RuntimeError('Unexpected registry upload location')
    request(location, 'DELETE', authorization)


def login(distributions):
    if not distributions or not set(distributions) <= DISTRIBUTIONS:
        raise RuntimeError('Unknown distribution in registry login request')
    username = os.environ['GITHUB_ACTOR']
    owner = os.environ['GITHUB_REPOSITORY_OWNER'].lower()
    candidates = [('GITHUB_TOKEN', os.environ.get('GHCR_GITHUB_TOKEN', '')),
                  ('GH_TOKEN', os.environ.get('GHCR_ORGANIZATION_TOKEN', ''))]
    for name, token in candidates:
        if not token:
            print(name + ': secret is not available', flush=True)
            continue
        if token.startswith('github_pat_'):
            print(name + ': fine-grained PAT; GitHub Packages does not support this token type', flush=True)
            continue
        try:
            for distribution in sorted(set(distributions)):
                can_write(token, username, owner + '/' + distribution.lower())
        except urllib.error.HTTPError as error:
            print(name + ': registry access rejected (HTTP ' + str(error.code) + ')', flush=True)
            continue
        except (urllib.error.URLError, RuntimeError, ValueError) as error:
            # Never print request objects, credentials, registry tokens, or response bodies.
            print(name + ': registry check failed (' + type(error).__name__ + ')', flush=True)
            continue
        print('Publishing with ' + name + '; package upload access verified', flush=True)
        subprocess.run(['docker', 'login', 'ghcr.io', '--username', username, '--password-stdin'],
                       input=token + '\n', text=True, check=True)
        return
    raise RuntimeError('No supported token has package upload access. GITHUB_TOKEN needs Container Actions write access; an organization PAT must be classic with write:packages.')


if __name__ == '__main__':
    try:
        if sys.argv[1:2] == ['--plan']:
            plan = json.loads(pathlib.Path(sys.argv[2]).read_text())['include']
            distributions = [item['distribution'] for item in plan]
        else:
            distributions = sys.argv[1:]
        login(distributions)
    except (RuntimeError, subprocess.CalledProcessError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
