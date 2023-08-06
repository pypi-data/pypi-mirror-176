import os

from datetime import datetime

import pandas as pd

from google.cloud import bigquery

from super_eureka import logging

def submit_for_bigquery(filepath: str) -> None:
    logging.info('Trying to submit file to BigQuery.')

    client = bigquery.Client()
    job_config = bigquery.LoadJobConfig(
        create_disposition='CREATE_IF_NEEDED',
        write_disposition='WRITE_APPEND'
    )

    logging.info('Reading file...')
    df = pd.read_csv(filepath, na_values='(No value)')

    logging.info('Procesing...')
    df.columns = df.columns.str.replace(' ', '_')
    df.rename(columns={
        'ad_group_id': 'ad_group_id_new',
        'ad_id': 'ad_id_new'
    }, inplace=True)
    df.columns = df.columns.str.upper()

    table_id = os.getenv('BIGQUERY_TABLE_ID')

    logging.info('Uploading...')
    load_job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    result = load_job.result()

    if not result.error_result:
        logging.info('Success!')
    else:
        logging.info('Failed with the following error(s):')
        for error in result.errors:
            logging.info(f'\t{repr(error)}')
        
        now = datetime.now()
        file_name = f'failure_{now.day}-{now.month}-{now.day} {now.hour}-{now.minute}-{now.second}.csv'
        folder = os.path.dirname(filepath)
        renamed_file_path = os.path.join(folder, file_name)
        os.rename(filepath, renamed_file_path)
        logging.info(f'The file will be renamed as {file_name} and kept for future upload.')

