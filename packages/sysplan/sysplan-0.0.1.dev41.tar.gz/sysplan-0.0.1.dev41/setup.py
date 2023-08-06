from setuptools import setup


setup(
    name='sysplan',
    version='0.0.1.dev41',
    setup_requires='setupmeta',
    install_requires=['cli2'],
    extras_require=dict(
        colors=['pygments'],
        test=[
            'pytest',
            'pytest-cov',
        ],
    ),
    author='James Pic',
    author_email='jamespic@gmail.com',
    url='https://yourlabs.io/oss/sysplan',
    include_package_data=True,
    license='MIT',
    keywords='sysplan',
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'sysplan = sysplan.cli:cli.entry_point',
        ],
        'sysplan': [
            'services = sysplan.systemd:ServicePlan',
            'mounts = sysplan.systemd:MountPlan',
            'timers = sysplan.systemd:TimerPlan',
            'files = sysplan.files:FilePlan',
            'docker = sysplan.docker:DockerConfig',
        ],
    },
)
