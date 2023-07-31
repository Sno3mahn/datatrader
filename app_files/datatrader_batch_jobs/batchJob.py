import logging
import sys
import pandas
import requests
import forecast

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def __batch_main__(sub_job_name, scheduled_time, runtime, part_num, num_parts, job_config, rundate, *args):

    logging.info(f"{sub_job_name=}")
    logging.info(f"{scheduled_time=}")
    logging.info(f"{runtime=}")
    logging.info(f"{part_num=}")
    logging.info(f"{num_parts=}")
    logging.info(f"{job_config=}")
    logging.info(f"{rundate=}")
    
    forecast.func()

    return 0
