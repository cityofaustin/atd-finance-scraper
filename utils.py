import argparse
import csv
import os

from bs4 import BeautifulSoup
import knackpy
import requests

from secrets import *


class Scraper:
    # Helper class for parsing page-specific table data
    def __init__(self, config):
        self.config = config

        self.html = self.get_html(config["form_data"])
        self.rows = self.handle_html()
        self.data = self.handle_rows()

    def get_html(self, form_data):
        res = requests.post(self.config["url"], form_data)
        res.raise_for_status()
        return res.text

    def handle_html(self):
        soup = BeautifulSoup(self.html, "html.parser")
        rows = soup.find_all("tr")

        # truncate misc unwanted table data
        if self.config["name"] == "master_agreements":
            rows = rows[10:]

        elif self.config["name"] == "objects":
            rows = rows[6:-1]

        elif self.config["name"] == "units":
            rows = rows[6:-1]

        else:
            raise Exception("This case should never happen due to cli_arg definitions.")

        parsed = []

        for row in rows:
            cols = row.find_all("td")
            cols = [ele.text.strip() for ele in cols]
            parsed.append(cols)

        return parsed

    def handle_rows(self):
        fieldnames = self.config.get("fieldnames")
        return [dict(zip(fieldnames, row)) for row in self.rows]


def cli_args(prog, description):

    parser = argparse.ArgumentParser(prog=prog, description=description)

    parser.add_argument(
        dest="resource",
        action="store",
        choices=["master_agreements", "objects", "units"],
        type=str,
        help="The name of the resource to be scraped.",
    )

    parser.add_argument(
        dest="app_name",
        action="store",
        type=str,
        help="Name of the knack application that will be accessed",
    )

    args = parser.parse_args()
    return args


def get_knack_data(app_name, config):
    return knackpy.Knack(
        scene=config["scene"],
        view=config["view"],
        ref_obj=config["ref_obj"],
        app_id=KNACK_CREDENTIALS[app_name]["app_id"],
        api_key=KNACK_CREDENTIALS[app_name]["api_key"],
    )


def compare(new_rows, existing_rows, key):
    existing_ids = [str(row[key]) for row in existing_rows]
    return [row for row in new_rows if str(row[key]) not in existing_ids]


def create_record(record, app_name, config):

    return knackpy.record(
        record,
        obj_key=config["ref_obj"][0],
        app_id=KNACK_CREDENTIALS[app_name]["app_id"],
        api_key=KNACK_CREDENTIALS[app_name]["api_key"],
        method="create",
    )
