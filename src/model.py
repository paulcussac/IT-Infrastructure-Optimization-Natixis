import pandas as pd
import numpy as np

def evaluate(pred, valid):
    """Evaluates the performance of Prophet forecasts on validation data.

    Parameters
    ----------
    pred : pd.DataFrame
        Dataframe containing forecasts and ground truth on both training and validation data.
    valid : pd.DataFrame
        Validation data, containing at least a date column (ds) and a target column (y).

    Returns
    -------
    dict
        Performance on validation data (RMSE and MAPE).
    """
    y_pred, y_true = np.array(pred[-len(valid):].yhat), np.array(pred[-len(valid):].y)
    mask = y_true != 0
    mape = np.mean(np.abs((y_true - y_pred) / y_true)[mask])
    rmse = np.sqrt(((y_true - y_pred) ** 2)[mask].mean())
    return {'RMSE': rmse, 'MAPE': mape}


def forecast(model, train, valid):
    """Fits a Prophet model to training data and makes forecasts on validation data.

    Parameters
    ----------
    model : Prophet
        Prophet model instantiated with the desired set of parameters.
    train : pd.DataFrame
        Training data, containing at least a date column (ds) and a target column (y).
    valid : pd.DataFrame
        Validation data, containing at least a date column (ds) and a target column (y).

    Returns
    -------
    pd.DataFrame
        Dataframe containing forecasts and ground truth on both training and validation data.
    """
    model.fit(train)
    full_df = pd.concat([train, valid], axis=0)
    pred = model.predict(full_df)
    pred['y'] = np.array(full_df['y'])
    return pred