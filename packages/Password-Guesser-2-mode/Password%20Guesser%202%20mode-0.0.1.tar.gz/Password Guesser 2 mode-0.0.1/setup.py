from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8'
]

setup(
    name='Password Guesser 2 mode',
    version='0.0.1',
    description='A very basic Password Guesser',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Bennett Mewes',
    author_email='bennettmewes@yahoo.com',
    license='MIT',
    classifiers=classifiers,
    keywords='Password',
    packages=find_packages(),
    install_requires=['']
)