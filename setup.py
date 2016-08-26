# -*- coding: utf-8 -*-
from setuptools import setup

with open('README.md') as f:
    Readme = f.read()

with open('LICENSE') as f:
    License = f.read()

install_requires = [
    "flask",
    "PyWechatAPI",
    "qrcode"
]

setup(
    name='flask-wechat-auth',
    version='0.0.1',
    description='WeChat Flask Blueprint Module',
    long_description=Readme,
    author='CaoKe',
    author_email='hitakaken@gmail.com',
    url='https://github.com/hitakaken/flask-wechat.git',
    license=License,
    platforms=["any"],
    packages=['mod_wechat'],
    # test_suite="test.tests",
    install_requires=install_requires,
    # tests_require=['nose'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ]
)
