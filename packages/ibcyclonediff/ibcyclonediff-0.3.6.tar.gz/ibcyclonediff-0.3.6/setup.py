from setuptools import find_packages, setup

from ibcyclonediff.version import VERSION

with open("README.md", encoding="utf-8") as f:
    readme = f.read()

# with open("requirements.txt", encoding="utf-8") as f:
#     requirements = f.read().split("\n")

setup_kwargs = dict(
    name='ibcyclonediff',
    version=VERSION,
    description='Software Bill of Material (SBOM) difference tool',
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/threehook/ibcyclonediff",
    author='Ton van de Ven',
    author_email='threehook@hotmail.com',
    maintainer='Ton van de Ven',
    maintainer_email='threehook@hotmail.com',
    license='Apache_2.0',
    keywords=["security", "tools", "SBOM", "DevSecOps", "SPDX", "CycloneDX"],
    # install_requires=requirements,
    install_requires=[
        'defusedxml',
        'pyyaml>=5.4'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    python_requires=">=3.7",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "sbomdiff = sbomdiff.cli:main",
        ],
    },
)

setup(**setup_kwargs)
