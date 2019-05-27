from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Cryptocurrency.data_predict import CryptoDataPredictions
import pandas as pd
from datetime import datetime, timedelta


class DatabaseOperator:

    def __init__(self, connection=None):
        self.connection = connection or 'postgresql+psycopg2://postgres:postgres@localhost:5433/cryptocurrency'
        self.cdp = CryptoDataPredictions()

    def create_engine_pgsql(self):
        #postgresql+psycopg2://user:password@hostname:host/database_name
        engine = create_engine(self.connection, echo=False)
        self.engine = engine

    # For data update from api
    def insert_to_db(self, df, table_name):
        print("TABLE NAME: {0}".format(table_name))
        df.to_sql(table_name, con=self.engine, if_exists="append", index=False)

    def get_db_data(self, pred_date):
        Session = sessionmaker()
        Session.configure(bind=self.engine)
        session = Session()
        df = pd.read_sql('SELECT * FROM public.bitcoin_historical_data', session.bind)
        df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y') # dd-mm-yyyy
        df.sort_values(by=['date'], ascending=True, inplace=True)

        #df['date_format'] = df[['date']].strftime('%Y%m%d')

        end_ts_obj = datetime.strptime(pred_date, '%Y-%m-%d')
        final_end_ts = end_ts_obj - timedelta(days=1)
        print(final_end_ts)
        df = df[(df['date'] < final_end_ts)]
        self.df = df

    def insert_to_db_predictions(self, table_name, model_type, end_ts):
        x = self.df['current_price']
        #print(self.df['current_price'])
        self.cdp.fit_ts_univariate_model(x, model_type)
        pred_data_df = self.cdp.predict_ts_univariate_model(end_ts, model_type)
        pred_data_df.to_sql(table_name, con=self.engine, if_exists="append", index=False)
        #print(pred_data_df.get_values())

if __name__ == '__main__':
    db_oper = DatabaseOperator()
    db_oper.create_engine_pgsql()

    # Testing prediction sequence
    prediction_date = '2019-05-05'
    db_oper.get_db_data(prediction_date)
    print(db_oper.df.columns)
    print(db_oper.df.get_values())
    db_oper.insert_to_db_predictions("bitcoin_forecasts", "ExponentialSmoothing", prediction_date)
