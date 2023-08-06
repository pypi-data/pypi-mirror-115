import setuptools

setuptools.setup(
    name="paravastu", # Replace with your own username
    version="0.9.9.1",
    author="Paravastu Lab",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=[
        'numpy',
        'pandas',
        'biopandas',
        'dtale',
	    'plotnine'
    ]
)
