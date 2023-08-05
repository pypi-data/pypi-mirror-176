import asyncio
from typing import Literal
from urllib import parse

import httpx
import numpy as np
import pandas as pd
from authlib.integrations.httpx_client import AsyncOAuth2Client, OAuth2Client


class SciNoteClient(object):
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        server_url: str,
        token_saver: callable,
        code: str = None,
        refresh_token: str = None,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.server_url = server_url
        self.token_saver = token_saver
        self.code = code
        self.refresh_token = refresh_token
        self.access_token = None
        self.token = None

        self.LIST_TYPES = ("list", "status", "checklist", "stock_unit")

        self.initialize()

    def initialize(self):
        if self.token is None:
            if self.refresh_token:
                self.refresh_access_token()
            elif self.code:
                self.fetch_access_token()
            else:
                raise Exception("No code or refresh token provided")

    def fetch_access_token(self):
        """Fetch access token from SciNote server."""
        client = OAuth2Client(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
        )
        token = client.fetch_token(
            url=self.server_url + "/oauth/token",
            grant_type="authorization_code",
            code=self.code,
        )
        self.update_token(token)

    def refresh_access_token(self):
        """Refresh access token from SciNote server."""
        client = OAuth2Client(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
        )
        token = client.refresh_token(
            url=self.server_url + "/oauth/token",
            refresh_token=self.refresh_token,
        )
        self.update_token(token)

    def update_token(self, token):
        """Update token and save it."""
        self.access_token = token["access_token"]
        self.refresh_token = token["refresh_token"]
        self.token = token
        self.token_saver(token)

    def sync_request(self, method, url, json=None):
        """Make a synchronous request to SciNote server."""
        with OAuth2Client(
            client_id=self.client_id,
            client_secret=self.client_secret,
            token=self.token,
            update_token=self.update_token,
        ) as client:
            return client.request(method, url, json=json)

    def get(self, url):
        """Make a synchronous GET request to SciNote server."""
        return self.sync_request("GET", url)

    def post(self, url, data):
        """Make a synchronous POST request to SciNote server."""
        return self.sync_request("POST", url, json=data)

    async def async_request(self, method, urls):
        """Make an asynchronous request to SciNote server."""
        client = AsyncOAuth2Client(
            client_id=self.client_id,
            client_secret=self.client_secret,
            token=self.token,
            update_token=self.update_token,
            timeout=httpx.Timeout(60.0, connect=10.0),
        )
        tasks = [client.request(method, url) for url in urls]
        result = await asyncio.gather(*tasks)
        await client.aclose()

        return result

    async def async_get(self, urls: list):
        """Make an asynchronous GET request to SciNote server."""
        return await self.async_request("GET", urls)

    def build_url_list(self, url):
        """Build a list of URLs for asynchronous requests."""
        r = self.get(url)
        r_json = r.json()
        self_page = r_json["links"]["self"]
        last_page = int(
            parse.parse_qs(parse.urlparse(r_json["links"]["last"]).query)[
                "page[number]"
            ][0]
        )
        url_list = [
            self_page.replace("page%5Bnumber%5D=1", f"page%5Bnumber%5D={i}")
            for i in range(1, last_page + 1)
        ]

        return url_list

    def get_teams(self, without_emoji=False):
        """Get all teams."""
        url = self.server_url + "/api/v1/teams"
        r = self.get(url)
        r_json = r.json()

        while r_json["links"]["next"]:
            r = self.get(r_json["links"]["next"])
            r_json.extend(r.json())

        teams_dict = {
            team["attributes"]["name"].replace("🟢 ", "")
            if without_emoji
            else team["attributes"]["name"]: team["id"]
            for team in r_json["data"]
            if "🟢" in team["attributes"]["name"]
        }

        return teams_dict

    def get_inventories(self, team_id):
        """Get all inventories for a team."""
        url = self.server_url + f"/api/v1/teams/{team_id}/inventories"
        r = self.get(url)
        r_json = r.json()

        while r_json["links"]["next"]:
            r = self.get(r_json["links"]["next"])
            r_json.extend(r.json())

        inventories_dict = {
            inventory["attributes"]["name"]: inventory["id"]
            for inventory in r_json["data"]
        }

        return inventories_dict

    def get_inventory_columns(self, team_id, inventory_id):
        """Get all columns for an inventory."""
        url = (
            self.server_url
            + f"/api/v1/teams/{team_id}/inventories/{inventory_id}/columns"
        )
        r = self.get(url)
        r_json = r.json()

        columns_dict = {
            column["attributes"]["name"]: {
                "id": column["id"],
                "type": column["attributes"]["data_type"],
            }
            for column in r_json["data"]
        }

        while r_json["links"]["next"]:
            r = self.get(r_json["links"]["next"])
            r_json = r.json()
            columns_dict.update(
                {
                    column["attributes"]["name"]: {
                        "id": column["id"],
                        "type": column["attributes"]["data_type"],
                    }
                    for column in r_json["data"]
                }
            )

        return columns_dict

    def get_inventory_column_items(
        self,
        team_id,
        inventory_id,
        column_id,
        type: Literal["list", "status", "checklist", "stock_unit"],
    ):
        """Get all list items for a column."""
        url = (
            self.server_url
            + f"/api/v1/teams/{team_id}/inventories/{inventory_id}/columns/{column_id}/{type}_items"
        )
        r = self.get(url)
        r_json = r.json()

        while r_json["links"]["next"]:
            r = self.get(r_json["links"]["next"])
            r_json.extend(r.json())

        options_dict = {
            option["attributes"]["data"]: option["id"] for option in r_json["data"]
        }

        return options_dict

    def get_inventory_items(self, team_id, inventory_id):
        """Get all items for an inventory."""
        urls = self.build_url_list(
            self.server_url
            + f"/api/v1/teams/{team_id}/inventories/{inventory_id}/items?include=inventory_cells"
        )
        r = asyncio.run(self.async_get(urls))
        r_json = [i.json() for i in r]

        data_df = pd.json_normalize(r_json[0]["data"])
        included_df = pd.json_normalize(r_json[0]["included"])

        for i in r_json[1:]:
            data_df = pd.concat(
                [data_df, pd.json_normalize(i["data"])], ignore_index=True
            )
            included_df = pd.concat(
                [included_df, pd.json_normalize(i["included"])], ignore_index=True
            )

        data_df = data_df[
            ["id", "attributes.name", "relationships.inventory_cells.data"]
        ]
        data_df = data_df.rename(columns={"attributes.name": "Name"})

        included_df = included_df.set_index("id")

        columns_dict = self.get_inventory_columns(team_id, inventory_id)
        stock_dict = {}

        for name, attributes in columns_dict.items():
            data_df[name] = np.nan

            if attributes["type"] == "stock":
                stock_dict[name + " Units"] = {
                    "id": attributes["id"] + " Units",
                    "type": "stock_units",
                }
                stock_dict[name + " Threshold"] = {
                    "id": attributes["id"] + " Threshold",
                    "type": "stock_threshold",
                }

                stock_items_dict = self.get_inventory_column_items(
                    team_id, inventory_id, attributes["id"], "stock_unit"
                )
                stock_items_dict = {v: k for k, v in stock_items_dict.items()}

        columns_dict.update(stock_dict)
        ids_columns = {value["id"]: key for key, value in columns_dict.items()}

        def get_relationships(row):
            ids = [str(d["id"]) for d in row["relationships.inventory_cells.data"]]
            for id in ids:
                column = str(included_df.loc[id, "attributes.column_id"])

                if included_df.loc[id, "attributes.value_type"] == "text":
                    row[ids_columns[column]] = included_df.loc[
                        id, "attributes.value.text"
                    ]
                elif included_df.loc[id, "attributes.value_type"] == "number":
                    row[ids_columns[column]] = included_df.loc[
                        id, "attributes.value.data"
                    ]
                elif included_df.loc[id, "attributes.value_type"] == "date":
                    row[ids_columns[column]] = included_df.loc[
                        id, "attributes.value.date"
                    ]
                elif included_df.loc[id, "attributes.value_type"] == "list":
                    row[ids_columns[column]] = included_df.loc[
                        id, "attributes.value.inventory_list_item_name"
                    ]
                elif included_df.loc[id, "attributes.value_type"] == "status":
                    row[ids_columns[column]] = included_df.loc[
                        id, "attributes.value.inventory_status_item_name"
                    ]
                elif included_df.loc[id, "attributes.value_type"] == "checklist":
                    row[ids_columns[column]] = included_df.loc[
                        id, "attributes.value.inventory_checklist_item_names"
                    ]
                elif included_df.loc[id, "attributes.value_type"] == "stock":
                    row[ids_columns[column]] = included_df.loc[
                        id, "attributes.value.amount"
                    ]
                    row[ids_columns[column + " Units"]] = stock_items_dict[
                        str(
                            int(
                                included_df.loc[
                                    id, "attributes.value.repository_stock_unit_item_id"
                                ]
                            )
                        )
                    ]
                    row[ids_columns[column + " Threshold"]] = included_df.loc[
                        id, "attributes.value.low_stock_threshold"
                    ]
                else:
                    print(
                        f"Unknown value type: {included_df.loc[id, 'attributes.value_type']}"
                    )

            return row

        df = data_df.apply(get_relationships, axis=1)
        df = df.drop(columns=["relationships.inventory_cells.data"])
        df = df.set_index("id", drop=True)

        return df

    def get_next_oligo(self, team_id, inventory_id):
        """Get the next available oligo from an inventory."""
        url = (
            self.server_url
            + f"/api/v1/teams/{team_id}/inventories/{inventory_id}/items"
        )
        r = self.get(url)
        r_json = r.json()

        last_page_link = r_json["links"]["last"]
        r = self.get(last_page_link)
        r_json = r.json()

        oligos = [item["attributes"]["name"] for item in r_json["data"]]

        second_to_last_page_link = r_json["links"]["prev"]
        r = self.get(second_to_last_page_link)
        r_json = r.json()

        oligos += [item["attributes"]["name"] for item in r_json["data"]]
        oligos = [int(oligo.replace("oACD", "")) for oligo in oligos]

        return max(oligos) + 1

    def create_inventory_item(self, team_id, inventory_id, data):
        """Create an inventory item."""
        url = (
            self.server_url
            + f"/api/v1/teams/{team_id}/inventories/{inventory_id}/items"
        )
        r = self.post(url, data)
        r_json = r.json()

        return r_json

    def submit_inventory_df(self, team_id, inventory_id, df):
        """Submit a dataframe to create inventory items from all rows."""
        df = df.rename(columns={"Sample Name": "Name"})

        columns_dict = self.get_inventory_columns(team_id, inventory_id)

        for _, row in df.iterrows():
            included_list = []
            for key, value in columns_dict.items():
                if key in row.index and row[key] != "None" and row[key] != "":
                    if value["type"] in self.LIST_TYPES:
                        list_item_dict = self.get_inventory_column_items(
                            team_id, inventory_id, value["id"], value["type"]
                        )
                        included_list.append(
                            {
                                "type": "inventory_cells",
                                "attributes": {
                                    "value": int(list_item_dict[row[key]]),
                                    "column_id": int(value["id"]),
                                },
                            }
                        )
                    else:

                        included_list.append(
                            {
                                "type": "inventory_cells",
                                "attributes": {
                                    "value": row[key],
                                    "column_id": int(value["id"]),
                                },
                            }
                        )
            data = {
                "data": {
                    "type": "inventory_items",
                    "attributes": {"name": row["Name"]},
                },
                "included": included_list,
            }

            self.create_inventory_item(team_id, inventory_id, data)

        return True

    def get_project_folders(self, team_id):
        """Get all project folders."""
        url = self.server_url + f"/api/v1/teams/{team_id}/project_folders"
        r = self.get(url)
        r_json = r.json()

        while r_json["links"]["next"]:
            r = self.get(r_json["links"]["next"])
            r_json.extend(r.json())

        folders_dict = {
            folder["attributes"]["name"]: folder["id"] for folder in r_json["data"]
        }

        return folders_dict

    def create_project_folder(self, team_id, parent_folder_id, name):
        """Create a project folder."""
        url = self.server_url + f"/api/v1/teams/{team_id}/project_folders"
        data = {
            "data": {
                "type": "project_folders",
                "attributes": {"name": name, "parent_folder_id": parent_folder_id},
            }
        }
        r = self.post(url, data)

        return r.json()
