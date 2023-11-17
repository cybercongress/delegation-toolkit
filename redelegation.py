import os
import pandas as pd

from src.get_data import get_delegations
from config import DELEGATOR_ADDRESS, NEW_STAKE_HERO_DICT, INITIAL_SEQUENCE, LCD_CLIENT
from main import get_result_table
from src.utils import redelegation_balancer
from src.tx import get_unsigned_redelegation_txs, get_unsigned_delegation_txs


def calculate_redelegation() -> pd.DataFrame:
    """
    Processes redelegation strategy

    1. Gets data of the current DELEGATOR_ADDRESS delegations
    2. Gets new delegation distribution
    3. Merges two dataframes by operator_address and finds diffs
    4. Rebalances current delegation distribution to new one
    """
    _old_delegations_df = get_delegations(DELEGATOR_ADDRESS)
    _new_delegations_df = get_result_table()
    _new_delegations_df.to_csv('./delegation_strategy.csv', index=False)
    _validators_df_raw = pd.merge(_new_delegations_df, _old_delegations_df, on='operator_address', how='outer')
    _validators_df_raw = _validators_df_raw[['operator_address', 'delegation', 'total']]
    _validators_df = _validators_df_raw.copy().fillna(0)
    _validators_df = _validators_df.rename(columns={'delegation': 'current_delegation', 'total': 'calculated_delegation'})
    for _new_stake_hero_address, _new_stake_hero_amount in NEW_STAKE_HERO_DICT.items():
        _validators_df.loc[_validators_df[_validators_df['operator_address'] == _new_stake_hero_address].index,
                           'current_delegation'] += _new_stake_hero_amount
    _validators_df['diff'] = _validators_df['calculated_delegation'] - _validators_df['current_delegation']
    _validators_df = _validators_df.sort_values(by='diff', ascending=False)
    _validators_df.to_csv('./redelegation_strategy.csv')
    _balanced_df = redelegation_balancer(_validators_df)
    _balanced_df.to_csv('./rebalanced_table.csv')
    _balanced_df.sort_values(by='amount')
    return _balanced_df


def redelegate() -> None:
    """
    Processes redelegation strategy

    1. Calculate redelegation
    2. Creates transaction files in ./txs/
    """
    _balanced_df = calculate_redelegation()
    _initial_sequence = INITIAL_SEQUENCE if INITIAL_SEQUENCE else LCD_CLIENT.auth.account_info(
        DELEGATOR_ADDRESS).sequence
    print(f'initial sequence: {_initial_sequence}')
    try:
        os.mkdir('./txs')
    except OSError:
        pass
    _next_sequence = get_unsigned_redelegation_txs(delegator_address=DELEGATOR_ADDRESS,
                                                   redelegations_df=_balanced_df,
                                                   initial_sequence=_initial_sequence)
    get_unsigned_delegation_txs(delegator_address=DELEGATOR_ADDRESS,
                                delegation_df=pd.DataFrame(NEW_STAKE_HERO_DICT.items(),
                                                           columns=['operator_address', 'total']),
                                initial_sequence=_next_sequence)


if __name__ == '__main__':
    redelegate()
