from setuptools import setup, find_packages

with open('README.md', 'r') as fp:
    long_description = fp.read()

setup(
    name='classicML-lite',
    version='0.7a0',
    description='An easy-to-use ML framework',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Steve R. Sun',
    author_email='s1638650145@gmail.com',
    url='https://github.com/sun1638650145/classicML',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    license='Apache Software License',
    install_requires=[
        'matplotlib==3.3.3',
        'numpy==1.19.4',
        'pandas==1.1.4',
    ],
    python_requires='>=3.8',
)
