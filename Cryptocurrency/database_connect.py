from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Cryptocurrency.data_retrieval import CoinGeckoApi
import pandas as pd
from datetime import datetime, timedelta
from statsmodels.tsa.holtwinters import ExponentialSmoothing


class DatabaseOperator:

    def __init__(self, connection=None):
        self.connection = connection or 'postgresql+psycopg2://postgres:postgres@localhost:5433/cryptocurrency'



    def create_engine_pgsql(self):
        #postgresql+psycopg2://user:password@hostname:host/database_name
        engine = create_engine(self.connection, echo=False)
        self.engine = engine

    # For data update from api
    def insert_to_db(self, df, table_name):
        print("TABLE NAME: {0}".format(table_name))
        df.to_sql(table_name, con=self.engine, if_exists="append", index=False)

    ######################################
    # IN - PROGRESS: For data predictions
    def get_db_data(self, end_ts):
        Session = sessionmaker()
        Session.configure(bind=self.engine)
        session = Session()
        df = pd.read_sql('SELECT * FROM public.bitcoin_historical_data', session.bind)
        df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y') # dd-mm-yyyy
        df.sort_values(by=['date'], ascending=True, inplace=True)

        #df['date_format'] = df[['date']].strftime('%Y%m%d')

        end_ts_obj = datetime.strptime(end_ts, '%Y-%m-%d')
        final_end_ts = end_ts_obj - timedelta(days=1)
        print(final_end_ts)
        df = df[(df['date'] < final_end_ts)]
        self.df = df
        return df

    ######################################
    # IN - PROGRESS: For data predictions
    def insert_to_db_predictions(self, table_name, end_ts):
        X = self.df['current_price']
        model = ExponentialSmoothing(X)
        model_fit = model.fit()

        # Predict 1 day at a time
        yhat = model_fit.forecast(1).values[0]
        pred_data = [[end_ts, yhat]]
        pred_data_df = pd.DataFrame(data=pred_data,
                     columns= ['date', 'HoltExponentialSmoothing'])
        pred_data_df.to_sql(table_name, con=self.engine, if_exists="append", index=False)

        return yhat

if __name__ == '__main__':
    db_oper = DatabaseOperator()
    db_oper.create_engine_pgsql()

    #cga  = CoinGeckoApi()
    #df = cga.get_data('29-12-2018')
    #db_oper.insert_to_db(df, '{0}_historical_data'.format('bitcoin'))

    df = db_oper.get_db_data('2019-05-10')
    print(df.columns)
    print(df.get_values())

    x = db_oper.insert_to_db_predictions("bitcoin_forecasts")
    print(x)
