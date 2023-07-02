from datetime import datetime, timezone

import requests

from model import RawGroupsData, GroupData


def fetch_groups(url) -> dict:
    now = datetime.utcnow().replace(tzinfo=timezone.utc)
    response = requests.get(url)
    print(f'[ {now} ] {response.status_code}')

    if response.status_code != 200:
        print(response.status_code)
        print(response.headers)
        print(response.text)
        raise ValueError(f'Response code: {response.status_code}')

    json_data = response.json()
    try:
        validate(json_data)
    except AssertionError as e:
        print(json_data)
        raise e
    groups = json_data[0].get('serviceGroups')
    return groups


def validate(json_data) -> None:
    """Expects a 1-element list. The sole element should contain serviceGroups"""
    assert type(json_data) == list
    assert len(json_data) == 1
    groups = json_data[0].get('serviceGroups')
    assert groups is not None
    for g in groups:
        assert g.get('serviceGroup') is not None
        assert g.get('peopleCount') is not None


def collect(url) -> list[GroupData]:
    now = datetime.utcnow().replace(tzinfo=timezone.utc)
    timestamp = int(now.timestamp())
    groups = fetch_groups(url)
    return [
        GroupData(
            time=timestamp,
            group=g['serviceGroup'],
            people=g['peopleCount'],
        )
        for g in groups
    ]


async def collect_task() -> list[GroupData]:
    host = 'https://api.osir-zoliborz.waw.pl:8443'
    path = 'BxNetRest/rest/people/license/amount'
    url = f'{host}/{path}'
    return collect(url)


# TODO: append entry to a file or a database whatever
#       just make it stay on disk and make it expandable 
# (adding new rows should be easy)