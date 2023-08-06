from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name="bouto",
    version="0.1",
    description="Project creation based on templates.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/Bournix/bouto",
    author="Bournix, Malivix, mmz2000",
    author_email="admin@ghaf.cloud",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["markdown", "wget>=3.2"],
    entry_points={
        "console_scripts": ["bouto=bouto.command_line:main"],
    },
    packages=["bouto"],
    zip_safe=False,
)
