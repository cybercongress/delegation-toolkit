import base64
import bech32
import pandas as pd

from config import REDELEGATION_NUMBER


def b64_to_cons(cons: str) -> str:
    """
    Converts hex representation of validator's node consensus public key
    to human-readable bech32 with bostromvalconspub prefix

    :param cons:
    :return bostromvalconspub_address:
    """
    cons = bytes(cons, 'utf-8')
    cons = base64.b64decode(cons)
    five_bit_r = bech32.convertbits(cons, 8, 5)
    return bech32.bech32_encode('bostromvalconspub', five_bit_r)


def clean_up_validators_set(
        validators_df: pd.DataFrame,
        number_of_jails_for_kick_off: int,
        black_list: list) -> pd.DataFrame:
    """
    Drops validators with a number of jails > number_of_jails_for_kick_off.
    Drops validators from the black_list.
    Resets index.

    :param validators_df:
    :param number_of_jails_for_kick_off:
    :param black_list:
    :return:
    """
    validators_df = validators_df.drop(validators_df[validators_df['jailed_times_100_000'] > number_of_jails_for_kick_off].index)
    validators_df = validators_df[~validators_df['operator_address'].isin(black_list)]
    return validators_df.reset_index(drop=True)


def redelegation_balancer(validators_df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns rebalanced df with columns
    source_validator, dist_validator and amount

    Rebalances the most significant amounts in REDELEGATION_NUMBER steps

    :param validators_df:
    :return rebalanced_df:
    """
    df = validators_df.copy(deep=True)
    data = []
    for _ in range(REDELEGATION_NUMBER):
        if df['diff'].min() > 0 or df['diff'].max() < 0:
            break
        min_diff_row = list(df.loc[df['diff'] == df['diff'].min()].index)[0]
        max_diff_row = list(df.loc[df['diff'] == df['diff'].max()].index)[0]

        diff = min(abs(df.loc[min_diff_row, 'diff']), abs(df.loc[max_diff_row, 'diff']))
        df.loc[min_diff_row, 'diff'] += diff
        df.loc[max_diff_row, 'diff'] -= diff
        data_item = (
            df.loc[min_diff_row, 'operator_address'],
            df.loc[max_diff_row, 'operator_address'],
            int(diff)
        )
        data.append(data_item)
    return pd.DataFrame(data, columns=['source_validator', 'dist_validator', 'amount'])
