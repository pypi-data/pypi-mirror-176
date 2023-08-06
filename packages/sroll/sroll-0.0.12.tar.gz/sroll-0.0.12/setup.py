from setuptools import setup

setup(
    name='sroll',
    version='0.0.12',    
    description='Python package for SRoll installation',
    ong_description ='test of desciption for sroll.\n Package for installation of sroll, create virtualenv, update python path and clone sroll repository to path.',
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
)

