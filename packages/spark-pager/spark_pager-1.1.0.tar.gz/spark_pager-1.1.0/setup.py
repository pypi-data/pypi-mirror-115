from setuptools import setup

setup(
    name='spark_pager',
    packages=['spark_pager'],
    version='1.1.0',
    description='Mail Notifier for all Spark Jobs',
    author='Bright Emah',
    author_email='bemah2020@gmail.com',
    url = 'https://github.com/BrightEmah123/spark-pager',
    python_requires='>=3',
    install_requires=['mailthon'],
    include_package_data=True
)