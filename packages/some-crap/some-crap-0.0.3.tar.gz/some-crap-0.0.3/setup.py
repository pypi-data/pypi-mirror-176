from os import path
from setuptools import setup
import some_crap

# read the README for long_description
cwd = path.abspath(path.dirname(__file__))
with open(path.join(cwd, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='some-crap',
    description='Python client for evidently nothing',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version=some_crap.__version__,
    license='MIT',
    author='Some Random guy',
    author_email='some-random-guy@gmail.com',
    # url='https://github.com/percy/percy-appium-python',
    keywords='nothing crap',
    packages=['some_crap'],
    include_package_data=True,
    install_requires=[
        'Appium-Python-Client==1.*',
        'requests==2.*'
    ],
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    test_suite='tests',
    tests_require=['Appium-Python-Client', 'httpretty', 'requests'],
    zip_safe=False
)
