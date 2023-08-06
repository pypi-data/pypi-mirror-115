# Python module for binary_c
Docstring coverage: 
![docstring coverage](./badges/docstring_coverage.svg)
Test coverage: 
![test coverage](./badges/test_coverage.svg)

Binary population synthesis code that interfaces with binary_c. Based on a original work by Jeff Andrews (can be found in old_solution/ directory). Updated and extended for Python3 by David Hendriks, Robert Izzard.

The current release is version 0.4, make sure to use that version number when installing!

## Requirements
To run this code you need to at least have installations of:

- Python 3.6 or higher
- binary_c version 2.1.7 or higher

And the following python packages (which will get installed automatically when installing with pip):

- numpy
- pytest
- h5py
- pathos
- pandas
- astropy
- matplotlib
- py_rinterpolate

## Environment variables
Before compilation you need to have certain environment variables:

Required:

- `BINARY_C` should point to the root directory of your binary_c installation
- `LD_LIBRARY_PATH` should include $BINARY_C/src and whatever directories are required to run binary_c (e.g. locations of libgsl, libmemoize, librinterpolate, etc.)
- `LIBRARY_PATH` should include whatever directories are required to build binary_c (e.g. locations of libgsl, libmemoize, librinterpolate, etc.)
- `GSL_DIR` should point to the root location where you installed GSL to. This root dir should contain `bin/`, `lib/` etc

## Build instructions
First, make sure you have built binary_c (See `$BINARY_C/doc/binary_c2.pdf` section: installation for all the installation instructions for `binary_c`)) and that it functions correctly. 

### Installation via PIP:
To install this package via pip:

```
pip install binarycpython
```

### Installation from source:
For this it is best to set up a virtual environment. Activate the virtualenvironment and enter the cloned version of the repo.

Then run:
```
python setup.py clean && python setup.py build --force && python setup.py sdist && pip install -v dist/binarycpython-<version of this package>.tar.gz
```
You can find the version of this package in setup.py.

This will install this package into the virtual environment. Making changes to the sourcecode can be "installed" into the virtual env with the same command. 

If this is not the first time you install the package, but rather rebuild it because you make changes in either binary_c or binarycpython, you should ignore the currently installed version, and also skip installing the dependencies again, by executing the following command:
```
python setup.py clean && python setup.py build --force && python setup.py sdist && pip install --ignore-installed --no-dependencies -v dist/binarycpython-<version of this package>.tar.gz
```

#### After installation
After installing the code via source it is useful to run the test suite before doing any programming with it. The test suite is stored in `binarycpython/tests` and running `python main.py` in there will run all the tests. 

## Examples
See the examples/ directory for example scripts and notebooks. The documentation contains example pages as well. 

## Usage notes
Make sure that with every change/recompilation you make in `binary_c`, you also rebuild this package. Whenever you change the sourcecode of this package, you need to reinstall it into your virtualenvironment as well

## Documentation
Look in the docs/ directory. Within the build/html/ there is the html version of the documentation. The 

## FAQ/Issues:
Building issues with binary_c itself: 
- see the documentation of binary_c (in doc/). 
- If you have MESA installed, make sure that the `$MESASDK_ROOT/bin/mesasdk_init.sh` is not sourced. It comes with its own version of some programs, and those can interfere with installing.  

When Pip install fails:
- Run the installation with `-v` and/or `--log <logfile>` to get some more info
- If gcc throws errors like `gcc: error: unrecognized command line option ‘-ftz’; did you mean ‘-flto’?`, this might be due to that the python on that system was built with a different compiler. It then passes the python3.6-config --cflags to the binarycpython installation, which, if done with gcc, will not work. Try a different python3.6. I suggest using `pyenv` to manage python versions. If installing a version of python with pyenv is not possible, then try to use a python version that is avaible to the machine that is built with the same compiler as binary_c was built with. 
- if pip installation results in `No files/directories in /tmp/pip-1ckzg0p9-build/pip-egg-info (from PKG-INFO)`, try running it verbose (`-v`) to see what is actually going wrong. 
- If pip terminates with the error FileNotFoundError: [Errno 2] No such file or directory: '<...>/binary_c-config' Then make sure that the path to your main $BINARY_C directory is set correctly.

Other:
- When running jupyter notebooks, make sure you are running the jupyter installation from the same virtual environment. 
- When the output of binary_c seems to be different than expected, you might need to rebuild this python package. Everytime binary_c is compiled, this package needs to be rebuilt too.