import nltk
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
import pandas as pd
import requests

api_key = 'AIzaSyDCgN6Fov5oXr44zsf65IPqhM9A2eOyQEA'
search_engine_id = 'chatbotgoogling'
nltk.download('punkt')

# Function to tokenize text
def tokenize(text):
    tokens = nltk.word_tokenize(text.lower())
    stems = [stemmer.stem(token) for token in tokens]
    return stems

# Function to perform a Google Custom Search
def google_search(query):
    url = f'https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={search_engine_id}'
    response = requests.get(url)
    data = response.json()

    print("Full API Response:", data)  # Add this line for debugging
    
    if 'items' in data:
        return data['items'][0]['snippet']  # Extracting the snippet from the first result
    else:
        return "I couldn't find relevant information for your query."


# Load the dataset of labeled user inputs and their corresponding responses
data = pd.read_csv("chatbot_dataset.csv")

# Append additional interactions to the dataset
additional_interactions = [
    "Can you tell me a joke?", "Sure, here's one: Why did the scarecrow win an award? Because he was outstanding in his field!",
    "Don't feel sad", "I'm here for you. Sometimes a good laugh or a chat with a friend can help brighten your mood.",
    "Search for Python programming tutorials", "Let me find some Python programming tutorials for you.",
    "Find information about space exploration", "Sure, I'll look up information about space exploration for you.",
    "Suggest a good book to read", "I can help with that. Let me find a recommendation for you."
]

additional_data = pd.DataFrame({"User input": additional_interactions[::2], "Bot response": additional_interactions[1::2]})
data = pd.concat([data, additional_data], ignore_index=True)

# Tokenize user input and perform stemming
stemmer = PorterStemmer()

# Create bag-of-words representation of user input
vectorizer = TfidfVectorizer(tokenizer=tokenize, stop_words="english")

# Train an SVM classifier on the labeled dataset
X_train = vectorizer.fit_transform(data["User input"])
y_train = data["Bot response"]
clf = SVC(kernel="linear")
clf.fit(X_train, y_train)

# Start the chatbot
print("Bot: Hi there! How can I assist you today?")

while True:
    user_input = input("User: ")

    # If the user asks for a search, perform a Google search
    if "search" in user_input.lower() and "search for" in user_input.lower():
        query = user_input.split("search for", 1)[1].strip()
        response = google_search(query)
    else:
        # Create bag-of-words representation of user input
        X_test = vectorizer.transform([user_input])

        # Predict the bot's response using the trained SVM classifier
        response = clf.predict(X_test)[0]

    print("Bot:", response)
