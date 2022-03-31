

- This folder creates ``packaging_tutorial`` following the tutorial in the [Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/): 
- [``pip`` build system](https://pip.pypa.io/en/stable/reference/build-system): ``pyproject-toml`` and ``setup-py``(legacy)
- Installation from repo (based on [VCS support doc](https://pip.pypa.io/en/stable/topics/vcs-support/))
```cmd
    $ pip install "git+https://github.com/pcrespov/sandbox-python.git@python-stuff#egg=example-package&subdirectory=packaging/example-package"    
        Collecting example-package
        Cloning https://github.com/pcrespov/sandbox-python.git (to revision python-stuff) to /tmp/pip-install-d6a85cvu/example-package_8ee4118ea3b143f5bc1c8dfc724b3480
        Running command git clone --filter=blob:none -q https://github.com/pcrespov/sandbox-python.git /tmp/pip-install-d6a85cvu/example-package_8ee4118ea3b143f5bc1c8dfc724b3480
        Resolved https://github.com/pcrespov/sandbox-python.git to commit 28df6b331fc0486fe56a11cee40d132ebd99c2a5
        Installing build dependencies ... done
        Getting requirements to build wheel ... done
        Preparing metadata (pyproject.toml) ... done
        Building wheels for collected packages: example-package
        Building wheel for example-package (pyproject.toml) ... done
        Created wheel for example-package: filename=example_package-0.0.1-py3-none-any.whl size=2614 sha256=08795666b6f7682c8f5e1ce69261aed71d77612509ee0e93b1e4e92cc3d9ec3c
        Stored in directory: /tmp/pip-ephem-wheel-cache-apsu_9dv/wheels/bf/06/f8/0e4e0a463766d1b7148414fa3c8cd5eccf7a17c49e784c4680
        Successfully built example-package
        Installing collected packages: example-package
        Successfully installed example-package-0.0.1
    $ pip list | grep example-package
        example-package   0.0.1
```
NOTE: do not forget quotes!