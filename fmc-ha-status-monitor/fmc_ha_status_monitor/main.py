import click
import requests

cdfmc_domain = "e276abec-e0f2-11e3-8169-6d9ed49b625f"


@click.command()
@click.argument(
    "env", type=click.Choice(["us", "eu", "aus", "in", "apj"], case_sensitive=False)
)
@click.option("--token", "-t", help="Specify the CDO token", required=True)
def cli(env, token):
    base_url = f"https://edge.{env}.cdo.cisco.com/api/rest/v1/cdfmc"
    get_ha_status(base_url, token)


def get_ha_status(base_url, token):
    url = f"{base_url}/api/fmc_config/v1/domain/{cdfmc_domain}/health/alerts?filter=moduleIds:FTD_HA&expanded=true"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        device_uids_of_ha_pairs_not_in_good_state = [
            item["deviceUUID"] for item in data["items"]
        ]
        ha_pair_uids = get_ha_pair_uids(
            base_url, token, device_uids_of_ha_pairs_not_in_good_state
        )
        get_ha_pair_statuses(base_url, token, ha_pair_uids)
    else:
        print(f"Failed to fetch HA status. HTTP Status Code: {response.status_code}")


import json


def get_ha_pair_statuses(base_url, token, ha_pair_uids):
    url = f"{base_url}/api/fmc_config/v1/domain/{cdfmc_domain}/devicehapairs/ftddevicehapairs"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    ha_pair_statuses = []
    for ha_pair_uid in ha_pair_uids:
        response = requests.get(
            f"{url}/{ha_pair_uid}", headers=headers
        )  # Fixed URL concatenation
        if response.status_code == 200:
            data = response.json()
            ha_pair_status = {
                "name": data["name"],
                "primary": {
                    "status": data["metadata"]["primaryStatus"]["currentStatus"],
                    "deviceUid": data["metadata"]["primaryStatus"]["device"]["id"],
                },
                "secondary": {
                    "status": data["metadata"]["secondaryStatus"]["currentStatus"],
                    "deviceUid": data["metadata"]["secondaryStatus"]["device"]["id"],
                },
                "configStatus": data["metadata"]["configStatus"],
            }
            ha_pair_statuses.append(ha_pair_status)

    # Convert the list of dictionaries to a JSON formatted string and print it
    print(json.dumps(ha_pair_statuses, indent=4))


def get_ha_pair_uids(base_url, token, device_uids):
    url = f"{base_url}/api/fmc_config/v1/domain/{cdfmc_domain}/devices/devicerecords?expanded=true&filter=ids:{','.join(device_uid for device_uid in device_uids)}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        ha_pair_uids = [
            item["metadata"]["containerDetails"]["id"]
            for item in data["items"]
            if "metadata" in item
            and "containerDetails" in item["metadata"]
            and item["metadata"]["containerDetails"]["type"] == "DeviceHAPair"
        ]
        return set(ha_pair_uids)
    else:
        print(f"Failed to fetch HA pair IDs. HTTP Status Code: {response.status_code}")


if __name__ == "__main__":
    cli()
