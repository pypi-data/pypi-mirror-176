"""main wrapper for Distributor Ranking 2.0 algorithm"""

import os
import sys
import argparse

import pandas as pd
import numpy as np
import datetime as dt

from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.db.db import DB, MySQL
from zeno_etl_libs.logger import get_logger

from zeno_etl_libs.utils.distributor_ranking2.distributor_ranking_calc import ranking_calc_dc


def main(debug_mode, time_interval_dc, time_interval_franchisee, as_low_vol_cutoff_dc,
         pr_low_vol_cutoff_dc, low_volume_cutoff_franchisee, volume_fraction, s3,
         rs_db_read, rs_db_write, read_schema, write_schema):

    mysql_write = MySQL(read_only=False)
    logger.info(f"Debug Mode: {debug_mode}")
    status = 'Failed'
    reset_date = dt.date.today()

    try:
        # calculate ranks
        logger.info("Calculating Zippin DC-level Ranking")
        features_rank_dc = ranking_calc_dc(
            reset_date, time_interval_dc, as_low_vol_cutoff_dc,
            pr_low_vol_cutoff_dc, volume_fraction, logger,
            db=rs_db_read, schema=read_schema)
        logger.info("Completed Zippin DC-level Ranking")

        x = 1

    except:
        None

    return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="This is ETL script.")
    parser.add_argument('-e', '--env', default="dev", type=str, required=False)
    parser.add_argument('-et', '--email_to',
                        default="vivek.revi@zeno.health", type=str,
                        required=False)

    parser.add_argument('-d', '--debug_mode', default="Y", type=str, required=False)
    parser.add_argument('-ti', '--time_interval_dc', default=90, type=int, required=False)
    parser.add_argument('-tif', '--time_interval_franchisee', default=180, type=int, required=False)

    parser.add_argument('-aslvcd', '--as_low_vol_cutoff_dc', default=0.02, type=float,
                        required=False)
    parser.add_argument('-prlvcd', '--pr_low_vol_cutoff_dc', default=0.01, type=float,
                        required=False)
    parser.add_argument('-lvcf', '--low_vol_cutoff_franchisee', default=0.0, type=float,
                        required=False)
    parser.add_argument('-vf', '--vol_frac', default="0.5-0.3-0.2", type=str,
                        required=False)

    args, unknown = parser.parse_known_args()

    env = args.env
    os.environ['env'] = env
    email_to = args.email_to

    debug_mode = args.debug_mode
    time_interval_dc = args.time_interval_dc
    time_interval_franchisee = args.time_interval_franchisee
    as_low_vol_cutoff_dc = args.as_low_vol_cutoff_dc
    pr_low_vol_cutoff_dc = args.pr_low_vol_cutoff_dc
    low_volume_cutoff_franchisee = args.low_vol_cutoff_franchisee
    volume_fraction = args.vol_frac

    logger = get_logger()
    s3 = S3()
    rs_db_read = DB(read_only=True)
    rs_db_write = DB(read_only=False)
    read_schema = 'prod2-generico'
    write_schema = 'prod2-generico'

    # open RS connection
    rs_db_read.open_connection()
    rs_db_write.open_connection()

    """ calling the main function """
    main(debug_mode, time_interval_dc, time_interval_franchisee, as_low_vol_cutoff_dc,
         pr_low_vol_cutoff_dc, low_volume_cutoff_franchisee, volume_fraction, s3,
         rs_db_read, rs_db_write, read_schema, write_schema)

    # close RS connection
    rs_db_read.close_connection()
    rs_db_write.close_connection()