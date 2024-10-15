from setuptools import setup, find_packages

setup(
    name='Steganography',
    version='0.1',                  # First version, just trying out this functionality
    packages=find_packages(),    
    install_requires=[
        'Imageio==2.35.1',          # The library used to read and manipulate PNG files
        'cryptography',             # Cryptography functionality
        'Pillow',                   # Other image file manipulation functionalities
        'mpmath',                   # High precision math operation
        ],
)
