# coding: utf-8

"""
    Collibra Import API

    <p>The Import API is an efficient way to load large volumes of data into the Collibra Data Governance Center. The API can automatically differentiate between creating and updating data.</p>  # noqa: E501

    The version of the OpenAPI document: 2.0
    Generated by: https://openapi-generator.tech
"""


from setuptools import setup, find_packages  # noqa: H301

NAME = "collibra-importer"
VERSION = "2.0.0-3"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["urllib3 >= 1.15", "six >= 1.10", "certifi", "python-dateutil"]

setup(
    name=NAME,
    version=VERSION,
    description="Collibra Import API",
    author="OpenAPI Generator community",
    author_email="team@openapitools.org",
    url="",
    keywords=["OpenAPI", "OpenAPI-Generator", "Collibra Import API"],
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    long_description="""\
    &lt;p&gt;The Import API is an efficient way to load large volumes of data into the Collibra Data Governance Center. The API can automatically differentiate between creating and updating data.&lt;/p&gt;  # noqa: E501
    """
)
