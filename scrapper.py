from datetime import datetime, timezone

import requests

from model import GroupData

ResponseData = dict


def right_now():
    return datetime.utcnow().replace(microsecond=0, tzinfo=timezone.utc)


async def fetch_groups(url) -> ResponseData:
    now = right_now()
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


async def collect(url) -> list[GroupData]:
    now = right_now()
    groups = await fetch_groups(url)
    return [
        GroupData(
            dt=now,
            group=g['serviceGroup'],
            people=g['peopleCount'],
        )
        for g in groups
    ]


async def collect_task() -> list[GroupData]:
    host = 'https://api.osir-zoliborz.waw.pl:8443'
    path = 'BxNetRest/rest/people/license/amount'
    url = f'{host}/{path}'
    return await collect(url)
