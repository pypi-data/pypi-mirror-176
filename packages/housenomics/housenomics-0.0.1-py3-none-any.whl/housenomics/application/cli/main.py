import logging
import os
from pathlib import Path

import typer
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.sql.expression import Select, SelectOfScalar

from housenomics.determine_seller_total import ServiceDetermineSellerTotal
from housenomics.gateways.gateway_cgd import GatewayCGD
from housenomics.import_transactions import ServiceImportTransactions
from housenomics.list_transactions import ServiceListTransactions
from housenomics.repositories.transactions import Transactions

logging_format: dict = {
    "level": logging.CRITICAL,
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
}

logging.basicConfig(**logging_format)
logger = logging.getLogger(__name__)

app = typer.Typer(add_completion=False)

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore


def create_db_and_tables():
    sqlite_file_name = os.environ["DATABASE"]
    sqlite_url = f"sqlite:///{sqlite_file_name}"

    engine = create_engine(sqlite_url, echo=False)
    SQLModel.metadata.create_all(engine)
    return engine


@app.command(name="import")
def import_(file_path: Path):
    engine = create_db_and_tables()

    with Session(engine) as session:
        try:
            gateway_cgd = GatewayCGD(file_path)
            transactions = Transactions(session)
            ServiceImportTransactions().execute(gateway_cgd, transactions)
            session.commit()
        except Exception as e:  # noqa # nosec
            # Could not complete the operation, are there repeated transactions?
            logger.critical("Error, could not import due to: %s", str(e), exc_info=True)
            typer.Exit(code=1)


@app.command(name="list")
def list_(
    _: str = typer.Argument(
        default="transactions",
        help="The item to be listed",
    ),
):
    engine = create_db_and_tables()
    with Session(engine) as session:
        results = ServiceListTransactions().execute(session)
        for m in results:
            print(f"Description: '{m.description:>22}', Value: {m.value:>10}")


@app.command(name="total")
def total(lookup: str):
    engine = create_db_and_tables()  #
    with Session(engine) as session:
        t = ServiceDetermineSellerTotal().execute(lookup, session)

    print(f"Lookup: '{lookup}', Value: {round(t, 2)}")


@app.command(name="version")
def version():
    typer.echo("0.0.1")


if __name__ == "__main__":
    app()
