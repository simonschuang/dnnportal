import os
import setuptools


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

# Get current __version__
version_locals = {}
execfile(os.path.join(os.path.dirname(__file__),'dnnport', 'version.py'), {}, version_locals)


setuptools.setup(
    name = "dnnport",
    version=version_locals['__version__'],
    author = "Simon Chuang",
    author_email = "simon.s.chuang@gmail.com",
    description = ("An DNN training portal."),
    license = "MIT",
    keywords = "dnn",
    url = "https://github.com/simonschuang/dnnportal",
    packages=setuptools.find_packages(),
    long_description=read('README.md'),
    classifiers=[
        "Framework :: Flask",
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=read('requirements.txt'),
    scripts=['dnnport-server'],
)
