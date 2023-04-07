import nltk
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
import pandas as pd
nltk.download('punkt')

# Load the dataset of labeled user inputs and their corresponding responses
data = pd.read_csv("chatbot_dataset.csv")

# Tokenize user input and perform stemming
stemmer = PorterStemmer()


def tokenize(text):
    tokens = nltk.word_tokenize(text.lower())
    stems = [stemmer.stem(token) for token in tokens]
    return stems


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

    # Create bag-of-words representation of user input
    X_test = vectorizer.transform([user_input])

    # Predict the bot's response using the trained SVM classifier
    response = clf.predict(X_test)[0]

    print("Bot:", response)
