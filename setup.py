from setuptools import setup, find_packages

setup(
    name="wg_auto_deploy",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'wg_auto_deploy=wg_auto_deploy.cli:main',
        ],
    },
)
