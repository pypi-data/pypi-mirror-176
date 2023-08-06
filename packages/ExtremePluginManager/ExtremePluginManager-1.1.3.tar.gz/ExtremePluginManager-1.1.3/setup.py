from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

packages = find_packages(where=".")

if "tests" in packages:
    packages.remove("tests")

setup(
    name='ExtremePluginManager',
    version='1.1.3',
    packages=packages,
    url='https://github.com/CPSuperstore/ExtremePluginManager',
    license='MIT Licence',
    author='CPSuperstore',
    author_email='cpsuperstoreinc@gmail.com',
    description='A powerful library for managing plugins in your Python application.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        "Bug Tracker": "https://github.com/CPSuperstore/ExtremePluginManager/issues",
    },
    keywords=['Plugin', 'Manager'],
    install_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Topic :: Desktop Environment',
        'Topic :: Games/Entertainment',
        'Topic :: Software Development',
        'Topic :: Utilities'
    ]
)
