from setuptools import find_packages, setup


INSTALL_REQUIRES = [
    'aiohttp',
    'aiohttp_apiset',
    'faker',
    'connexion'
]

setup(
    name='auth-service',
    version="0.1",
    description='Demos API',
    platforms=['POSIX'],
    package_dir={'': 'src'},
    packages=find_packages('src'),
    package_data={
        '': ['.openapi/swagger.yaml']
    },
    entry_points={
        'console_scripts': ['auth-service=auth.__main__:main']},
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    zip_safe=False,
)
