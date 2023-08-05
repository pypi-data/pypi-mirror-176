import os

from setuptools import setup

# Readme as long description
with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme_file:
    long_description = readme_file.read()

setup(
    name="django-auditlog-with-elasticsearch-indexing",
    url="https://github.com/Eslamhathout/django-auditlog-with-elasticsearch-indexing",
    license="MIT",
    author="ehathout",
    description="Audit log app for Django with Elasticsearch indexing.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
    install_requires=["Django>=3.2", "python-dateutil>=2.7.0"]
)
