from distutils.core import setup

setup(
    name="meteonetwork-api-client-python",
    version="0.1.0",
    description="Simple python client for meteonetwork api",
    author="Denny Baldini",
    author_email="dennybaldini@gmail.com",
    url="https://github.com/dennyb87/meteonetwork-api-client-python",
    install_requires=[
        "requests==2.31.0",
    ],
    packages=["meteonetwork_api"],
    package_dir={"": "src"},
)
