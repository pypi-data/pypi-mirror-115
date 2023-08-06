from setuptools import setup

with open("README.md", 'r') as fh:
    long_discription = fh.read()

setup(
    name='helloworld-boyan-20210805',          # this is what pip install
    version='0.0.2',  # 0.0.x >> unstable
    description='Say Hello now',
    long_description=long_discription,
    long_description_content_type="text/markdown",
    py_modules=['helloworldagain'], # this is what people import, not pip install.
    package_dir={'': 'src'},    #code is under 'src'
    install_requires=[
    ],
    extras_require= {
        "dev": [
            'pytest>=3.7',
        ],
    },
)
