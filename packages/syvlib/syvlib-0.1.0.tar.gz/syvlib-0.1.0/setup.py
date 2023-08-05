from setuptools import setup

setup(
    name='syvlib',
    version='0.1.0',
    description='Array codec and API wrapper for SYV server',
    url='https://bitbucket.org/Thomas_Ash/syvlib/',
    author='Thomas Ash',
    author_email='syv.development@protonmail.com',
    license='GPL',
    packages=['syvlib'],
    zip_safe=True,
    install_requires=['numpy']
)
