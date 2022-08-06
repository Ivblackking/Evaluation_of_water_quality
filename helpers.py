import pandas as pd
import numpy as np
from xgboost import XGBClassifier


def predicting_layout(filepath, modelpath, minerals_for_del, targets):

    data = pd.read_excel(filepath)
    data = data.drop(["Sample ID"], axis = 1)
    df = data.fillna(0)

    for row in range(df.shape[0]):
        for col in list(df.columns):
            if type(df.loc[row, col]) == str:
                df.loc[row, col] = np.nan

            elif df.loc[row, col] < 0:
                df.loc[row, col] = np.nan
    
    df2 = df.fillna(0)

    X = df2.drop(minerals_for_del, axis = 1)

    model = XGBClassifier()
    model.load_model(modelpath)

    y_pred = model.predict(X)

    class_id = y_pred[0]

    return targets[class_id]


def test_Drinking(filepath):

    minerals_for_del1 = ["Mineral35","Mineral37", "Mineral39", "Mineral40", "Mineral41", "Mineral44", "Mineral45"]
    minerals_for_del2 = ["Mineral4","Mineral12","Mineral13","Mineral14","Mineral18","Mineral19",
                         "Mineral22", "Mineral36", "Mineral38"]
    
    minerals_for_del = minerals_for_del1 + minerals_for_del2
    return predicting_layout(filepath, "Models/Model_drinking.json", minerals_for_del, targets = ["No", "Yes"])


def predict_WellType(filepath):

    minerals_for_del1 = ["Mineral35","Mineral37", "Mineral39", "Mineral40", "Mineral41", "Mineral44", "Mineral45"]
    minerals_for_del2 = ["Mineral4","Mineral12","Mineral13","Mineral14","Mineral18","Mineral19",
                        "Mineral29", "Mineral30", "Mineral34","Mineral36", "Mineral38", "Mineral49"]
    
    minerals_for_del = minerals_for_del1 + minerals_for_del2
    return predicting_layout(filepath, "Models/Model_WellType.json", minerals_for_del, targets = ["Standard well", "Drilling"])