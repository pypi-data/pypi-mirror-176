import setuptools
from pathlib import Path


this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setuptools.setup(
    name="dbtq",
    version="0.0.1",
    author="Ethan Brown",
    author_email="ethan.w.brown@gmail.com",
    description=("Query compiled dbt models locally"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "pandas",
        "pyyaml",
        "psycopg2[binary]",
        "rich",
        "rich_tools",
        "sqlalchemy",
        "typer[all]",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "dbtq = dbtq.main:app",
        ]
    },
)
