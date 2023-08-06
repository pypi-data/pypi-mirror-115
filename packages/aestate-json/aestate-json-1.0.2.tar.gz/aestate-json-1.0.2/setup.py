import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aestate-json",
    version="1.0.2",
    author="CACode",
    author_email="cacode@163.com",
    description="Aestate Framework for Python,You can see:https://gitee.com/canotf/aestate",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/canotf/aestate-json",
    project_urls={
        "Bug Tracker": "https://gitee.com/canotf/aestate-json/issues",
    },
    license=' Apache License 2.0',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
