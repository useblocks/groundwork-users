"""
groundwork-users
================
"""
from setuptools import setup, find_packages
import re
import ast

_version_re = re.compile(r'__version__\s+=\s+(.*)')
with open('groundwork_users/version.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    name='groundwork-users',
    version=version,
    url='http://groundwork-users.readthedocs.io',
    license='MIT license',
    author='team useblocks',
    author_email='groundwork@useblocks.com',
    description="Plugins and Patterns for managing users inside a groundwork application",
    long_description=__doc__,
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    platforms='any',
    setup_requires=[],
    tests_require=[],
    install_requires=['groundwork-database>=0.1.3', 'flask-babel', 'flask-security',
                      'groundwork-web>=0.1.3', 'groundwork>=0.1.10'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    entry_points={
        'console_scripts': [],
        'groundwork.plugin': ["gw_users_web="
                              "groundwork_users.plugins.gw_users_web_manager.gw_users_web_manager:GwUsersWebManager"],
    }
)
