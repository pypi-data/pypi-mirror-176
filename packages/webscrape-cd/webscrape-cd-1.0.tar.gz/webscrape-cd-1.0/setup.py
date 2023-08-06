import setuptools
  
with open("README.md", "r") as fh:
    description = fh.read()
  
setuptools.setup(
    name="webscrape-cd",
    version="1.0",
    author="Ayush Mudunuru",
    author_email="ayush.mudunuru@gmail.com",
    packages=["cdpackage"],
    description="FOSS Contact detail extractor ",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/CrownCrafter/webscrapecd",
    license='MIT',
    python_requires='>=3.10',
    install_requires=['googlesearch', 'urllib.request', 'bs4','requests', 'csv', 're']
)