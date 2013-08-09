"""
When doing 'hg push', print pushed revisions according to CHANGESET_FORMAT

Put file somewhere like ~/.hgext/push_urls.py

Then add to ~/.hgrc or <patch to repo>/.hg/hgrc

[extensions]
push_urls = /Users/alek/.hgext/push_urls.py
[hooks]
pre-push = python:push_urls.hook
"""
import subprocess
import re

CHANGESET_FORMAT = "<Kyle address here> {rev}"
CHANGESET_RE = re.compile(r'^changeset:\s+\d+:(\w+)$')

def hook(ui, repo, hooktype, node=None, source=None, **kwargs):
    if hooktype != 'pre-push' or 'opts' not in kwargs:
        return

    path = kwargs['pats'][0] if 'pats' in kwargs and kwargs['pats'] else ''
    
    cmd = "hg outgoing {} {} {} {}".format(
        " ".join("-B {}".format(b) for b in kwargs['opts']['bookmark']),
        " ".join("-b {}".format(b) for b in kwargs['opts']['branch']),
        " ".join("-r {}".format(r) for r in kwargs['opts']['rev']),
        path,
    )
    try:
        for l in subprocess.check_output(cmd, shell=True).split('\n'):
            m = CHANGESET_RE.match(l)
            if m:
                print CHANGESET_FORMAT.format(rev=m.group(1))
    except Exception, e:
        return
