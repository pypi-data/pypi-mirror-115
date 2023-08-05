from setuptools import setup, find_packages


classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='frozenSpider',
    version='0.0.6',
    description='Library to implement and visualise ML Algorithms',
    long_description=open('ReadMe.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='https://github.com/mrfrozen97',
    author='mr_frozen97',
    author_email='mrfrozenpeak@gmail.com',
    license="MIT",
    classifiers=classifiers,
    keywords='ml algorithms',
    packages=find_packages(),
    install_requires=['numpy']
)