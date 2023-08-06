# hub-redirect
Redirects "pip install hub" and "import hub" to deeplake

This is an empty package with `deeplake` as the only dependancy, essentially serving as a backwards compatibility redirect for pip installs. Also the `__init__` redirects `import hub` to `import deeplake`.
