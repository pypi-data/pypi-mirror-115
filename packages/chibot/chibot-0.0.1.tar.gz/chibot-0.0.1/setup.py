from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='chibot',
    version='0.0.1',
    description='ChiBot is simple chatbot for python.',
    long_description=open('README.txt').read() + '\n\n' +
    open('CHANGELOG.txt').read(),
    url='',
    author='Tarun Bhardwaj',
    author_email='tarun.bhardwaj.developer@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='chatbot chibot chat bot',
    packages=find_packages(),
    install_requires=['re', 'random', 'json', 'datetime']
)
