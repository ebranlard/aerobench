from setuptools import setup, find_packages

VERSION='1.0.0'
setup(
    name='aerobench',
    version=VERSION,
    long_description="""""",
    long_description_content_type = 'text/markdown',
    author='',
    author_email='',
    url='http://github.com/ebranlard/aerobench/',
    license='MIT',
    python_requires=">=3.6",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        'matplotlib', 
        'numpy',
        'pandas', 
    ],
    include_package_date = True,
)
