import os
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import classification_report
import joblib


def train_model(csv_path, result_model_path, cv = 10, seed=0):
    
    df = pd.read_csv(csv_path)
    
    X = df.loc[:,df.columns != "quality"]
    y = df["quality"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=seed)

    mdl = Pipeline([("sc", StandardScaler()), ("lr", LogisticRegression(max_iter=1000, penalty="l2"))])

    param_grid = {"lr__C": np.arange(0.001, 0.1, 0.001)}

    rs = RandomizedSearchCV(estimator=mdl,
                        param_distributions=param_grid,
                        cv=cv,
                        n_iter=90,
                        scoring="accuracy")

    rs.fit(X_train, y_train)    
    joblib.dump(value=rs, filename=open(result_model_path, "wb"))
    
    return(True)

def make_prediction(model_path, input_df):
    
    model = joblib.load(model_path)
    prediction = model.predict(input_df)
    
    return(prediction)
    