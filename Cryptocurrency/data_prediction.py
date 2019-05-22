from statsmodels.tsa.holtwinters import ExponentialSmoothing
import pandas as pd


#####################################
# IN - PROGRESS: For data predictions
class CryptoDataPredictions:

    def __init__(self):
        pass

    def get_data(self):
        pass

    def fit_model(self, data):
        #data = df['current_price']

        #data_exog = df['']
        #closed issue / total issues

        model = ExponentialSmoothing(data)
        #model = VARMAX(data, exog=data_exog, order=(1, 1))
        pass

    def make_predictions(self):
        pass
