from setuptools import setup

with open("README.md","r") as fh:
    long_description=fh.read()

setup(
    name='PandaTex',
    version='0.0.3',
    description='Say hello!',
    py_modules= ["helloworld"],
    package_dir={'':'src'},
    install_requires=["pandas","numpy"],
    classifiers=[
        "Programming Language :: Python :: 3.7"],
    long_description = long_description,
    long_description_content_type="text/markdown",
    extras_require={
        "dev":[
            "pytest>=3.7",
        ],
    },
    author="Marcelo Kenji Noda",
    author_email="nodamarcelokenjinoda@gmail.com",
    url="https://github.com/Marcelo-Kenji-Noda/"
)