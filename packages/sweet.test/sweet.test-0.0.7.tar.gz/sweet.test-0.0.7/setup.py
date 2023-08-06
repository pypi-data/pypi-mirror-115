from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="sweet.test",
    version="0.0.7",
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
        'uvicorn'    # web
    ],      
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)