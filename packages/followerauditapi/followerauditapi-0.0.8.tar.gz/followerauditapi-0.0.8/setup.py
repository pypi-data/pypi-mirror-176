from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='followerauditapi',
    version='0.0.8',
    packages=['followeraudit'],
    description='Python library to access followeraudit API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/bytesview/followerauditapi-python',
    author='Followeraudit',
    author_email='contact@followeraudit.com',
    license='GNU V3',
    install_requires=["requests<3.0.0"],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',    
    python_requires='>=3.5',
    keywords=[
        'followerauditapi',
        'newaudit',
        'bulkaudit',
        'getaudit'
        ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Customer Service",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10"
      ] 

)
