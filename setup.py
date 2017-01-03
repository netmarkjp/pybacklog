from setuptools import setup

setup(
    name="pybacklog",
    version="0.0.1",
    description="Backlog API v2 Client",
    author="Toshiaki Baba",
    author_email="toshiaki@netmark.jp",
    url="https://github.com/netmarkjp/pybacklog",
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Topic :: Utilities",
    ],
    packages=["pybacklog"],
    requires=["requests"],
)
