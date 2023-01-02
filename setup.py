"""Setup file for OIDIA."""

##############################################################################
# Python imports.
from pathlib    import Path
from setuptools import setup, find_packages

##############################################################################
# Import the library itself to pull details out of it.
import oidia

##############################################################################
# Work out the location of the README file.
def readme():
    """Return the full path to the README file.

    :returns: The path to the README file.
    :rtype: ~pathlib.Path
    """
    return Path( __file__ ).parent.resolve() / "README.md"

##############################################################################
# Load the long description for the package.
def long_desc():
    """Load the long description of the package from the README.

    :returns: The long description.
    :rtype: str
    """
    with readme().open( "r", encoding="utf-8" ) as rtfm:
        return rtfm.read()

##############################################################################
# Perform the setup.
setup(

    name                          = "oidia",
    version                       = oidia.__version__,
    description                   = str( oidia.__doc__ ),
    long_description              = long_desc(),
    long_description_content_type = "text/markdown",
    url                           = "https://github.com/davep/oidia",
    author                        = oidia.__author__,
    author_email                  = oidia.__email__,
    maintainer                    = oidia.__maintainer__,
    maintainer_email              = oidia.__email__,
    packages                      = find_packages(),
    package_data                  = { "oidia": [ "py.typed" ] },
    include_package_data          = True,
    install_requires              = [ "textual==0.9.1", "xdg" ],
    python_requires               = ">=3.10",
    keywords                      = "terminal textual streak todo",
    entry_points                  = {
        "console_scripts": "oidia=oidia.app:run"
    },
    license                       = (
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)"
    ),
    classifiers                   = [
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Environment :: Console",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Utilities",
        "Topic :: Terminals",
        "Typing :: Typed"
    ]

)

### setup.py ends here
