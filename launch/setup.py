from setuptools import find_packages, setup

package_name = 'golf_trolley_waypoint_navigation'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name],
        ),
        (
            'share/' + package_name,
            ['package.xml'],
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='adriantee',
    maintainer_email='adriantee@example.com',
    description=(
        'Nav2 multiple-waypoint navigation node '
        'for the simulated autonomous golf trolley.'
    ),
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            (
                'golf_trolley_waypoints = '
                'golf_trolley_waypoint_navigation.'
                'golf_trolley_waypoints:main'
            ),
        ],
    },
)
