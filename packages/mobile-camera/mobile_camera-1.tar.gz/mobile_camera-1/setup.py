from setuptools import setup, find_packages
import codecs
import os

VERSION = '1'
DESCRIPTION = 'Access mobile camera'
LONG_DESCRIPTION = """For accessing a mobile camera install this library on your desktop.
Then download IP Webcam App on android phone. After installing the app click on start server.
Give all permissions to the app. You will get IPv4 & IPv6 ip address. Copy TPv4 ip address.
Then open browser on your desktop and paste that url on browser. You will get some opption.
Select Javascript. You will get a preview. Then open python file. See the example file.
Then write that code. You can take ip by taking input or you can also give the ip address on file.
You also can edit the mobile_camera library code also and you can give me suggestion on saminshamima@gmail.com."""

setup(
    name="mobile_camera",
    version=VERSION,
    author="Md. Samin Mustakim",
    author_email="saminshamima@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    project_url = "https://github.com/saminmustakim/Mobile-Camera",
    packages=find_packages(),
    install_requires=[],
    keywords=['mobile', 'camera', 'cv', 'python tutorial', 'samin mustakim', 'mobile camera'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)