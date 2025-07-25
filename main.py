from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
from typing import Literal
import pandas as pd
 
ml=joblib.load("food_model.pkl")
label=joblib.load("label_encoders.pkl")

class inp_data(BaseModel):
    mood:Literal["happy","sad","neutral","angry","tired","energetic","stressed","bored","excited"]
    time_of_day:Literal["breakfast", "lunch", "dinner","evening"]
    is_hungry:Literal[0,1]
    prefers_spicy:int
    diet:Literal["veg", "vegan","non-veg"]
app=FastAPI()

@app.get('/')
def root_msg():
        return {"message": "Welcome"}
@app.post('/predict')
def predict(data: inp_data):
    inputs=pd.DataFrame([data.dict()])
    encode_columns = ["mood","time_of_day","diet","food_prediction"]
    for col in encode_columns:
        inputs[col] = label[col].transform(inputs[col])
    res=ml.predict(inputs)
    prd=label["food_prediction"].inverse_transform([res])[0]

    return {"Predicted_food":prd}

    