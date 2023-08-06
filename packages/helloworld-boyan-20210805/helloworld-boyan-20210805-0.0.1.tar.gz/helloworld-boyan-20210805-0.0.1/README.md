# Publish to PyPI Demo

- PyPI - The Python Package Index
- https://packaging.python.org/tutorials/packaging-projects/#classifiers

1. Extract the reusable code into seperate modules.
2. Put it into 'project/src'
3. Create a new 'project/setup.py' 
4. `$ python setup.py bdist_wheel`
    ```
    ...
    creating build
    creating build/lib
    copying src/helloworld.py -> build/lib
    ...
    creating build/bdist.macosx-10.9-x86_64/wheel/helloworld-0.0.1.dist-info/WHEEL
    creating 'dist/helloworld-0.0.1-py3-none-any.whl' and adding 'build/bdist.macosx-10.9-x86_64/wheel' to it
    removing build/bdist.macosx-10.9-x86_64/wheel

    $ tree .
    .
    ├── README.md
    ├── build
    │   ├── bdist.macosx-10.9-x86_64
    │   └── lib
    │       └── helloworld.py
    ├── dist
    │   └── helloworld-0.0.1-py3-none-any.whl
    ├── setup.py
    └── src
        ├── helloworld.egg-info
        │   ├── PKG-INFO
        │   ├── SOURCES.txt
        │   ├── dependency_links.txt
        │   └── top_level.txt
        └── helloworld.py
    ```
5. Test install it locally 
    - 每次更新package， 都跑一遍：
    - `$ pip install -e .`  : '-e' flag links to the code rather than copy the code to install.
    ```
    $ pip install -e .
    Obtaining file:///Users/boyang/Documents/Dev/Python%20Demo%20Projects/publish-your-first-package-on-PyPI
    Installing collected packages: helloworld
        Running setup.py develop for helloworld
    Successfully installed helloworld
    ```
6. git ignore ([gitignore.io](gitignore.io))
7. Licence ([choosealicense.com](https://choosealicense.com))
8. Add classifiers in 'setup.py' (https://pypi.org/classifiers/)

8. Documentation (ReStructured Text (python doc, can use `**Sphinx**`) or Markdown (simpler, less powerful) version)
9. Testing (with `pytest`...)
10. Update Read setup.py for `install_requires` and extra `extras_require`.
    - then update README for developers
11. Source Distribution
    - `$ python setup.py sdist`
12. Add manifest for srce dis??....
13. Publish it!
    - python setup.py bdist_wheel sdist
    - `$ pip install twine`
    - `$ twine upload dist/*`
14. USE tox for testing different python environments

?. + 个test？


## Usage
```python
from helloworld import say_hello

```


## Developent
```bash
$ pip install -e .[dev]
```
