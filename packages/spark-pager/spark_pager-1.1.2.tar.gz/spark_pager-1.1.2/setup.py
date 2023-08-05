import codecs
import os
from setuptools import setup


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()

setup(
    name='spark_pager',
    packages=['spark_pager'],
    version='1.1.2',
    description='A Python library for sending notifications on Spark Job Status.',
    author='Bright Emah',
    author_email='bemah2020@gmail.com',
    url = 'https://github.com/BrightEmah123/spark-pager',
    python_requires='>=3',
    install_requires=['mailthon'],
    include_package_data=True,
    long_description=read('README.md'),
    keywords=['spark', 'etl', 'pyspark'],
    long_description_content_type="text/markdown",
)