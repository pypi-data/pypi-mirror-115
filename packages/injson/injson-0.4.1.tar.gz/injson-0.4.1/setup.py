from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="injson",
    version="0.4.1",
    author="Leo Tong",
    author_email="tonglei@qq.com",
    description="Test the sub json if or not in parent json",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sweeterio/injson",
    py_modules=['injson'],
    install_requires=[],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3"
    ],
    entry_points={

    }
)
