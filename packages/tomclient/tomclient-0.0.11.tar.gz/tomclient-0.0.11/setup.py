from setuptools import setup, find_packages

setup(
    name='tomclient',
    author="Xiaozhe Yao",
    author_email="askxzyao@gmail.com",
    description="TOMClient is a client library for TOM",
    version='0.0.11',
    scripts=["tomclient/tom"],
    package_dir={'tomclient': 'tomclient'},
    packages=find_packages(),
    install_requires=[
        "typer",
        "jsonrpc-websocket",
        "netifaces",
        "pynvml",
        "py3nvml",
        "requests",
    ]
)