from setuptools import setup

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
    url='https://github.com/BrokenShell/MonsterLab',
    author="Robert Sharp",
    author_email="webmaster@sharpdesigndigital.com",
    version="0.0.2",
    description="Monster Generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Free for non-commercial use",
    install_requires=["Fortuna"],
    modules=["MonsterLab.py"],
    classifiers=[
        dev_status["Alpha"],
        "Programming Language :: Python :: 3.9",
    ],
    keywords=[
    ],
    python_requires=">=3.6",
)
