from core.execute_data_collect import core_get_data, core_db_insert_to_db
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

SCHEDULE_INTERVAL = '@daily'

default_args = {
    'owner': 'SkYe',
    'start_date': datetime(2019,2,1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=1)
}

DAG_VERSION = 'COLLECT-CRYPTO-BTC-USD-1.0'

dag = DAG(DAG_VERSION,
          default_args=default_args,
          schedule_interval=SCHEDULE_INTERVAL,
          concurrency=1,
          max_active_runs=1,
          catchup=True)

get_crypto_data = PythonOperator(
    task_id = 'get_crypto_data',
    python_callable=core_get_data,
    retries=0,
    provide_context=True,
    op_kwargs = { "crypto": "bitcoin",
                  "ccy": "usd" },
    dag=dag
)

db_insert_to_crypto_db = PythonOperator(
    task_id='db_insert_to_crypto_db',
    python_callable=core_db_insert_to_db,
    retries=0,
    provide_context=True,
    op_kwargs= {"table_name": "bitcoin_historical_data"},
    dag=dag
)

get_crypto_data >> db_insert_to_crypto_db