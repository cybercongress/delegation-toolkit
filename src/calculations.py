import math
import pandas as pd

from config import ALLOCATION, COST_OPTIMIZATION, DECENTRALIZATION, CONFIDENCE, RELIABILITY, SUPERINTELLIGENCE, \
    PUBLIC_ACTIVITY, VALIDATOR_SET


def get_cost_optimization(commission: float) -> float:
    """
    Calculates cost_optimization value by validator's commission value

    :param commission:
    :return cost_optimization:
    """
    if 0.01 <= commission <= 0.10:
        return 1 / (commission ** 2)
    else:
        return 0.0


def get_cost_optimization_endorsement(
        cost_optimization: float,
        cost_optimization_sum: float) -> int:
    """
    Calculates cost_optimization_endorsement value
    by validator's cost_optimization value as share of cost_optimization_sum

    :param cost_optimization:
    :param cost_optimization_sum:
    :return cost_optimization_endorsement:
    """
    return int(cost_optimization / cost_optimization_sum * ALLOCATION * COST_OPTIMIZATION)


def get_decentralization(rank: float) -> float:
    """
    Calculates decentralization value based on validators descending rank

    :param rank:
    :return decentralization:
    """
    return rank


def get_decentralization_endorsement(
        decentralization: float,
        decentralization_sum: float) -> int:
    """
    Calculates decentralization_endorsement value
    by validator's decentralization value as share of decentralization_sum

    :param decentralization:
    :param decentralization_sum:
    :return decentralization_endorsement:
    """
    return int((decentralization / decentralization_sum) * ALLOCATION * DECENTRALIZATION)


def get_confidence(ownership: float) -> float:
    """
    Calculates confidence value based on validator's ownership (self_delegated) value

    :param ownership:
    :return confidence:
    """
    return 1 - (1 / (1e-32 ** (-ownership)))


def get_confidence_endorsement(
        confidence: float,
        confidence_sum: float) -> int:
    """
    Calculates confidence_endorsement value
    by validator's confidence value as share of confidence_sum

    :param confidence:
    :param confidence_sum:
    :return confidence_endorsement:
    """
    return int((confidence / confidence_sum) * ALLOCATION * CONFIDENCE)


def get_reliability(
        jails: int,
        staked: int,
        delegator_shares: float) -> float:
    """
    Calculates reliability value based on
    validators jails number for all time,
    staked tokens and delegators shares

    :param jails:
    :param staked:
    :param delegator_shares:
    :return reliability:
    """
    tokens_bluring = staked / delegator_shares
    if tokens_bluring == 1 and jails == 0:
        return 3
    else:
        return 1 / 2 ** jails + tokens_bluring ** 2


def get_reliability_endorsement(
        reliability: float,
        reliability_sum: float) -> int:
    """
    Calculates reliability_endorsement value
    by validator's reliability value as share of reliability_sum

    :param reliability:
    :param reliability_sum:
    :return reliability_endorsement:
    """
    return int((reliability / reliability_sum) * ALLOCATION * RELIABILITY)


def get_superintelligence(power: float) -> float:
    """
    Calculates superintelligence value based on validators power (amount of volts multiplied to amount of amperes)

    :param power:
    :return superintelligence:
    """
    return math.log10(power + 1)


def get_superintelligence_endorsement(
        superintelligence: float,
        superintelligence_sum: float) -> int:
    """
    Calculates superintelligence_endorsement value
    by validator's superintelligence value as share of superintelligence_sum

    :param superintelligence:
    :param superintelligence_sum:
    :return superintelligence_endorsement:
    """
    return int((superintelligence / superintelligence_sum) * ALLOCATION * SUPERINTELLIGENCE)


def get_public_activity_endorsement(
        exist_passport: bool,
        validators_with_passports_cnt: int) -> int:
    """
    Calculates public_activity_endorsement value
    by validator's passport existing as share of validators_with_passports_cnt

    :param exist_passport:
    :param validators_with_passports_cnt:
    :return public_activity_endorsement:
    """
    assert validators_with_passports_cnt > 0
    return int(exist_passport / validators_with_passports_cnt * ALLOCATION * PUBLIC_ACTIVITY)


