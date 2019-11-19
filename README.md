# airflow-coingeckApi-machineLearningPredictions

## File structure for dags and additional logic at AIRFLOW_HOME
* AIRFLOW_HOME=~/airflow

<br><br>
> Cryptocurrency (business functions) <br>
>> data_collect.py
>> data_predict.py
>> database.connect.py

> src <br>
>> core (core etl logic) <br>
>>> execute_data_collect.py <br>
>>> execute_data_predict.py <br>

>> dags <br>
>>> collect_bitcoin_usd_crypto_data.py <br>
>>> predict_bitcoin_usd_crypto_data.py <br>
