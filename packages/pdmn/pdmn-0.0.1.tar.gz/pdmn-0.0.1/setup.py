import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pdmn",
    version="0.0.1",
    author="Simon Vandevelde",
    author_email="s.vandevelde@kuleuven.be",
    description="A package providing a pDMN solver",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=['openpyxl==3.0.0', 'ply==3.11',
                      'numpy', 'python-dateutil',
                      'problog'],
    entry_points={
        'console_scripts': ['pdmn=pdmn.pdmn:main']
    }
)
