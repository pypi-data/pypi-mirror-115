from setuptools import setup, find_packages


setup(
    long_description=open("README.md", "r").read(),
    name="loragateway",
    version="0.3",
    description="lora gateway",
    author="Pascal Eberlein",
    author_email="pascal@eberlein.io",
    url="https://github.com/nbdy/loragateway",
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License'
    ],
    keywords="lora gateway",
    packages=find_packages(),
    install_requires=[
        "paho-mqtt", "loguru", "dataset", "loraspi"
    ],
    entry_points={
        'console_scripts': [
            'loragw = loragateway.__main__:main'
        ]
    },
    long_description_content_type="text/markdown",
)