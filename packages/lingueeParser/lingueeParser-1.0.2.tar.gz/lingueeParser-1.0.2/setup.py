from setuptools import setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')


setup(
    name='lingueeParser',
    version='1.0.2',
    packages=['lingueeParser'],
    install_requires=['lxml', 'requests'],
    url='https://github.com/Schlaumra/linguee-parser',
    license='GPL3',
    author='schlaumra',
    author_email='amhof13raphael10@gmail.com',
    description='Linguee translation parser',
    long_description=long_description,
    long_description_content_type='text/markdown',
)
