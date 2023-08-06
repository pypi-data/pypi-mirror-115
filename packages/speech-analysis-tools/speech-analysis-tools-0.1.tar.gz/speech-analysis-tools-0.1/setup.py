import setuptools


with open("README.md", "r", encoding="utf-8") as help_file:
    long_description = help_file.read()

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="speech-analysis-tools",
    version="0.1",
    author="AdityaTB, Zihan Jin",
    author_email="aditya@resemble.ai",
    description="Vocal Fry and other Metrics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/resemble-ai/speech-analysis-tools",
    download_url="https://github.com/resemble-ai/speech-analysis-tools/archive/refs/tags/v0.1.tar.gz",
    keywords = ['Kane Drugman', 'Vocal Fry', 'Creaky Voice', 'Speech Analysis'],
    package_dir={"":"src"},
    project_urls={
        'Bug Reports': 'https://github.com/resemble-ai/speech-analysis-tools/issues',
        'Source': 'https://github.com/resemble-ai/speech-analysis-tools/src/',
    },
    packages=setuptools.find_packages(where="src"),
    install_requires=requirements,
    python_requires=">=3.6",
)