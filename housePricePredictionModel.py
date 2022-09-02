from sklearn.model_selection import train_test_split, GridSearchCV,cross_val_score
from sklearn.metrics import r2_score
import pandas as pd
import xgboost as xgb
from xgboost import XGBRegressor

df = pd.read_csv("emlak_verisi_son.csv")
df.drop("Sehir", axis = 1, inplace = True)
df.drop("Mahalle", axis = 1, inplace = True)
df.dropna(inplace = True)

df = df[["İlce","Fiyat","brüt metrekare","Net Metrekare","Oda Sayısı","Binanın Yaşı","Bulunduğu Kat"]]

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

#colsample_bytree 0.5
#learning_rate 0.02
#max_depth 5
#n_estimators 100

xgb1 = XGBRegressor(colsample_bytree = 0.5, 
                    learning_rate = 0.02, 
                    max_depth = 5, 
                    n_estimators = 100)
                
model_xgb = xgb1.fit(X_train, y_train)




