import setuptools
with open("README.md", "r", encoding = 'utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="vc_algo",
    version="1.1",
    author="Frank",
    author_email="frank@vc.com",
    description="维C算法工具包",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(where='.'
                                      ,exclude=()
                                      ,include=('*')
                                      ),
    license='vc-private',
    install_requires=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
)