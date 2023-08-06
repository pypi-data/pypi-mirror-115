import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pydosLinux",
    version="0.2.8066",
    author="yijiafeiji",
    author_email="jjy1207826398@163.com",
    description="py-dos is a toolset.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/yizhigezi_yijiafeiji/py-dos",
    project_urls={
        "Bug Tracker": "https://gitee.com/yizhigezi_yijiafeiji/py-dos/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)