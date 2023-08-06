from setuptools import setup

setup(
    name='sroll',
    version='0.0.6',    
    description='Python package for SRoll installation',
    url='https://gitlab.ifremer.fr/iaocea/srollex.git',
    author='Theo Foulquier',
    author_email='tfoulqui@ifemer.fr',
    license='BSD 2-clause',
    include_package_data = True,
    packages=['sroll_package'],
    install_requires=['virtualenv','numpy',                                          
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3.6',
    ],

    python_requires = ">=3.6"
)

