from setuptools import setup

setup(
    name="vbauto",
    version="0.2.0",
    packages=["vbauto"],
    python_requires=">=3.6",
    entry_points={"console_scripts": ["vbauto = vbauto.__main__:app"]},
)
