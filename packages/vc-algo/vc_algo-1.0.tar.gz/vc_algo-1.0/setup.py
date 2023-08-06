import setuptools
with open("README.md", "r", encoding = 'utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="vc_algo",
    version="1.0",
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
    license='vcredit-private',
    install_requires=[
        'scikit-learn==0.23.1'
        ,'numpy==1.23.2'
        ,'pandas==11.2.9'
        ,'scipy==1.5.0'
        ,'lightgbm==3.3.2'
        ,'xgboost==1.6.2'
    ],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
)