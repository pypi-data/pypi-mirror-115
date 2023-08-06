from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='DataExtractionTiket',
    version='0.0.1',
    description='Air Travel Data Extraction Python Module',
    long_descriptiion=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Julian Tanja',
    author_email='jrtanja@bu.edu',
    license='MIT',
    classifiers=classifiers,
    keywords='data analysis, data science, data extraction',
    packages=find_packages(),
    install_requires=['']  #libraries that u need.

)