import nltk
from nltk.tokenize import word_tokenize
import spacy

# Download NLTK tokenizer models if not already downloaded
nltk.download('punkt')

# Knowledge base with FAQs and answers about engineering
knowledge_base = {
    "What is engineering?": "Engineering is the application of science and mathematics to solve problems by designing and building structures, machines, and systems.",
    "What are the main branches of engineering?": "The main branches of engineering include Mechanical, Electrical, Civil, Chemical, and Computer Engineering, among others.",
    "What skills are important for future engineers?": "Important skills for future engineers include proficiency in programming, knowledge of emerging technologies, problem-solving, and adaptability to new tools and methods.",
    "How to become an engineer?": "To become an engineer, you generally need to complete a bachelor's degree in engineering, followed by internships or practical experience in the field. Some regions may also require passing professional exams to obtain a license.",
    "What subjects should we take after 10th class?": "After 10th class, students aiming to become engineers should focus on subjects such as Mathematics, Physics, and Chemistry. Additionally, pursuing a science stream with these subjects in higher secondary education is important for engineering aspirants.",
}

# Load the SpaCy model
nlp = spacy.load("en_core_web_sm")

def tokenize_input(input_text):
    try:
        # Use NLTK for tokenization
        tokens = word_tokenize(input_text)
    except LookupError:
        # Fallback to SpaCy if NLTK fails, without printing any message
        doc = nlp(input_text)
        tokens = [token.text for token in doc]
    return tokens

def identify_entities(input_text):
    doc = nlp(input_text)
    entities = [(entity.text, entity.label_) for entity in doc.ents]
    return entities

def identify_intent(input_text, entities):
    lower_text = input_text.lower()
    
    if "engineering" in lower_text and "branch" in lower_text:
        return "branches_info"
    elif "engineering" in lower_text:
        return "engineering_info"
    elif "skills" in lower_text and "engineers" in lower_text:
        return "skills_info"
    elif "become" in lower_text and "engineer" in lower_text:
        return "become_engineer"
    elif "subjects" in lower_text and "10th" in lower_text:
        return "subjects_after_10th"
    else:
        return "unknown"

def generate_response(intent, knowledge_base):
    if intent == "engineering_info":
        return knowledge_base["What is engineering?"]
    elif intent == "branches_info":
        return knowledge_base["What are the main branches of engineering?"]
    elif intent == "skills_info":
        return knowledge_base["What skills are important for future engineers?"]
    elif intent == "become_engineer":
        return knowledge_base["How to become an engineer?"]
    elif intent == "subjects_after_10th":
        return knowledge_base["What subjects should we take after 10th class?"]
    else:
        return "I'm not sure I understand your question. Can you please rephrase?"

def chatbot():
    # Start the conversation
    print("Hello! I can answer your questions about engineering.")
    
    while True:
        # Ask a question to the user
        user_input = input("Ask me a question or type 'exit' to end: ")
        
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        
        # Process the user input and generate a response
        tokens = tokenize_input(user_input)
        entities = identify_entities(user_input)
        intent = identify_intent(user_input, entities)
        response = generate_response(intent, knowledge_base)
        
        # Print the chatbot's response
        print(f"Answer: {response}\n")

# Run the chatbot
chatbot()
