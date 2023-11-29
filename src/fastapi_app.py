# Import necessary libraries
import re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib


# Sample input data format
class Item(BaseModel):
    entity_name_1: str
    entity_name_2: str

    # Helper function for preprocessing the entities
    def preprocess_entity_name(entity_name):
        # Lowercasing
        entity_name = entity_name.lower()
        # Remove punctuation and special characters
        entity_name = re.sub(r'[^\w\s]', '', entity_name)

        return entity_name


app = FastAPI()

# # Define a placeholder for the model
# model = None

# # Load the pre-trained model
# model = joblib.load("../models/trained_model.joblib")

# # Load the TF-IDF vectorizer
# vectorizer = TfidfVectorizer()
# vectorizer.fit(pd.read_csv("data/features.csv")['processed_entity_names'])


# API endpoint to predict entity name similarity
@app.post("/predict")
async def predict(item: Item):
    # # Ensure that the model is loaded before making predictions
    # if model is None:
    #     raise HTTPException(status_code=500, detail="Model not loaded")

    # Preprocess input data
    processed_entity_name_1 = Item.preprocess_entity_name(entity_name=item.entity_name_1)
    processed_entity_name_2 = Item.preprocess_entity_name(entity_name=item.entity_name_2)
    processed_entity_names = processed_entity_name_1 + ' ' + processed_entity_name_2

    # # Transform the input using the TF-IDF vectorizer
    # features = vectorizer.transform([processed_entity_names])

    # # Make prediction using the loaded model
    # prediction = model.predict(features)[0]

    # return {"entity_similarity": prediction}
    return {"entity_similarity": processed_entity_names}
