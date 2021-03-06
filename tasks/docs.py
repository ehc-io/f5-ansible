#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from invoke import task
from .lib.common import init

from .lib.common import BASE_DIR


@task(name='module')
def module_(c):
    result = c.run('python {0}/devtools/bin/limit_module_docs.py'.format(BASE_DIR))
    c.run('rm {0}/docs/modules/* || true'.format(BASE_DIR))

    cmd = [
        'python', '{0}/devtools/bin/plugin_formatter.py'.format(BASE_DIR),
        '--module-dir', '{0}/library/modules/'.format(BASE_DIR),
        '--template-dir', '{0}/devtools/templates/'.format(BASE_DIR),
        '--output-dir', '{0}/docs/modules/'.format(BASE_DIR),
        '-v',
        '--limit-to', result.stdout
    ]
    c.run(' '.join(cmd))


@task
def build(c):
    with c.cd("docs"):
        c.run("rm -rf _build")
        c.run("make html")


@task(module_, build)
def make(c):
    print("done")
