import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read() + open("CHANGELOG.txt", "r").read()

setuptools.setup(
     name='aylien_message_puller',
     version='0.0.1',
     author="AYLIEN Engineering",
     author_email="eng-team@aylien.com",
     description="Tool for pulling messages from pubsub subscriptions",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="",
     packages=['aylien_message_puller'],
     install_requires=[
        "google-api-core==1.33.2",
        "google-cloud-pubsub==1.1.0",
        "google-cloud-core==1.1.0",
        "lz4==4.0.2"
     ],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
