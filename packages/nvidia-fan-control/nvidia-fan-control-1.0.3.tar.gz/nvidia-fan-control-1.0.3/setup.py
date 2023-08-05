
import os

from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


data_files=[
    ("/usr/share/applications", ["nvidiafancontrol.desktop"]),
    ("/usr/share/pixmaps", ["nvidia_fan_control/nvidiafancontrol.svg"]),
    ("nvidia_fan_control", ["nvidia_fan_control/font.css"]),
    ('share/locale/en/LC_MESSAGES', ['languages/en/LC_MESSAGES/nvidiafancontrol.mo']),
    ('share/locale/it/LC_MESSAGES', ['languages/it/LC_MESSAGES/nvidiafancontrol.mo']),
]


setup(
    name='nvidia-fan-control',
    version='1.0.3',
    packages=['nvidia_fan_control'],
    url='https://github.com/tudo75/nvidia-fan-control',
    project_urls={
        "Bug Tracker": "https://github.com/tudo75/nvidia-fan-control/issues",
    },
    license='GNU General Public License v3.0',
    author='Nicola Tudino',
    author_email='tudo75@gmail.com',
    description='Nvidia Fan Control',
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    # scripts=['nvidiafancontrol'],
    entry_points="""
        [console_scripts]
        nvidiafancontrol = nvidia_fan_control.nvidiafancontrol:main
        """,
    data_files=data_files,
    keywords="nvidia fan control gui linux gpu speed",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: X11 Applications :: GTK",
        "Topic :: Utilities",
        "Intended Audience :: End Users/Desktop",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    install_requires=[
        'pycairo>=1.20.1',
        'pygobject>=3.36.0',
    ],
)
