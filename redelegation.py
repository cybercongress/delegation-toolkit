import os
import pandas as pd

from src.get_data import get_delegations
from config import DELEGATOR_ADDRESS, NEW_STAKE_AMOUNT, NEW_STAKE_HERO
from main import get_result_table
from src.utils import redelegation_balancer
from src.tx import get_unsigned_redelegation_txs


def redelegate() -> None:
    """
    Processes redelegation strategy

    1. Gets data of the current DELEGATOR_ADDRESS delegations
    2. Gets new delegation distribution
    3. Merges two dataframes by operator_address and finds diffs
    4. Rebalances current delegation distribution to new one
    5. Creates transaction files in ./txs/
    """
    old_delegations_df = get_delegations(DELEGATOR_ADDRESS)
    new_delegations_df = get_result_table()
    new_delegations_df.to_csv('./delegation_strategy.csv', index=False)
    validators_df_raw = pd.merge(new_delegations_df, old_delegations_df, on='operator_address', how='outer')
    validators_df_raw = validators_df_raw[['operator_address', 'delegation', 'total']]
    validators_df = validators_df_raw.copy().fillna(0)
    validators_df = validators_df.rename(columns={'delegation': 'current_delegation', 'total': 'calculated_delegation'})
    validators_df.loc[validators_df[validators_df['operator_address'] == NEW_STAKE_HERO].index,
                      'current_delegation'] += NEW_STAKE_AMOUNT
    validators_df['diff'] = validators_df['calculated_delegation'] - validators_df['current_delegation']
    validators_df = validators_df.sort_values(by='diff', ascending=False)
    validators_df.to_csv('./redelegation_strategy.csv')
    balanced_df = redelegation_balancer(validators_df)
    balanced_df.to_csv('./rebalanced_table.csv')
    balanced_df.sort_values(by='amount')
    try:
        os.mkdir('./txs')
    except OSError:
        pass
    get_unsigned_redelegation_txs(DELEGATOR_ADDRESS, balanced_df)


if __name__ == '__main__':
    redelegate()
