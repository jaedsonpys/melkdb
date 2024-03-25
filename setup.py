from setuptools import setup

_version_globals = dict()

with open('melkdb/__version__.py') as f:
    exec(f.read(), _version_globals)

with open(f'README.md', 'r') as reader:
    readme = reader.read()

setup(
    author='Jaedson Silva',
    author_email='jaedson.dev@proton.me',
    name='melkdb',
    description='MelkDB: A faster key-value database',
    version=_version_globals['__version__'],
    long_description_content_type='text/markdown',
    long_description=readme,
    license='MIT License',
    install_requires=['pycryptodome==3.20'],
    packages=['melkdb'],
    url='https://github.com/jaedsonpys/melkdb',
    project_urls={
        'License': 'https://github.com/jaedsonpys/melkdb/blob/master/LICENSE',
        'Documentation': 'https://github.com/jaedsonpys/melkdb/tree/master/docs'
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Database :: Database Engines/Servers'
    ],
    keywords=['database', 'noSQL', 'key-value', 'db', 'engine']
)