import yaml
import pandas as pd
import sqlalchemy as sa
import typer
from os.path import expanduser
from rich import box
from rich.console import Console
from rich_tools import df_to_table
from sqlalchemy.engine.url import URL
from sqlalchemy.sql import text


app = typer.Typer()
console = Console()


def pretty_print_dataframe(df: pd.DataFrame):
    table = df_to_table(df)
    table.highlight = True
    table.row_styles = ["none", "dim"]
    table.box = box.SIMPLE_HEAD
    for column in table.columns:
        column.overflow = "fold"
    console.print(table)


@app.command()
def query(
    sql: str,
    profile: str = None,
    output_path: str = "result.csv",
    driver: str = "postgresql+psycopg2",
):
    # get dbt profile info
    home = expanduser("~")
    with open(f"{home}/.dbt/profiles.yml", "r") as f:
        profile_yaml = yaml.safe_load(f)
    profiles = list(profile_yaml.keys())
    db_config = profile_yaml[profile or profiles[0]]
    target = db_config["target"]
    cfg = db_config["outputs"][target]

    # read sql file
    with open(sql, "r") as f:
        q = f.read()

    # build the sqlalchemy URL
    url = URL.create(
        drivername=driver,
        host=cfg["host"],
        port=cfg["port"],
        database=cfg["dbname"],
        username=cfg["user"],
        password=cfg["password"],
    )

    # query db
    console.print("executing query...")
    engine = sa.create_engine(url)
    with engine.connect() as conn:
        df = pd.io.sql.read_sql(text(q), conn)
    console.print("done.")

    # record result
    console.print(f"recording to `{output_path}`...")
    df.to_csv(output_path)
    console.print("done.")

    # print result
    pretty_print_dataframe(df.head())


@app.command()
def csv(path: str, n_rows: int = None):
    df = pd.read_csv(path, index_col=0, nrows=n_rows)
    pretty_print_dataframe(df)


if __name__ == "__main__":
    app()
