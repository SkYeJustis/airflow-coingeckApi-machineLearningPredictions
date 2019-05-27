from Cryptocurrency.database_connect import DatabaseOperator

def core_make_db_predictions(**kwargs):
    task_instance = kwargs['ti']
    # '2019-05-10' -> '%Y-%m-%d' ->  yyyy-mm-dd
    prediction_date = task_instance.execution_date.strftime('%Y-%m-%d')
    db_oper = DatabaseOperator()
    db_oper.create_engine_pgsql()
    db_oper.get_db_data(prediction_date)
    db_oper.insert_to_db_predictions("bitcoin_forecasts", "ExponentialSmoothing", prediction_date)