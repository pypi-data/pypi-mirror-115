from setuptools import setup

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

install_requires = [
    "aiohttp>=3.7.4.post0",
    "starlette>=0.13.6",
]

setup(
    long_description=long_description,
    name="external-logging-handlers",
    version="0.1.4",
    packages=["custom_handlers"],
    url="https://github.com/alexvoksa/logging-handlers",
    license="MIT License",
    author="Alexander",
    author_email="bf-109g@yandex.ru",
    description="Custom handlers for standard logging module",
    install_requires=install_requires,
    python_requires=">=3.9.1",
)
