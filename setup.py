from setuptools import setup, find_packages


def readme():
    try:
        with open('README.md') as f:
            return f.read()
    except BaseException:
        pass


setup(
    name='termicoder',
    version='0.3.0',
    url='https://github.com/termicoder/termicoder',
    author='Divesh Uttamchandani',
    author_email='diveshuttamchandani@gmail.com',
    license='MIT',
    description='CLI to view, code & submit problems directly from terminal',
    long_description=readme(),
    long_description_content_type='text/markdown',
    keywords='competitive codechef oj',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Education',
        'Topic :: Education',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
      ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'requests',
        'beautifulsoup4',
        'click-default-group',
        'click-repl',
        'click_completion',
        'requests_oauthlib',
        'pyyaml',
        'click-log',
        'pyperclip',
        'beautifultable',
        'Markdown',
        'Tomd',
        'mdv'
    ],
    entry_points='''
        [console_scripts]
        termicoder=termicoder.cli:main
        [termicoder.judge_plugins]
        codechef=termicoder.judges:Codechef
    ''',
    project_urls={
        'Bug Reports': 'https://github.com/termicoder/termicoder/issues',
        'Say Thanks!': 'https://saythanks.io/to/diveshuttam',
        'Source': 'https://github.com/termicoder/termicoder/',
    }
)
