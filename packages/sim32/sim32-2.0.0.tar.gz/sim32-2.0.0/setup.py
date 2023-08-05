from setuptools import setup


PACKAGE_NAME = 'sim32'
VERSION = "2.0.0"

REQUIRES = ["beautiful_repr==1.1.1", "pyoverload==1.1.24", "colorama==0.4.6"]


with open('README.md') as readme_file:
    LONG_DESCRIPTION = readme_file.read()

setup(
    name=PACKAGE_NAME,
    description="Library to help you write games",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    version=VERSION,
    url="https://github.com/TheArtur128/SimEngine",
    download_url=f"https://github.com/TheArtur128/SimEngine/archive/refs/tags/{VERSION}.zip",
    author="Arthur",
    author_email="s9339307190@gmail.com",
    install_requires=REQUIRES,
    python_requires='>=3.10',
    packages=[
        PACKAGE_NAME,
        f"{PACKAGE_NAME}.pygame_integration",
        f"{PACKAGE_NAME}.examples",
        f"{PACKAGE_NAME}.errors"
    ],
    package_dir={
        PACKAGE_NAME: "sim32",
        f"{PACKAGE_NAME}.pygame_integration": "pygame_integration",
        f"{PACKAGE_NAME}.examples": "examples",
        f"{PACKAGE_NAME}.errors": "errors"
    }
)
