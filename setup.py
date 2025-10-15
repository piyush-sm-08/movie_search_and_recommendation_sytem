from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="movie_recommender",
    version="0.1",
    author="PIYUSH MADHESHIYA",
    author_email='piyushsmmadheshiya0806@gmail.com',
    description="A simple movie recommendation system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "streamlit",
        "pandas",
        "numpy",
        "scikit-learn",
        "requests" 
    ],
    python_requires=">=3.10",
)



