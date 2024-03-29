from setuptools import setup, find_packages
from setuptools.glob import glob

setup(
    name='dmx-priest',
    version='0.1',
    description='Record and play back dmx presets over Art-Net',
    url='https://github.com/Virusmater/dmx-priest',
    author='Dima Kompot',
    author_email='virusmater@gmail.com',
    license='GPLv3',
    install_requires=['gpiozero', 'smbus', 'pyserial'],
    packages=find_packages(),
    package_data={'dmx_priest': ['presets/*']},
    entry_points=dict(
        console_scripts=['dmx-priest=dmx_priest.main:main']
    )
)