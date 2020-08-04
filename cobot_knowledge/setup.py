import os
from glob import glob
from setuptools import setup

package_name = 'cobot_knowledge'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name, glob('resource/database/*.owl')),
        ('share/' + package_name + '/user_defined/', glob('resource/user_defined/*.owl')),
        (os.path.join('share', package_name), glob('launch/*.launch.py'))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='alex',
    maintainer_email='alexandre.angleraud@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'world = cobot_knowledge.world:main'
        ],
    },
)
