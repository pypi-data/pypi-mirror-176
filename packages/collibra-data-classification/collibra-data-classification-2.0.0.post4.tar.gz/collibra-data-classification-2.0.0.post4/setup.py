# coding: utf-8

"""
    Collibra Catalog classification API

    <p>The Catalog API offers functionality related to the catalog product.<br/> It is mainly focused on facilitating the ingestion of information into Catalog. The API enables users to more easily connect Catalog to sources that are not necessarily natively supported in the product. </p>  # noqa: E501

    The version of the OpenAPI document: 1.0
    Generated by: https://openapi-generator.tech
"""


from setuptools import setup, find_packages  # noqa: H301

NAME = "collibra-data-classification"
VERSION = "2.0.0-4"
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
    description="Collibra Catalog classification API",
    author="OpenAPI Generator community",
    author_email="team@openapitools.org",
    url="",
    keywords=["OpenAPI", "OpenAPI-Generator", "Collibra Catalog classification API"],
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    long_description="""\
    &lt;p&gt;The Catalog API offers functionality related to the catalog product.&lt;br/&gt; It is mainly focused on facilitating the ingestion of information into Catalog. The API enables users to more easily connect Catalog to sources that are not necessarily natively supported in the product. &lt;/p&gt;  # noqa: E501
    """
)
