from setuptools import setup
from distutils.command.upload import upload as upload_orig

with open("README.md") as readme:
    long_description = readme.read()


class Upload(upload_orig):
    def _get_rc_file(self):
        return "/.pypirc"


setup(
    name="es_lmr_iwf_api_helper",
    packages=["es_lmr_iwf_api_helper"],
    version="1.2.28",
    description="Helper for creating REST APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Proprietary",
    author="Munish Mehta",
    author_email="munish.mehta.au@gmail.com",
    url="",
    keywords=["flask", "rest", "api"],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    install_requires=[
        "Flask==2.1.3",
        "Werkzeug==2.1.2",
        "rfc5424-logging-handler==1.4.3",
        "yoyo-migrations==7.3.2",
        "setuptools==58.2.0",
        "SQLAlchemy==1.4.32",
        "flask-expects-json==1.7.0",
        "prometheus-client==0.14.1",
        "gunicorn==20.1.0",
        "gevent==21.12.0",
        "requests==2.28.1",
        "Flask-SQLAlchemy==2.5.1",
        "PyMySQL==1.0.2",
        "tzlocal==2.1",
    ],
    cmdclass={
        "upload": Upload,
    },
)
