

- This folder creates ``packaging_tutorial`` following the tutorial in the [Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/): 
- [``pip`` build system](https://pip.pypa.io/en/stable/reference/build-system): ``pyproject-toml`` and ``setup-py``(legacy)
- Installation from repo (based on [VCS support doc](https://pip.pypa.io/en/stable/topics/vcs-support/))
```
    $ pip install "git+https://github.com/pcrespov/sandbox-python.git@python-stuff#egg=example-package&subdirectory=packaging/example-package"    
```
NOTE: do not forget quotes!