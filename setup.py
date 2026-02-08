from setuptools import setup, find_packages

setup(
    name="wg_auto_dplmnt",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'wg_auto_dplmnt=wg_auto_dplmnt.cli:main',
        ],
    },
)
