"""all calculations for """

import pandas as pd

from zeno_etl_libs.utils.distributor_ranking2.pull_data import pull_data_dc, pull_data_franchisee
from zeno_etl_libs.utils.distributor_ranking2.calculate_ranking import calc_ranking_dc
from zeno_etl_libs.utils.distributor_ranking2.preprocess_features import preprocess_features_dc
from zeno_etl_libs.utils.distributor_ranking2.calculate_features import calculate_features


def ranking_calc_dc(reset_date, time_interval_dc, as_low_vol_cutoff_dc,
            pr_low_vol_cutoff_dc, volume_fraction, logger, db, schema):

    # =============================== PULL DATA ===============================

    logger.info('Pulling data for DC')
    # add 7 days to time interval since we do not want to include last week's data.
    time_interval = time_interval_dc + 7

    df_features, df_distributors = pull_data_dc(reset_date, time_interval, db, schema)
    logger.info('Data pull for DC completed')

    # ========================== DATA PRE-PROCESSING ==========================

    logger.info('Data preprocessing starts')
    df_features = preprocess_features_dc(df_features, db, schema)

    # add distributor name and distributor features here.
    df_features = pd.merge(df_features, df_distributors, on=['partial_distributor_id'],
                           how='left', validate='many_to_one')
    logger.info('Data preprocessing completed')

    # ========================== FEATURE CALCULATION ==========================

    logger.info('Feature calculation starts')
    features = calculate_features(df_features, reset_date, time_interval_dc,
                                  group_cols=['partial_dc_id',
                                              'partial_distributor_id',
                                              'drug_id'])

    # add drug type column
    features = pd.merge(features,
                        df_features[['drug_id', 'drug_type']].drop_duplicates(),
                        on=['drug_id'],
                        how='left',
                        validate='many_to_one')

    # add dist type column
    features = pd.merge(features, df_features[
        ['partial_distributor_id', 'partial_distributor_name',
         'partial_distributor_type', 'partial_distributor_credit_period']].drop_duplicates(),
                        on=['partial_distributor_id'], how='left',
                        validate='many_to_one')

    # add dc name
    features = pd.merge(features, df_features[
        ['partial_dc_id', 'dc_name']].dropna().drop_duplicates(),
                        on=['partial_dc_id'], validate='many_to_one',
                        how='left')

    # add drug name
    features = pd.merge(features,
                        df_features[['drug_id', 'drug_name']].drop_duplicates(),
                        on=['drug_id'], validate='many_to_one', how='left')
    logger.info('Feature calculation completed')

    # ============================ CALCULATE RANKS ============================

    logger.info('Ranking starts')
    df_ranking = calc_ranking_dc(features)




    return df_features


