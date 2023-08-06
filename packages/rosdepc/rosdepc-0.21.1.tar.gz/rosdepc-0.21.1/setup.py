import os
from setuptools import setup

kwargs = {
    'name': 'rosdepc',
    # same version as in:
    # - src/roscdep2/__init__.py
    # - stdeb.cfg
    'version': '0.21.1',
    'packages': ['roscdep2', 'roscdep2.ament_packages', 'roscdep2.platforms'],
    'package_dir': {'': 'src'},
    # 'data_files': [("melodic",['src/roscdep2/rosdistro/melodic/distribution.yaml'])],
    'install_requires': ['catkin_pkg >= 0.4.0', 'rospkg >= 1.3.0', 'rosdistro >= 0.7.5', 'PyYAML >= 3.1'],
    'test_suite': 'nose.collector',
    'test_requires': ['mock', 'nose >= 1.0'],
    'author': 'Tully Foote, Ken Conley',
    'author_email': 'tfoote@osrfoundation.org',
    'url': 'http://wiki.ros.org/rosdep',
    'keywords': ['ROS'],
    'entry_points': {
        'console_scripts': [
            'rosdepc = roscdep2.main:rosdep_main',
            'rosdepc-source = roscdep2.install:install_main'
        ]
    },
    'classifiers': [
        'Programming Language :: Python',
        'License :: OSI Approved :: BSD License'],
    'description': 'rosdep package manager abstraction tool for ROS',
    'long_description': 'Command-line tool for installing system '
                        'dependencies on a variety of platforms.',
    'license': 'BSD',
}
if 'SKIP_PYTHON_MODULES' in os.environ:
    kwargs['packages'] = []
    kwargs['package_dir'] = {}
if 'SKIP_PYTHON_SCRIPTS' in os.environ:
    kwargs['name'] += '_modules'
    kwargs['entry_points'] = {}

setup(**kwargs)
