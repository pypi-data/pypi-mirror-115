import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()

setuptools.setup(
    name="ttt_game",
    version="0.1.0",
    author="dm1sh",
    author_email="me@dmitriy.icu",
    description="A simple tic tac toe game implementation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dm1sh/ttt-game",
    project_urls={
        "Bug Tracker": "https://github.com/dm1sh/ttt-game/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
