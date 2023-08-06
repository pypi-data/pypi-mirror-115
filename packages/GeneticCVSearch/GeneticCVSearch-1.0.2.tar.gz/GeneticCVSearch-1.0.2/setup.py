#!/usr/bin/env python
# coding: utf-8

# In[1]:


import setuptools

with open('C:/Users/Hindy/Desktop/GeneticCVSearch/README.md', 'r') as fh:
    long_descripion = fh.read()
    
setuptools.setup(
    setup_requires=['wheel'],
    name='GeneticCVSearch', 
    version='1.0.2',
    author='Hindy Yuen', 
    author_email='hindy888@hotmail.com',
    license='MIT',
    description='GeneticCVSearch', 
    long_description=long_descripion, 
    long_description_content_type='text/markdown', 
    url='https://github.com/HindyDS/GeneticCVSearch', 
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
],
    keywords='Genetic CV Hypeparameters Search',
    package_dir={"":"GeneticCVSearch"},
    packages=['GeneticCVSearch'],
    python_requires='>=3.6',
)

