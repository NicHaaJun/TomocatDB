from setuptools import setup, find_packages

setup(
    name='tomocatdb',
    version='0.1.0',    
    description='Python database package',
    url='https://github.com/NicolaiHaaberJunge/TomocatDB',
    author='Nicolai Haaber Junge',
    author_email='n.h.junge@smn.uio.no',
    license='MIT',
    install_requires=['sqlalchemy',
                      'psycopg2',                     
                      'pandas'],
    entry_points={
        'console_scripts': [
            'tomodb=bin.tomodb:main'
        ]
    },
    packages=find_packages(),
)