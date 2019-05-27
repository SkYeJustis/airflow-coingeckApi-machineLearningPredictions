from core.execute_data_predict import core_make_db_predictions
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

DAG_VERSION = 'PREDICT-CRYPTO-BTC-USD-1.0'

dag = DAG(DAG_VERSION,
          default_args=default_args,
          schedule_interval=SCHEDULE_INTERVAL,
          concurrency=1,
          max_active_runs=1,
          catchup=True)

make_db_predictions = PythonOperator(
    task_id = 'make_db_predictions',
    python_callable=core_make_db_predictions,
    retries=0,
    provide_context=True,
    dag=dag
)

make_db_predictions