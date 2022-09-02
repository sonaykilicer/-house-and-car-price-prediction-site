from sklearn.model_selection import train_test_split, GridSearchCV,cross_val_score
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
from sklearn.metrics import r2_score
import xgboost as xgb
import numpy
from xgboost import XGBRegressor

df = pd.read_csv("son_hali_araba.csv")

df.drop("Unnamed: 0", axis = 1, inplace = True)
df.drop("Model", axis = 1, inplace = True)

X = df.drop(["Fiyat"], axis = 1)
y = df["Fiyat"] 

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 144)

params = {"colsample_bytree":[0.4,0.5,0.6],
          "learning_rate":[0.01,0.02,0.09],
          "max_depth":[2,3,4,5,6],
          "n_estimators":[100,200,500,2000]}

#xgb = XGBRegressor()
#grid = GridSearchCV(xgb, params, cv = 10, n_jobs = -1, verbose = 2)
#grid.fit(X_train, y_train)

#colsample_bytree 0.4
#learning_rate 0.02
#max_depth 5
#n_estimators 2000
        
xgb1 = XGBRegressor(colsample_bytree = 0.4, 
                    learning_rate = 0.02, 
                    max_depth = 5, 
                    n_estimators = 2000)
                
model_xgb = xgb1.fit(X_train, y_train)
