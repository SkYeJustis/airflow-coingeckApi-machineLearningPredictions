from Cryptocurrency.database_connect import DatabaseOperator
from Cryptocurrency.data_collect import CoinGeckoApi

# crypto
# ccy
# date

# https://diogoalexandrefranco.github.io/about-airflow-date-macros-ds-and-execution-date/

def core_get_data(**kwargs):
    task_instance = kwargs['ti']
    execution_date = task_instance.execution_date.strftime("%d-%m-%Y")
    crypto_df = CoinGeckoApi(crypto=kwargs['crypto'], ccy=kwargs['ccy']).get_data(execution_date)
    task_instance.xcom_push(key='crypto_df', value=crypto_df)


def core_db_insert_to_db(**kwargs):
    task_instance = kwargs['ti']
    db_oper = DatabaseOperator()
    db_oper.create_engine_pgsql()
    crypto_df = task_instance.xcom_pull(key='crypto_df', task_ids='get_crypto_data')
    db_oper.insert_to_db(crypto_df, kwargs['table_name'])