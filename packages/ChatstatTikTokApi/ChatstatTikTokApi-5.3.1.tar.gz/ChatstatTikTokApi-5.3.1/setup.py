from distutils.core import setup
import os.path
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ChatstatTikTokApi",
    packages=setuptools.find_packages(),
    version="5.3.1",
    license="MIT",
    description="The Unofficial TikTok API Wrapper in Python 3 for our own Chatstat.",
    author="J Teng",
    author_email="j.teng@chatstat.com",
    url="https://github.com/j-teng96/TikTok-Api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    download_url="https://github.com/j-teng96/TikTok-Api/tree/master",
    keywords=["tiktok", "python3", "api", "unofficial", "tiktok-api", "tiktok api"],
    install_requires=["requests", "playwright"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
