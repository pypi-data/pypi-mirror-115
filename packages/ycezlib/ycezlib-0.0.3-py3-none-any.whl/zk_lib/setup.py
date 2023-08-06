from distutils.core import setup
#setup(name="zk_lib", version="0.0.1", description="Hello,this is zk's lib for python", author="xcntime", py_modules=['py_lib'])

import setuptools

with open("README.md", "r",encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="ycezlib", # Replace with your own username
    version="0.0.3",
    author="xcntime",
    author_email="xcntime@qq.com",
    description="Hello,this is zk's lib for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/xcntime",
    license="GPLv3",
    packages=setuptools.find_packages(),
    install_requires=[
        "pandas",
        "numpy"
        ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)



