from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'serial_motor_demo'

setup(
    name=package_name,
    version='0.0.1',
    package_dir={'': 'src'},
    packages=find_packages(exclude=['test'], where='src'),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
    ],
    install_requires=['setuptools', 'pyserial'],
    zip_safe=False,
    maintainer='user',
    maintainer_email='user@todo.todo',
    description='Serial motor demo package',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'motor_controller = serial_motor_demo.motor_controller:main',
            'serial_bridge = serial_motor_demo.serial_bridge:main',
        ],
    },
)