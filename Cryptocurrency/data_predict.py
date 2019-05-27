from statsmodels.tsa.holtwinters import ExponentialSmoothing, SimpleExpSmoothing
from statsmodels.tsa.arima_model import ARIMA
import pandas as pd

class CryptoDataPredictions:

    def __init__(self):
        self.models = {}

    def fit_ts_univariate_model(self, x, model_type = 'SimpleExpSmoothing'):
        if model_type == 'ExponentialSmoothing':
            model = ExponentialSmoothing(x)
            model_fit = model.fit()
        elif model_type == 'ARIMA':
            model = ARIMA(x, order=(1, 1, 1))
            model_fit = model.fit(disp=False)
        else:
            model = SimpleExpSmoothing(x)
            model_fit = model.fit()
        self.models[model_type] = model_fit

    def predict_ts_univariate_model(self, end_ts, model_type = 'SimpleExpSmoothing'):
        # Predict 1 day at a time
        if model_type == 'ARIMA':
            yhat = self.models[model_type].forecast()[0][0]
        else:
            yhat = self.models[model_type].forecast(1).values[0]
        pred_data = [[end_ts, model_type, yhat]]
        return pd.DataFrame(data=pred_data, columns=['date', 'model_type', 'prediction_value'])

if __name__ == '__main__':
    # Any test code #
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from datetime import datetime, timedelta

    engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5433/cryptocurrency', echo=False)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    df = pd.read_sql('SELECT * FROM public.bitcoin_historical_data', session.bind)
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')  # dd-mm-yyyy
    df.sort_values(by=['date'], ascending=True, inplace=True)

    pred_date = '2019-05-05'

    end_ts_obj = datetime.strptime(pred_date, '%Y-%m-%d')
    final_end_ts = end_ts_obj - timedelta(days=1)
    print(final_end_ts)
    input_df = df[(df['date'] < final_end_ts)]

    x = input_df['current_price']

    cdp = CryptoDataPredictions()

    cdp.fit_ts_univariate_model(x, model_type='SimpleExpSmoothing')
    cdp.fit_ts_univariate_model(x, model_type='ARIMA')

    pred = cdp.predict_ts_univariate_model(pred_date, model_type = 'ARIMA')
    print(pred.get_values())

    pred = cdp.predict_ts_univariate_model(pred_date, model_type = 'SimpleExpSmoothing')
    print(pred.get_values())

# = sql to check data  =
# SELECT TO_TIMESTAMP(d.date,'DD-MM-YYYY'), model_type, current_price, prediction_value
# FROM public.bitcoin_historical_data d
# LEFT JOIN public.bitcoin_forecasts p
#     ON ( TO_TIMESTAMP(p.date,'YYYY-MM-DD') = TO_TIMESTAMP(d.date,'DD-MM-YYYY')
#         and model_type = 'ExponentialSmoothing' )
# ORDER BY TO_TIMESTAMP(d.date,'DD-MM-YYYY') asc, model_type;

# SELECT TO_TIMESTAMP(d.date,'DD-MM-YYYY'), model_type, current_price, prediction_value
# FROM public.bitcoin_historical_data d
# LEFT JOIN public.bitcoin_forecasts p
#     ON ( TO_TIMESTAMP(p.date,'YYYY-MM-DD') = TO_TIMESTAMP(d.date,'DD-MM-YYYY')
#         and model_type = 'SimpleExpSmoothing' )
# ORDER BY TO_TIMESTAMP(d.date,'DD-MM-YYYY') asc, model_type;