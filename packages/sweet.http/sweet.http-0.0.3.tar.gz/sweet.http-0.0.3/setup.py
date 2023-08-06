from setuptools import setup


with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="sweet.http",
    version="0.0.3",
    author="tonglei",
    author_email="tonglei@qq.com",
    description="Sweet's http autotest module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sweeterio/http",
    packages=['sweet.modules'],
    package_data={'.': ['*.py']},
    install_requires=[
        'requests',
        'injson'
    ],            
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)