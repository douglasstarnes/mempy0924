from collections import Counter

import click
import requests
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    func,
    select,
    distinct,
)
from sqlalchemy.orm import declarative_base, sessionmaker

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"

console = Console()

Base = declarative_base()


class Investment(Base):
    __tablename__ = "investments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    coin = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)
    buy_sell = Column(Boolean, default=True, nullable=False)
    timestamp = Column(DateTime, default=func.now(), nullable=False)


engine = create_engine("sqlite:///portfolio.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def get_coin_values(coins, currency="usd"):
    if not isinstance(coins, list):
        ids = [coins]
    else:
        ids = ",".join(coins)
    response = requests.get(
        COINGECKO_URL,
        params={
            "ids": ids,
            "vs_currencies": currency,
        },
    )

    return response.json(), currency


@click.group()
def cli():
    pass


@click.command()
@click.argument("coin")
@click.option("--currency", default="usd")
def lookup_coin(coin, currency):
    coin_values, currency = get_coin_values(coin, currency)

    message = Text(f"{coin_values[coin][currency]} {currency}", style="bold blue")
    title = Text(f"The current value of {coin}", style="bold blue")
    panel = Panel(
        message,
        title=title,
        border_style="green",
    )

    console.print(panel)


@click.command()
@click.argument("coin")
@click.argument("quantity", type=float)
def buy_coin(coin, quantity):
    new_investment = Investment(coin=coin, quantity=quantity)
    session.add(new_investment)
    session.commit()

    console.print(f"[bold green]Bought {quantity} {coin}[/bold green]")


@click.command()
@click.argument("coin")
@click.argument("quantity", type=float)
def sell_coin(coin, quantity):
    new_investment = Investment(coin=coin, quantity=quantity, buy_sell=False)
    session.add(new_investment)
    session.commit()

    console.print(f"[bold red]Sold {quantity} {coin}[/bold red]")


@click.command()
@click.option("--summarize/--no-summarize", default=False)
@click.option("--currency", default="usd")
def list_portfolio(summarize, currency):
    table = Table(title="Investments")
    table.add_column("Coin")
    table.add_column("Quantity")
    table.add_column("Buy")
    table.add_column("Timestamp")
    stmt = select(Investment).order_by(Investment.timestamp)
    investments = session.execute(stmt).all()
    if summarize == True:
        stmt = select(distinct(Investment.coin))
        coins = [row[0] for row in session.execute(stmt).all()]
        coin_values, _ = get_coin_values(coins, currency)
        totals = Counter()
    for row in investments:
        if row[0].buy_sell == True:
            text = Text("Yes", style="bold green")
            if summarize == True:
                totals[row[0].coin] += row[0].quantity
        else:
            text = Text("No", style="bold red")
            if summarize == True:
                totals[row[0].coin] -= row[0].quantity
        table.add_row(
            row[0].coin,
            str(row[0].quantity),
            text,
            row[0].timestamp.strftime("%B %d, %Y %H:%M:%S %p"),
        )

    console.print(table)

    if summarize == True:
        summary_table = Table(title="Portfolio Summary")

        summary_table.add_column("Coin")
        summary_table.add_column("Total Quantity")
        summary_table.add_column("Total Value")

        for coin, total in totals.items():
            summary_table.add_row(
                coin, str(total), f"{total * coin_values[coin][currency]} {currency}"
            )

        console.print(summary_table)

        total_value = sum(
            [total * coin_values[coin][currency] for coin, total in totals.items()]
        )
        total_panel = Panel(
            Text(f"{total_value} {currency}"),
            title=f"Portfolio Value",
        )

        console.print(total_panel)


cli.add_command(lookup_coin)
cli.add_command(buy_coin)
cli.add_command(sell_coin)
cli.add_command(list_portfolio)

if __name__ == "__main__":
    cli()
