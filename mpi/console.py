import click
from prettytable import PrettyTable
import bootstrap
import auction

@click.group()
def main():
    pass

@main.command()
@click.option('--email', default=None)
@click.option('--minimum-year', default=None)
@click.option('--model', default=None)
def subscribe(email, minimum_year, model):
    if not email:
        raise Exception("Subscription requires --email=<addr>")

    search = {
        'year': {},
        'model': {}
    }

    if minimum_year:
        search['year']['minimum'] = minimum_year

    if model:
        search['model'] = model

    bootstrap.auctions.subscribe(auction.Subscription(
        email,
        search
    ))

@main.command()
def subscriptions():
    subscriptions = bootstrap.auctions.subscriptions()

    table = PrettyTable(['Subscription ID', 'Email', 'Search'])

    for subscription in subscriptions:
        table.add_row([
            subscription.subscriptionId,
            subscription.email,
            subscription.search
        ])

    print(table)

if __name__ == "__main__":
    main()

