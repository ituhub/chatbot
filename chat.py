import streamlit as st
import random
import re

# Initialize Streamlit app
st.set_page_config(page_title="Cleverbit Chatbot", layout="wide")

# Default theme configuration (user can customize)
if 'theme_config' not in st.session_state:
    st.session_state['theme_config'] = {
        'font_size': '16px',
        'background_color': '#FFFFFF',
        'text_color_user': '#000000',
        'text_color_bot': '#007bff',
        'theme': 'light'
    }

# Sidebar customization options
st.sidebar.title("Customize Chat")

# Theme switcher (light or dark mode)
theme = st.sidebar.selectbox("Choose Theme", ["light", "dark"], index=0)
if theme == "dark":
    st.session_state['theme_config']['background_color'] = '#333333'
    st.session_state['theme_config']['text_color_user'] = '#FFFFFF'
    st.session_state['theme_config']['text_color_bot'] = '#4CAF50'
else:
    st.session_state['theme_config']['background_color'] = '#FFFFFF'
    st.session_state['theme_config']['text_color_user'] = '#000000'
    st.session_state['theme_config']['text_color_bot'] = '#007bff'

# Font size customization
font_size = st.sidebar.slider("Font Size", 10, 30, 16)
st.session_state['theme_config']['font_size'] = f"{font_size}px"

# Chat background color customization
bg_color = st.sidebar.color_picker(
    "Choose Background Color", value=st.session_state['theme_config']['background_color'])
st.session_state['theme_config']['background_color'] = bg_color

# User and Bot text color customization
user_text_color = st.sidebar.color_picker(
    "Choose User Text Color", value=st.session_state['theme_config']['text_color_user'])
st.session_state['theme_config']['text_color_user'] = user_text_color

bot_text_color = st.sidebar.color_picker(
    "Choose Bot Text Color", value=st.session_state['theme_config']['text_color_bot'])
st.session_state['theme_config']['text_color_bot'] = bot_text_color

# Title and Layout
st.title("🤖 Cleverbit Software Assistant")
st.markdown("Welcome to the **Cleverbit Chatbot**. How can we help you today?")

