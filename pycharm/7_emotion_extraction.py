from transformers import AutoModelForSequenceClassification, AutoTokenizer
import numpy as np
from scipy.special import softmax
import pandas as pd

def preprocess(text):
    """
    Preprocesses the text by replacing user mentions and URLs.

    Args:
        text (str): The input text.

    Returns:
        str: The preprocessed text.
    """
    new_text = []
    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)

def predict_emotions(df):
    """
    Predicts the emotions for lyrics in the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing the lyrics.

    Returns:
        pd.DataFrame: The DataFrame with added emotion predictions and scores.
    """
    task = 'emotion'
    MODEL = f"cardiffnlp/twitter-roberta-base-{task}"

    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)

    labels = ['anger', 'joy', 'optimism', 'sadness']

    emotions = []
    scores_list = []

    for lyrics in df['lyrics']:
        # Preprocess lyrics
        lyrics = preprocess(lyrics)

        # Encode lyrics
        encoded_input = tokenizer.encode_plus(
            lyrics,
            max_length=512,
            truncation=True,
            padding="max_length",
            return_tensors='pt'
        )

        # Make prediction
        output = model(**encoded_input)
        scores = output.logits[0].detach().numpy()
        scores = softmax(scores)

        # Store emotion label and scores
        dominant_emotion_index = np.argmax(scores)
        dominant_emotion = labels[dominant_emotion_index]
        emotions.append(dominant_emotion)
        scores_list.append(scores)

    # Create columns for each emotion with scores
    scores_array = np.array(scores_list)
    for i, label in enumerate(labels):
        df[label] = scores_array[:, i]

    df['emotion'] = emotions
    return df

def lambda_handler(event, context):
    # Read the CSV file into a DataFrame
    df = pd.read_csv('cleaned_lyrics (1).csv')

    # Predict emotions for lyrics
    df = predict_emotions(df)

    print(df.head(10))

    # Save the dataframe to a CSV file
    csv_buffer = df.to_csv(index=False)

    # Upload the CSV file to S3
    csv_key = 'lyrics_emotions.csv'

    # Save the DataFrame to a local CSV file
    df.to_csv('lyrics_emotions.csv', index=False)

    print("CSV file saved to 'lyrics_emotions.csv'")

if __name__ == "__main__":
    lambda_handler(None, None)
