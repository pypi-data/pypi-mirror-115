import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'A basic Panda package'

setuptools.setup(
     name='PandaTTex',  
     version=VERSION,
     scripts=['PandaTTex'] ,
     author="Marcelo Kenji Noda",
     author_email="nodamarcelokenjinoda@gmail.com",
     description= DESCRIPTION,
     long_description=long_description,
    long_description_content_type="text/markdown",
     url="https://github.com/javatechy/dokr",
     packages=setuptools.find_packages(),
     install_requires=['pandas'],
     keyword=['latex','pandas','python','texts'],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )