from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
from gensim.models import Word2Vec
import numpy as np
import re

# Load the trained Word2Vec model
word2vec_model = Word2Vec.load("./models/word2vec_model.model")

# Load the trained XGBoost model
xgb_model = joblib.load("./models/XGBoost_model.joblib")


# Define the preprocessing function
def preprocess_entity_name(entity_name):
    # Lowercasing
    entity_name = entity_name.lower()
    # Remove punctuation and special characters
    entity_name = re.sub(r'[^\w\s]', '', entity_name)

    return entity_name


# Define a function to average word vectors for a given text
def average_word_vectors(words, model, vocabulary, num_features):
    feature_vector = np.zeros((num_features,), dtype="float64")
    n_words = 0
    for word in words:
        if word in vocabulary:
            n_words += 1
            feature_vector = np.add(feature_vector, model.wv[word])
    if n_words:
        feature_vector = np.divide(feature_vector, n_words)
    return feature_vector


# Function to get average word vectors for new input
def get_avg_feature_vectors_new_input(input_data, model, num_features):
    vocabulary = set(model.wv.index_to_key)
    avg_feature_vectors = [average_word_vectors(tokens, model, vocabulary, num_features) for tokens in input_data]
    return np.array(avg_feature_vectors)


# Function to predict using the trained XGBoost model
def predict_similarity(entity_1, entity_2, word2vec_model, xgb_model):
    # Preprocess entities
    entity_1 = preprocess_entity_name(entity_1)
    entity_2 = preprocess_entity_name(entity_2)

    # Tokenize the input data
    input_data = [sentence.split() for sentence in [entity_1 + ' ' + entity_2]]

    # Get average word vectors for the new input
    input_w2v = get_avg_feature_vectors_new_input(input_data, word2vec_model, 100)

    # Make predictions using the trained XGBoost model
    predictions = xgb_model.predict(input_w2v)

    return predictions


# Pydantic model for request body
class PredictionInput(BaseModel):
    entity_1: str
    entity_2: str


# Define the FastAPI app
app = FastAPI()


# Route to handle predictions
@app.post("/predict")
def predict_similarity_endpoint(data: PredictionInput):
    try:
        entity_1 = data.entity_1
        entity_2 = data.entity_2

        # Make predictions
        predictions = predict_similarity(entity_1, entity_2, word2vec_model, xgb_model)

        return {"entity_1": entity_1, "entity_2": entity_2, "prediction": int(predictions[0])}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
