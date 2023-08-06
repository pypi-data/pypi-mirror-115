#!/usr/bin/env python
# coding: utf-8

import setuptools

setuptools.setup(
    version='0.0.3',
    keywords='mkdocs python markdown wiki mkdocs-edit',
    name="mkdocs-edit-url",
    license='GNU',
    python_requires='>=3.5',
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
