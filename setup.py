from setuptools import setup

setup(
    name='tomocatdb',
    version='0.1.0',    
    description='Python database package',
    url='https://github.com/shuds13/pyexample',
    author='Nicolai Haaber Junge',
    author_email='n.h.junge@smn.uio.no',
    license='BSD 2-clause',
    packages=['tomocatdb'],
    install_requires=['sqlalchemy',
                      'psycopg2',                     
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)