from setuptools import setup, find_packages

setup(
    name='termicoder',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'requests',
        'beautifulsoup4'
    ],
    entry_points='''
        [console_scripts]
        termicoder=termicoder.cli:main
    '''
)
