from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="sweetest",
    version="1.4.4",
    author="tonglei",
    author_email="tonglei@qq.com",
    description="Sweet experience version",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sweeterio/sweet",
    packages=['sweet'],
    package_data={'sweet': ['*.py', 'lib/*py', 'modules/*py']},
    install_requires=[
        'openpyxl',  # excel
        'loguru',    # log
        'arrow',     # report
        'starlette', # web
        'uvicorn',   # web
        'sweet.web',
        'sweet.http'
    ],      
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)