from accelo_mlops import AcceloClient
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import datetime as dt
import joblib
import sys
from unittest.mock import MagicMock

sys.modules['accelo'] = MagicMock()
ORG_KEY = 'ORG_KEY'
API_KEY = 'API_KEY'


def load_model():
    return joblib.load('/Users/apple/acceldata/ad-mlops-sdk/examples/deposit_prediction/random_forest_classifier.pkl')


def load_baseline_data():
    return pd.read_csv('/Users/apple/acceldata/ad-mlops-sdk/examples/deposit_prediction/baseline_model_data.csv')


def one_hot_encode(dataframe, column_list, drop_first_flag=True):
    for x in column_list:
        dummies = pd.get_dummies(dataframe[x], prefix=x, dummy_na=False, drop_first=drop_first_flag)
        dataframe = dataframe.drop(x, 1)
        dataframe = pd.concat([dataframe, dummies], axis=1)
    return dataframe


def load_serving_data(date_filter) -> pd.DataFrame:
    df = pd.read_csv('/Users/apple/acceldata/ad-mlops-sdk/examples/deposit_prediction/input/bank-full.csv',
                     delimiter=';')
    df = df.rename(columns={'y': 'deposit'})
    date_col = pd.DataFrame(pd.date_range(start='2021-01-01', periods=df.shape[0], freq='min'),
                            columns=['load_datetime'])
    df['load_datetime'] = date_col
    df['load_dt'] = df['load_datetime'].dt.date

    serving_df = df[(df.load_dt == date_filter)].copy()
    serving_df.name = 'serving_df_' + str(date_filter)
    return serving_df


def feature_transform(df: pd.DataFrame) -> pd.DataFrame:
    # Create a Balance Category
    df["balance_status"] = np.nan
    lst = [df]

    for col in lst:
        col.loc[col["balance"] < 0, "balance_status"] = "negative"
        col.loc[(col["balance"] >= 0) & (col["balance"] <= 30000), "balance_status"] = "low"
        col.loc[(col["balance"] > 30000) & (col["balance"] <= 40000), "balance_status"] = "middle"
        col.loc[col["balance"] > 40000, "balance_status"] = "high"

    df = one_hot_encode(df, ['job', 'marital', 'education', 'contact', 'poutcome', 'balance_status'])
    df['loan'] = LabelEncoder().fit_transform(df['loan'])
    df['housing'] = LabelEncoder().fit_transform(df['housing'])
    df['default'] = LabelEncoder().fit_transform(df['default'])
    df['deposit'] = LabelEncoder().fit_transform(df['deposit'])

    df.drop("duration", axis=1, inplace=True)
    df.drop("month", axis=1, inplace=True)
    df.drop("load_datetime", axis=1, inplace=True)
    df.drop("load_dt", axis=1, inplace=True)
    df = df.loc[:, df.columns != 'deposit']
    return df


def label_predict(model, df: pd.DataFrame) -> pd.DataFrame:
    preds = model.predict(df)
    return pd.DataFrame([str(x) for x in preds])


if __name__ == "__main__":
    MODEL_ID = 1234  # received this when they registered model with our API when creating the pipeline
    MODEL_VERSION = 1
    client = AcceloClient(ad_access_key=ORG_KEY, ad_secret_key=API_KEY, workspace='phonepe')

    classifer = load_model()
    baseline_df = load_baseline_data()
    print('Training dataset shape', baseline_df.shape)

    serving_date = dt.date(2021, 1, 26)
    serving_data = load_serving_data(serving_date)

    predictions = np.random.randint(0, 2, size=serving_data.shape[0])
    actuals = np.random.randint(0, 2, size=serving_data.shape[0])

    print(serving_data.shape)
    print(actuals.shape)
    print(predictions.shape)

    ##### Instrument Acceldata SDK to log the actuals and predictions together ######
    client.log_predictions_and_actuals(feature_data=serving_data,
                                       predictions=list(predictions),
                                       actuals=list(actuals),
                                       model_id=MODEL_ID,
                                       model_version=MODEL_VERSION)

    ##### Instrument Acceldata SDK to log the predictions ######
    # ids = client.log_predictions(feature_data=serving_features,
    #                              predictions=predictions,
    #                              model_id=MODEL_ID,
    #                              model_version=MODEL_VERSION) # store the ids
    #
    # client.log_actuals(actual_labels=actuals,
    #                    actual_ixs=ids,
    #                    model_id=MODEL_ID,
    #                    model_version=MODEL_VERSION)
