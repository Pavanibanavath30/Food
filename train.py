import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier 
from sklearn.preprocessing import LabelEncoder
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['second_project']
collection = db['second']
data = list(collection.find({},{"_id":0}))
df=pd.DataFrame(data)
"""df=pd.read_csv("food_dataset.csv")
rec=df.to_dict(orient='records')
collection.insert_many(rec)"""
label_encoders = {}
encode_columns = ["mood","time_of_day","diet","food_prediction"]
for col in encode_columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le
X = df.drop("food_prediction", axis=1) 
y = df["food_prediction"]
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(random_state=42)
model.fit(x_train, y_train)

joblib.dump(model, "food_model.pkl")
joblib.dump(label_encoders, "label_encoders.pkl")