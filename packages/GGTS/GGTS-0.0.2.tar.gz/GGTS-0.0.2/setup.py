import setuptools
import pathlib
import pkg_resources

with pathlib.Path('requirements.txt').open() as requirements_txt:
    install_requires = [str(requirement) for requirement in pkg_resources.parse_requirements(requirements_txt)]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="GGTS",
    version="0.0.2",
    author="Javier Albaráñez Martínez",
    author_email="j.albar@geodb.com",
    description="This library allows to compress, visualize, generate and process sequences of geographic locations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AlbaranezJavier/GGTS",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        #"License :: ", #:: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

# https://packaging.python.org/en/latest/tutorials/packaging-projects/#uploading-your-project-to-pypi
# python setup.py sdist bdist_wheel
# python -m twine upload dist/*
# create .pypirc at home
# [distutils]
# index-servers=pypi
#
# [pypi]
# repository: https://upload.pypi.org/legacy/
# username: <your username>
# password: <your password>
#
# [testpypi]
# repository: https://test.pypi.org/legacy/
# username: <your username>
# password: <your password>