from setuptools import setup, find_packages

with open("README.md", "r") as file:
    long_description = file.read()

dev_status = {
    "Alpha": "Development Status :: 3 - Alpha",
    "Beta": "Development Status :: 4 - Beta",
    "Pro": "Development Status :: 5 - Production/Stable",
    "Mature": "Development Status :: 6 - Mature",
}

setup(
    name="MonsterLab",
    url='https://github.com/BrokenShell/Fortuna',
    author="Robert Sharp",
    author_email="webmaster@sharpdesigndigital.com",
    version="0.0.5",
    description="Monster Generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Free for non-commercial use",
    install_requires=["Fortuna"],
    packages=find_packages(),
    classifiers=[
        dev_status["Pro"],
        "Programming Language :: Python :: 3.7",
    ],
    keywords=[
        "MonsterLab", "Fortuna"
    ],
    python_requires=">=3.7",
)
