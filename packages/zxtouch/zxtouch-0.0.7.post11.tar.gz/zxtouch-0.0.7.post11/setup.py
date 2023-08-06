from os import path
from setuptools import setup


def readme():
    this_directory = path.abspath(path.dirname(__file__))
    with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
        return f.read()


setup(
    name='zxtouch',
    version='0.0.7-11',
    description='iOS Automation Framework iOS Touch Simulation Library',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://gitlab.com/marzzzello/zxtouch',
    author='xuan32546, marzzzello',
    author_email='zxtouch@07f.de',
    license='GPL-3.0',
    packages=['zxtouch'],
    python_requires='>=3.7',
    zip_safe=False,
)
