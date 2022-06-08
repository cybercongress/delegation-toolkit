import os
import shutil

from config import BLACK_LIST, NUMBER_OF_JAILS_FOR_KICKOFF, DELEGATOR_ADDRESS
from src.calculations import calculate_endorsement
from src.get_data import get_validators
from src.tx import get_unsigned_delegation_txs
from src.utils import clean_up_validators_set


def get_result_table():
    """
    1. Gets validators info
    2. Sorts validators by staked tokens descending and ranks them in validator_rank column
    3. Drops validators by clean_up_validators_set definition
    4. Returns dataframe with calculated endorsement
    :return:
    """
    validators_df = get_validators()
    validators_df['validator_rank'] = validators_df['staked'].rank(ascending=False)
    validators_df = clean_up_validators_set(validators_df, NUMBER_OF_JAILS_FOR_KICKOFF, BLACK_LIST)
    return calculate_endorsement(validators_df)


def processor():
    """
    Processes delegation strategy.
    1. Gets result table
    2. Saves results to ./delegation_strategy.csv
    3. Sort by total ascending for transactions generated from less to high values
    5. Removes ./txs folder if exists
    6. Creates ./txs folder
    7. Save unsigned .json transactions in the ./txs folder
    """
    validators_df = get_result_table()
    validators_df.to_csv('./delegation_strategy.csv', index=False)
    validators_df = validators_df.sort_values(by=['total']).reset_index(drop=True)
    try:
        shutil.rmtree('./txs')
    except OSError as e:
        print("Error: %s : %s" % ('./txs', e.strerror))
    os.mkdir('./txs')
    get_unsigned_delegation_txs(DELEGATOR_ADDRESS, validators_df)


if __name__ == '__main__':
    processor()