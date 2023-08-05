import logging
import setuptools
from distutils.errors import CCompilerError, DistutilsExecError, DistutilsPlatformError
from Cython import Distutils

_version="0.7.5"
logging.basicConfig()
log = logging.getLogger(__file__)

ext_errors = (CCompilerError, ModuleNotFoundError, DistutilsExecError, DistutilsPlatformError, IOError, SystemExit)

with open("README.rst", 'r') as f:
    long_description = f.read()


class CustomBuildExtCommand(Distutils.build_ext):
    """build_ext command for use when numpy headers are needed."""

    def run(self):
        import numpy
        self.include_dirs.append(numpy.get_include())
        Distutils.build_ext.run(self)
        
        
setup_args = {'name':"classixclustering",
        'packages':["classix"],
        'version':_version,
        'install_requires':["numpy>=1.17.3",
                            "scipy>=0.7.0",
                            "pandas", 
                            "matplotlib>=3.5",
                            "requests"],
        'package_data':{"classix": ["aggregation_c.pyx",
                                "aggregation_cm.pyx", 
                                "merging_cm.pyx"]
                    },
        'cmdclass': {'build_ext': CustomBuildExtCommand},
        'classifiers':["Intended Audience :: Science/Research",
                "Intended Audience :: Developers",
                "Programming Language :: Python",
                "Topic :: Software Development",
                "Topic :: Scientific/Engineering",
                'Operating System :: Microsoft :: Windows',
                'Operating System :: POSIX',
                'Operating System :: Unix',
                'Operating System :: MacOS',
                "Programming Language :: Python :: 3",
                "Programming Language :: Python :: 3.6",
                "Programming Language :: Python :: 3.7",
                "Programming Language :: Python :: 3.8",
                "Programming Language :: Python :: 3.9",
                "Programming Language :: Python :: 3.10"
                ],
        'long_description':long_description,
        'author':"Xinye Chen, Stefan Güttel",
        'author_email':"xinye.chen@manchester.ac.uk, stefan.guettel@manchester.ac.uk",
        'description':"Fast and explainable clustering based on sorting",
        'long_description_content_type':'text/x-rst',
        'url':"https://github.com/nla-group/CLASSIX.git",
        'license':'MIT License'
}

try:
    from Cython.Build import cythonize
    
    setuptools.setup(
        setup_requires=["cython", "numpy>=1.17.3"],
        ext_modules=cythonize(["classix/*.pyx"], include_path=["classix"]),
        **setup_args
    )


except ext_errors as ext:
    log.warn(ext)
    log.warn("The C extension could not be compiled.")

    setuptools.setup(setup_requires=["numpy>=1.17.3"], **setup_args)
    log.info("Plain-Python installation succeeded.")
    
    
