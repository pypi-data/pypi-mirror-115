import setuptools

setuptools.setup(
    name="mkdocs-edit-url",
    version='0.0.4',
    keywords='mkdocs python markdown wiki mkdocs-edit',    
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
