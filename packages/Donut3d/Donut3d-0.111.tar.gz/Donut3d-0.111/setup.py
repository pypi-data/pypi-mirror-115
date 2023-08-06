from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(name='Donut3d',
      version='0.111',
      description='3d ASCII Donut3d in python',
      long_description = long_description,
      long_description_content_type="text/markdown",
      packages=['Donut3d'],
      author_email='Grigoriev.ilia1@yandex.ru',
      zip_safe=False)
