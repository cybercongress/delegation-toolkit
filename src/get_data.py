import requests
import pandas as pd
from tqdm import tqdm

from cyberpy._wallet import address_to_address
from config import LCD_API, JAILED_WINDOW


def get_validators() -> pd.DataFrame:
    """
    Gets info about validators if validator isn't jailed
    as like moniker, operator address, staking tokens,
    delegator shares, commission rate, self staked tokens,
    power, number of jails for the last 100,000 blocks,
    number of jails for all time, isjailed state.

    :return validators:
    """
    url = LCD_API + '/cosmos/staking/v1beta1/validators?pagination.limit=1000'
    res = requests.get(url).json()['validators']
    height_url = LCD_API + '/cosmos/base/tendermint/v1beta1/blocks/latest'
    min_height = int(requests.get(height_url).json()['block']['header']['height']) - JAILED_WINDOW
    result = [
        (
            validator['description']['moniker'],
            validator['operator_address'],
            int(validator['tokens']),
            float(validator['delegator_shares']),
            float(validator['commission']['commission_rates']['rate']),
            get_self_delegation(validator['operator_address'], int(validator['tokens'])),
            get_power(validator['operator_address']),
            get_jailed_times(validator['operator_address'], min_height),
            get_jailed_times(validator['operator_address'], 2),
            validator['jailed']
        ) for validator in tqdm(res) if validator['jailed'] == False]
    return pd.DataFrame(result, columns=[
        'moniker',
        'operator_address',
        'staked',
        'delegator_shares',
        'greed',
        'ownership',
        'power',
        'jailed_times_100_000',
        'jailed_times_all',
        'isjailed',
    ])


def get_self_delegation(
        validator_address: str,
        tokens: int) -> float:
    """
    Returns self delegation share by a given validator address.
    Returns 0 in case of key error exception

    :param validator_address:
    :param tokens:
    :return delegation_share:
    """
    delegator_address = address_to_address(validator_address, 'bostrom')
    url = LCD_API + f'/cosmos/staking/v1beta1/validators/{validator_address}/delegations/{delegator_address}'
    try:
        delegated = int(requests.get(url).json()['delegation_response']['balance']['amount'])
        delegation_share = delegated / tokens
    except KeyError as e:
        print(e, url)
        delegation_share = 0
    return delegation_share


def get_jailed_times(
        address: str,
        min_height: int = 2) -> int:
    """
    Returns a number of jails for range (min_height, now)

    :param address:
    :param min_height:
    :return jailed_times:
    """
    url = LCD_API + \
          f'/txs?message.action=%2Fcosmos.slashing.v1beta1.MsgUnjail' \
          f'&message.sender={address}&limit=1000&tx.minheight={min_height}'
    res = requests.get(url).json()
    if 'txs' in res.keys():
        return len(res['txs'])
    else:
        return 0


def get_power(validator_address: str) -> float:
    """
    Returns a validator's power by a given address
    as multiplication of validator's ampere and volt balances

    :param validator_address:
    :return power:
    """
    address = address_to_address(validator_address, 'bostrom')
    url = LCD_API + f"/cosmos/bank/v1beta1/balances/{address}"
    try:
        balances = requests.get(url).json()['balances']
    except KeyError as e:
        print(e, url)
        balances = []
    milliampere = list(filter(lambda balance: balance['denom'] == 'milliampere', balances))
    millivolt = list(filter(lambda balance: balance['denom'] == 'millivolt', balances))
    if milliampere == [] or millivolt == []:
        power = 0
    else:
        milliampere = int(milliampere[0]['amount']) / 1000
        millivolt = int(millivolt[0]['amount']) / 1000
        power = milliampere * millivolt
    return power


def get_delegations(delegator_address: str) -> pd.DataFrame:
    """
    Returns dataframe with delegations by a give delegator address

    :param delegator_address:
    :return delegations:
    """
    delegations_raw = \
        requests.get(LCD_API + f'/cosmos/staking/v1beta1/delegations/{delegator_address}?pagination.limit=1000').json()
    delegations_raw = delegations_raw['delegation_responses']
    delegations = [(d['delegation']['validator_address'], int(d['balance']['amount'])) for d in delegations_raw]
    return pd.DataFrame(delegations, columns=['operator_address', 'delegation'])
