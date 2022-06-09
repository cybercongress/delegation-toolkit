import json
import pandas as pd

from config import MSGS_IN_TX, GAS_LIMIT, MEMO


def get_tx(
        messages: list,
        memo: str,
        gas_limit: int) -> dict:
    """
    Returns transaction body in dict for signing

    :param messages:
    :param memo:
    :param gas_limit:
    :return: transaction
    """
    return {
        "body": {
            "messages": messages,
            "memo": memo,
            "timeout_height": "0",
            "extension_options": [],
            "non_critical_extension_options": []
        },
        "auth_info": {
            "signer_infos": [],
            "fee": {
                "amount": [],
                "gas_limit": str(gas_limit),
                "payer": "",
                "granter": ""
            }
        },
        "signatures": []
    }


def get_delegation_msg(
        delegator_address: str,
        validator_address: str,
        amount: int) -> dict:
    """
    Returns delegation message in dict

    :param delegator_address:
    :param validator_address:
    :param amount:
    :return message:
    """
    return {
                "@type": "/cosmos.staking.v1beta1.MsgDelegate",
                "delegator_address": delegator_address,
                "validator_address": validator_address,
                "amount": {
                    "denom": "boot",
                    "amount": str(amount)
                }
            }


def get_redelegation_message(
        delegator_address: str,
        source_validator: str,
        dist_validator: str,
        amount: int) -> dict:
    """
    Returns redelegation message in dict

    :param delegator_address:
    :param source_validator:
    :param dist_validator:
    :param amount:
    :return redelegation_message:
    """
    return {
                "@type": "/cosmos.staking.v1beta1.MsgBeginRedelegate",
                "delegator_address": delegator_address,
                "validator_src_address": source_validator,
                "validator_dst_address": dist_validator,
                "amount": {
                    "denom": "boot",
                    "amount": str(amount)
                }
            }


def get_unsigned_delegation_tx(
        delegator_address: str,
        validator_addresses: list,
        amounts: list) -> dict:
    """
    Returns transaction for signing with messages

    :param delegator_address:
    :param validator_addresses:
    :param amounts: amount of messages
    :return transaction:
    """
    msgs = []
    for validator_address, amount in zip(validator_addresses, amounts):
        msg = get_delegation_msg(delegator_address, validator_address, amount)
        msgs.append(msg)
    return get_tx(msgs, MEMO, GAS_LIMIT)


def get_unsigned_redelegation_tx(
        delegator_address: str,
        source_validators: list,
        dist_validators: list,
        amounts: list) -> dict:
    """
    Returns transaction for signing with messages

    :param delegator_address:
    :param source_validators:
    :param dist_validators:
    :param amounts:
    :return transaction:
    """
    msgs = []
    for source_validator, dist_validator, amount in zip(source_validators, dist_validators, amounts):
        msg = get_redelegation_message(delegator_address, source_validator, dist_validator, amount)
        msgs.append(msg)
    return get_tx(msgs, MEMO, GAS_LIMIT)


def get_unsigned_delegation_txs(
        delegator_address: str,
        df: pd.DataFrame) -> None:
    """
    Pack by MSGS_IN_TX messages and save transaction files in ./txs/

    :param delegator_address:
    :param df:
    """
    counter = df.shape[0] // MSGS_IN_TX + 1
    c = 0
    for i in range(counter):
        tx = get_unsigned_delegation_tx(
            delegator_address,
            df[c: c + MSGS_IN_TX].operator_address.to_list(),
            df[c: c + MSGS_IN_TX].total.to_list())
        if tx['body']['messages'] == []:
            continue
        else:
            with open(f"./txs/unsigned_{i}.json", "w") as fp:
                json.dump(tx, fp, indent=4)
            c += MSGS_IN_TX


def get_unsigned_redelegation_txs(
        delegator_address: str,
        df: pd.DataFrame) -> None:
    """
    Pack by MSGS_IN_TX messages and save transaction files in ./txs/

    :param delegator_address:
    :param df:
    """
    counter = df.shape[0] // MSGS_IN_TX + 1
    c = 0
    for i in range(counter):
        tx = get_unsigned_redelegation_tx(
            delegator_address,
            df[c: c + MSGS_IN_TX].source_validator.to_list(),
            df[c: c + MSGS_IN_TX].dist_validator.to_list(),
            df[c: c + MSGS_IN_TX].amount.to_list())
        if not tx['body']['messages']:
            continue
        else:
            with open(f"./txs/unsigned_{i}.json", "w") as fp:
                json.dump(tx, fp, indent=4)
            c += MSGS_IN_TX


