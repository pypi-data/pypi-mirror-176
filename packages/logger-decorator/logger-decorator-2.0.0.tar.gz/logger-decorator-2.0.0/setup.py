from setuptools import setup

VERSION="2.0.0"

setup(
    name="logger-decorator",
    author="Dmitriy Ignatiev",
    author_email="dmitrignatyev@gmail.com",
    version=VERSION,
    py_modules=["universal_logger"],
    description="Logger decorator with request id",
    long_description="""
    Logger decorator with log request_id (optionally)
    """,
    install_requires=[
        "loguru"
    ]
)
