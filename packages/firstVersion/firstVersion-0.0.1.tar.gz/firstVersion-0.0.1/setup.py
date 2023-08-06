from setuptools import setup, find_packages

classifiers=[
    'Development Statut ::5 - Production/Satble',
    'Intended Audience :: Education',
    'Operating System :: MIT License',
    'Programming Language :: Python :: 3'

]

setup(
    name='firstVersion',
    version='0.0.1',
    description='A very basic calculator',
    Long_description=open('Readme.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='sokhar samb',
    author_email='ssamb@aimsammi.org',
    licence='MIT',
    classifier= classifiers,
    keywords='calculator',
    package=find_packages(),
    install_requires=['']


)