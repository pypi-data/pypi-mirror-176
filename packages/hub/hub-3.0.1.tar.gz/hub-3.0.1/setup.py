from setuptools import setup


config = {
    "name": "hub",
    "version": "3.0.1",
    "description": "Activeloop Deep Lake",
    "long_description": "Use deeplake instead: pip install deeplake",
    "long_description_content_type": "text/x-rst",
    "author": "activeloop.ai",
    "author_email": "support@activeloop.ai",
    "install_requires": ["deeplake"],
    "zip_safe": False,
    "url": "https://www.github.com/activeloopai/deeplake",
    "license": "MPL-2.0",
    "classifiers": [
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
    ],
}

setup(**config)
