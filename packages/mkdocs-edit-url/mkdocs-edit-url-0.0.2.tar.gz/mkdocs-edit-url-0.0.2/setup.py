#!/usr/bin/env python
# coding: utf-8

import setuptools

setuptools.setup(
    version='0.0.2',
    name="mkdocs-edit-url",
     install_requires=[
        'mkdocs>=1',
        'wcmatch>=7'
    ],
    entry_points={
        'mkdocs.plugins': [
            'mkdocs-edit-url = mkdocs_edit_url.plugin:EditUrlPlugin',
        ]
    }
)
