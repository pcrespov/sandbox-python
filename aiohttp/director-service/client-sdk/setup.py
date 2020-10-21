from setuptools import (
    find_packages, 
    setup
)


INSTALL_REQUIRES = [
    'aiohttp',
    'aiohttp_apiset',
    'trafaret',
    'trafaret-config'
]

TESTS_REQUIRE = [
    'faker',
    'pytest',
    'pyyaml'
]

    
setup(
    name='director-client-sdk',
    version="0.1",
    description='Demos API',
    platforms=['POSIX'],
    python_requires='>=3.6',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    package_data={
        '': ['.openapi/swagger.yaml']
    },
    entry_points={
        'console_scripts': ['director-client=director.__main__:main']},
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    tests_require=TESTS_REQUIRE,
    extras_require={
        'test': TESTS_REQUIRE
    },
    zip_safe=False
)
