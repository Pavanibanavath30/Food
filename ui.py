import streamlit as st
import pymongo
import requests

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['Food_prediction']
collection = db['users']

st.title(" Food Predictor😋 ")
select=st.sidebar.selectbox("Page Navigator",["Registration Page","Prediction Page"])

if(select=="Registration Page"):
    st.header("New Registration ")
    un=st.text_input("Enter your username")
    pw=st.text_input("Enter your password: ",type="password")
    bn=st.button("Register")
    if bn:
        if un!="" and pw!="":
            collection.insert_one({
                            "username":un,
                            "password":pw})
            st.success("Registration is success")
        else:
            st.error("Enter the proper username and password")
elif(select=="Prediction Page"):
    st.header("Login")
    un=st.text_input("Username: ")
    pw=st.text_input("Password: ",type="password")
    if un!="" and pw!="":
        if(collection.find_one({"username":un,"password":pw}) is not None):
            st.markdown("-------------")
            st.header(f"Hi {un} Predict your food preference")
            mood=st.selectbox("mood:",["happy","sad","neutral","angry","tired","energetic","stressed","bored","excited"])
            time_of_day=st.selectbox(" time_of_day",["breakfast", "lunch", "dinner","evening"])
            diet=st.selectbox("Choose your diet",["veg", "vegan","non-veg"])
            is_hungry=st.checkbox("Are you hungry?")
            ps=st.checkbox("Prefer Spicy! ")
            if(st.button("Predict the food")):
                  data={
                      "mood":mood,
                    "time_of_day":time_of_day,
                    "is_hungry":is_hungry,
                    "prefers_spicy":ps,
                    "diet":diet
                    }
                  res=requests.post("http://127.0.0.1:8000/predict",json=data)
                  result=res.json()
                  st.write("Predicted Food : ",result["Predicted_food"])