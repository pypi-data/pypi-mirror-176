from mtel_client import __version__
from setuptools import setup

setup(
    name="mtel_client",
    version=__version__,
    description="Little client for getting profile info from MTEL Montenegro",
    url="https://github.com/infnetdanpro/mtel-montenegro-data/",
    author="Maksim Artemev",
    author_email="danpro334@gmail.com",
    packages=["mtel_client"],
    install_requires=["httpx", "pydantic[email]"],
)
