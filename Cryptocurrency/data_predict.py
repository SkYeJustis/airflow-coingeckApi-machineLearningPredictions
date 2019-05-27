from statsmodels.tsa.holtwinters import ExponentialSmoothing, SimpleExpSmoothing
import pandas as pd

class CryptoDataPredictions:

    def __init__(self):
        self.models = {}

    def fit_ts_univariate_model(self, x, model_type = 'SimpleExpSmoothing'):
        if model_type == 'ExponentialSmoothing':
            model = ExponentialSmoothing(x)
            model_fit = model.fit()
        else:
            model = SimpleExpSmoothing(x)
            model_fit = model.fit()
        self.models[model_type] = model_fit

    def predict_ts_univariate_model(self, end_ts, model_type = 'SimpleExpSmoothing'):
        # Predict 1 day at a time
        yhat = self.models[model_type].forecast(1).values[0]
        pred_data = [[end_ts, model_type, yhat]]
        return pd.DataFrame(data=pred_data, columns=['date', 'model_type', 'prediction_value'])

if __name__ == '__main__':
    #Any test code
    pass