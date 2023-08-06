from setuptools import setup

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

install_requires = [
    "aiohttp==3.7.4.post0",
    "anyio==3.2.1",
    "async-timeout==3.0.1",
    "attrs==21.2.0",
    "certifi==2021.5.30",
    "chardet==4.0.0",
    "charset-normalizer==2.0.2",
    "idna==2.10",
    "multidict==5.1.0",
    "sniffio==1.2.0",
    "starlette==0.13.6",
    "typing-extensions==3.10.0.0",
    "urllib3==1.26.6",
    "yarl==1.6.3",
]

setup(
    long_description=long_description,
    name="external-logging-handlers",
    version="0.1.3",
    packages=["custom_handlers"],
    url="https://github.com/alexvoksa/logging-handlers",
    license="MIT License",
    author="Alexander",
    author_email="bf-109g@yandex.ru",
    description="Custom handlers for standard logging module",
    install_requires=install_requires,
    python_requires=">=3.9.1",
)
