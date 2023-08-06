import setuptools
from setuptools import setup

VERSION="2.1.1"

setup(
    name="logger-decorator",
    author="Dmitriy Ignatiev",
    author_email="dmitrignatyev@gmail.com",
    version=VERSION,
    py_modules=["logger_decorator"],
    description="Logger decorator with request id",
    long_description="""
    Logger decorator with log request_id (optionally)
    """,
    install_requires=[
        "loguru"
    ],
    python_requires='>=3.6'
)
