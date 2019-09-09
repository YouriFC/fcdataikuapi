import setuptools

setuptools.setup(name='fcdataikuapi',
    version='0.1', 
    packages=setuptools.find_packages(),
    description='FrieslandCampina-specific dataiku management API',
    url='https://github.com/YouriFC/fcdataikuapi',
    author="Youri Immerzeel",
    author_email='youri.immerzeel@frieslandcampina.com', 
    install_requires=['dataiku'])