# Custom CSS to apply the selected customizations
custom_css = f"""
    <style>
        .reportview-container {{
            background-color: {st.session_state['theme_config']['background_color']};
        }}
        .chat-message-user {{
            color: {st.session_state['theme_config']['text_color_user']};
            font-size: {st.session_state['theme_config']['font_size']};
            text-align: right;
        }}
        .chat-message-bot {{
            color: {st.session_state['theme_config']['text_color_bot']};
            font-size: {st.session_state['theme_config']['font_size']};
            text-align: left;
        }}
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Chat history
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Knowledge Base
company_knowledge_base = {
    "greeting": [
        "Hello! How can Cleverbit Software assist you today?",
        "Hi there! What can I help you with?"
    ],
    "farewell": [
        "Goodbye! Feel free to reach out if you need anything.",
        "Take care! We're always here to assist."
    ],
    "services": [
        "Cleverbit Software offers Custom Software Development, Business Intelligence, Business Automation, and Tech-for-Business Consultancy.",
        "We provide software development, business intelligence, automation, and technology consulting services tailored to your business needs."
    ],
    "business_intelligence": [
        "Our Business Intelligence solutions provide real-time dashboards, automated reporting, and AI-driven insights to help you make smarter business decisions.",
        "Cleverbit specializes in BI to help businesses optimize their data analysis and reporting."
    ],
    "business_automation": [
        "We streamline operations by automating manual tasks and integrating your systems, boosting productivity and reducing costs.",
        "Cleverbit helps businesses automate workflows and eliminate time-consuming processes."
    ],
    "tech_consultancy": [
        "We provide expert technology consulting to help you choose the best solutions for your business.",
        "Our consultancy services include advising on technology stacks, software development, and business process optimization."
    ],
    "managed_development": [
        "Cleverbit offers managed software development services, ensuring the end-to-end delivery of projects with scalable solutions.",
        "We handle everything from building products from scratch to modernizing outdated systems."
    ],
    "technologies": [
        "We use a robust tech stack, including .NET, Azure, React, Angular, Cosmos DB, and Power BI.",
        "Our technology solutions cover Microsoft 365, SharePoint, Azure services, and more."
    ],
    "contact": [
        "You can reach us at contact@cleverbit.com or call us at +44 204 538 9855.",
        "Feel free to contact Cleverbit via email at contact@cleverbit.com or by phone at +44 204 538 9855."
    ],
    "principles": [
        "Cleverbit's core principles are Understanding Client Needs, Ethical Business Practices, and Transparency.",
        "We believe in being focused, transparent, and ethical in all our business interactions."
    ],
    "location": [
        "We are headquartered in the EU but serve clients worldwide, including the UK, US, and Malta.",
        "Cleverbit operates globally, with teams based across the EU, UK, and other regions."
    ],
    "team": [
        "Our team consists of highly skilled professionals with expertise in software development, business intelligence, and automation.",
        "Cleverbit has a team of over 70 skilled employees located across the EU, UK, and US."
    ],
    "unknown": [
        "I'm not sure how to respond to that. Can you please rephrase?",
        "I didn't quite understand that. Could you ask in a different way?"
    ]
}

# Helper Functions


def preprocess(text):
    """Tokenize input and remove punctuation"""
    text = re.sub(r'[^\w\s]', '', text.lower())
    return text.split()


def get_intent(tokens):
    """Identify intent based on user input using regex patterns"""
    text = ' '.join(tokens)
    intent_patterns = {
        'greeting': r'\b(hi|hello|hey|greetings)\b',
        'farewell': r'\b(bye|goodbye|see\s+you|farewell)\b',
        'services': r'\b(service|offer|provide)\b',
        'business_intelligence': r'\b(business intelligence|bi|data|analytics|reporting|dashboard)\b',
        'business_automation': r'\b(business automation|automation|streamline|process)\b',
        'tech_consultancy': r'\b(tech|consultancy|consult|advice)\b',
        'managed_development': r'\b(managed|development|software|product)\b',
        'technologies': r'\b(tech|technology|stack|use|work with)\b',
        'location': r'\b(where|location|based|country)\b',
        'team': r'\b(team|employee|staff|people)\b',
        'principles': r'\b(principle|value|approach|methodology)\b',
        'contact': r'\b(contact|email|phone|call|reach)\b'
    }

    for intent, pattern in intent_patterns.items():
        if re.search(pattern, text, re.IGNORECASE):
            return intent
    return 'unknown'


def generate_response(intent):
    """Generate a response based on intent"""
    if intent in company_knowledge_base:
        return random.choice(company_knowledge_base[intent])
    else:
        return random.choice(company_knowledge_base['unknown'])


# Chat columns
col1, col2 = st.columns([3, 1])

# User input in Streamlit
with col1:
    st.markdown("### Chat Here:")
    user_input = st.text_input("You:", key="input")

    # Process the input and generate a response
    if user_input:
        tokens = preprocess(user_input)
        intent = get_intent(tokens)
        response = generate_response(intent)

        # Append to chat history
        st.session_state['chat_history'].append(
            f"<p class='chat-message-user'>You: {user_input}</p>")
        st.session_state['chat_history'].append(
            f"<p class='chat-message-bot'>Bot: {response}</p>")

    # Display chat history
    st.markdown("### Conversation History:")
    for message in st.session_state['chat_history']:
        st.markdown(message, unsafe_allow_html=True)

# Clear chat button
if col2.button("Clear Chat"):
    st.session_state['chat_history'] = []

# Additional features in sidebar (like theme switching, if needed)
st.sidebar.markdown("### Options")
st.sidebar.write("Feel free to customize or reset the chat.")
