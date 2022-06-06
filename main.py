import os
import shutil

from config import BLACK_LIST, NUMBER_OF_JAILS_FOR_KICKOFF, DELEGATOR_ADDRESS
from src.calculations import calculate_endorsement
from src.get_data import get_validators
from src.tx import get_unsigned_txs
from src.utils import clean_up_validators_set


def processor():
    """
    Processes delegation strategy.
    1. Gets validators info
    2. Sorts validators by staked tokens descending and ranks them in validator_rank column
    3. Drops validators by clean_up_validators_set definition
    4. Calculates endorsements and total
    5. Saves results to ./delegation_strategy.csv
    6. Sort by total ascending for transactions generated from less to high values
    7. Removes ./txs folder if exists
    8. Creates ./txs folder
    9. Save unsigned .json transactions in the ./txs folder
    """
    validators_df = get_validators()
    validators_df['validator_rank'] = validators_df['staked'].rank(ascending=False)
    validators_df = clean_up_validators_set(validators_df, NUMBER_OF_JAILS_FOR_KICKOFF, BLACK_LIST)
    validators_df = calculate_endorsement(validators_df)
    validators_df.to_csv('./delegation_strategy.csv', index=False)
    validators_df = validators_df.sort_values(by=['total']).reset_index(drop=True)
    try:
        shutil.rmtree('./txs')
    except OSError as e:
        print("Error: %s : %s" % ('./txs', e.strerror))
    os.mkdir('./txs')
    get_unsigned_txs(DELEGATOR_ADDRESS, validators_df)


if __name__ == '__main__':
    processor()