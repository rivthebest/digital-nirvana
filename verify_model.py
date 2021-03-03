import pandas as pd
from pycaret.regression import load_model, predict_model, pull

model_catboost = load_model('Final_CatBoost_Model_06AUG2020')
print("CatBoost Model Loaded")
print("\n")
model_lightgbm = load_model('Final_LightGBM_Model_06AUG2020')
print("LightGBM Model Loaded")

# Loading the holdout dataset
holdout_dataset = pd.read_csv("<your_holdout_dataset.csv>")

dataset_catboost = predict_model(model_catboost, data=holdout_dataset)
print("CatBoost Model Prediction Completed")
print("\n")
dataset_lightgbm = predict_model(model_lightgbm, data=holdout_dataset)
print("LightGBM Model Prediction Completed")

print('\n')
print("Printing Catboost Score Grid")
print("\n")
print(dataset_catboost.describe())
print("\n")
print("Printing LightGBM Score Grid")
print("\n")
print(dataset_lightgbm.describe())