def calculate_endorsement(validators_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates cost_optimization, cost_endorsement,
    decentralization, decentralization_endorsement,
    confidence, confidence_endorsement,
    superintelligence, superintelligence_endorsement,
    reliability, reliability_endorsement and total
    for validators_df and returns validators_df with
    named columns

    :param validators_df:
    :return validators_df:
    """
    validators_df.loc[:, 'cost_optimization'] = validators_df.apply(
        lambda x: get_cost_optimization(commission=x['greed']),
        axis=1)
    validators_df.loc[:, 'cost_endorsement'] = validators_df.apply(
        lambda x: get_cost_optimization_endorsement(cost_optimization=x['cost_optimization'],
                                                    cost_optimization_sum=validators_df['cost_optimization'].sum()),
        axis=1)
    validators_df.loc[:, 'decentralization'] = validators_df.apply(
        lambda x: get_decentralization(rank=x['validator_rank']),
        axis=1)
    validators_df.loc[:, 'decentralization_endorsement'] = validators_df.apply(
        lambda x: get_decentralization_endorsement(decentralization=x['decentralization'],
                                                   decentralization_sum=validators_df['decentralization'].sum()),
        axis=1)
    validators_df.loc[:, 'confidence'] = validators_df.apply(
        lambda x: get_confidence(ownership=x['ownership']),
        axis=1)
    validators_df.loc[:, 'confidence_endorsement'] = validators_df.apply(
        lambda x: get_confidence_endorsement(confidence=x['confidence'],
                                             confidence_sum=validators_df['confidence'].sum()),
        axis=1)
    validators_df.loc[:, 'superintelligence'] = validators_df.apply(
        lambda x: get_superintelligence(power=x['power']),
        axis=1)
    validators_df.loc[:, 'superintelligence_endorsement'] = validators_df.apply(
        lambda x: get_superintelligence_endorsement(superintelligence=x['superintelligence'],
                                                    superintelligence_sum=validators_df['superintelligence'].sum()),
        axis=1)
    validators_df.loc[:, 'reliability'] = validators_df.apply(
        lambda x: get_reliability(jails=x['jailed_times_100_000'],
                                  staked=x['staked'],
                                  delegator_shares=x['delegator_shares']),
        axis=1)
    validators_df.loc[:, 'reliability_endorsement'] = validators_df.apply(
        lambda x: get_reliability_endorsement(reliability=x['reliability'],
                                              reliability_sum=validators_df['reliability'].sum()),
        axis=1)
    validators_df.to_csv('validators_test.csv')
    validators_df.loc[:, 'public_activity_endorsement'] = validators_df.apply(
        lambda x: get_public_activity_endorsement(exist_passport=x['exist_passport'],
                                                  validators_with_passports_cnt=validators_df['exist_passport'].sum()),
        axis=1)
    validators_df.loc[:, 'total'] = \
        validators_df['cost_endorsement'] + validators_df['decentralization_endorsement'] + \
        validators_df['confidence_endorsement'] + validators_df['reliability_endorsement'] + \
        validators_df['superintelligence_endorsement'] + validators_df['public_activity_endorsement']
    validators_df = validators_df.sort_values(by=['total'], ascending=False).reset_index(drop=True)
    return rebalance_to_set(validators_df, VALIDATOR_SET)


def rebalance_to_set(
        validators_df: pd.DataFrame,
        validator_set: int) -> pd.DataFrame:
    """
    Rebalance tokens if result set more than validator_set

    :param validators_df:
    :param validator_set:
    :return validator_set:
    """
    if validators_df.shape[0] <= validator_set:
        return validators_df
    else:
        tokens_to_rebalance = validators_df[validator_set:]['total'].sum()
        validators_df = validators_df[:validator_set]
        tokens_total = validators_df['total'].sum()
        validators_df.loc[:, 'total'] = \
            validators_df['total'] + validators_df['total'] / tokens_total * tokens_to_rebalance
        return validators_df
