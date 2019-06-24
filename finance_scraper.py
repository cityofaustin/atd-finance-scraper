"""
Scrape financial codes from COA Controller website and upload to Knack application.
"""
import datautil

from config import CFG
from secrets import *
from utils import *


def main():

    args = cli_args(
        "finance_scraper.py",
        "Scrape financial codes from COA Controller website and upload to Knack application.",
    )

    config = CFG[args.resource]

    scraper = Scraper(config)

    kn = get_knack_data(args.app_name, config)

    new_records = compare(scraper.data, kn.data, config["primary_key"])

    new_records = datautil.replace_keys(new_records, kn.field_map)

    for record in new_records:

        create_record(record, args.app_name, config)

    return len(new_records)


if __name__ == "__main__":

    try:
        results = main()

    except Exception as e:
        raise e
