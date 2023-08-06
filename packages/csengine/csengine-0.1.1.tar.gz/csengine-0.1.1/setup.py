import os

import pkg_resources
from setuptools import setup, find_packages


package_dir = os.path.dirname(os.path.join(__file__))

with open('requirements/requirements.txt') as requirements_txt:
    requirements = [str(requirement) for requirement in pkg_resources.parse_requirements(requirements_txt)]

setup(
    name="csengine",
    version="0.1.1",
    packages=find_packages(exclude=('tests.*',)),
    install_requires=requirements,
    author="csdev",
    author_email='vmbdevel@gmail.com',
    license_files=('LICENSE.txt',),
    description="MVC framework",
    long_description=open("README.md").read(),
    keywords="engine mvc framework",
    url="",   # project home page, if any
    project_urls={
    },
    extras_require={
        "fastapi": ["fastapi==0.68.0", "starlette-prometheus==0.7.0", "starlette==0.13.6"],
        "aioredis": ["aioredis==1.3.1"],
        "redis": ["redis==3.5.3"],
        "gcloud-aio": ["gcloud-aio-storage==5.5.4", "aiohttp==3.6.2"],
        "gcloud": ["google-cloud-storage==1.29.0"],
        "rq": ["rq==1.5.0"],
        "es": ["elasticsearch>=7.0.0,<8.0.0"],
        "es-async": ["elasticsearch[async]>=7.0.0,<8.0.0"],
    },
    classifiers=[
        'Programming Language :: Python :: 3.8',    
        'Operating System :: POSIX :: Linux',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
