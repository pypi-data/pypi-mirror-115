from setuptools import setup
from setuptools import find_namespace_packages

#Load the README file. 
#with open(file = "README.md", mode="r") as readme_handle:
#    long_description = readme_handle.read()

setup(
    #Define the library name, this is what is use with pip install
    name = 'corpit.sharedmailboxconvert',

    author = 'Thaddius Cho',

    author_email = 'mcho@assurance.com',

    #Define the version of this library
    #Read as 
        #Major Version
        #Minor Version
        #Maintenance Version

    version = '0.1.0',  

    descriptions = 'python client used to leverage api calls to read Jira issues',

    #long_description = long_description,

    install_requires = [
        "requests==2.24.0",
        "pandas==1.1.3"    
    ], 

    keywords = 'corpit, Jira, user_management', 


    packages = find_namespace_packages(
        include= ['shared_mailbox_converter', 'shared_mailbox_converter/output/']
    ),

    #package_data = {
     #   "output" : []
    #},

    include_package_data=True,

    python_requires='>=3.8',

    #classifiers =




)


