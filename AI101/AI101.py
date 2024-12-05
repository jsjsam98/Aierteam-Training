#!/usr/bin/env python
# coding: utf-8

# # AI 101 - Say Hi to AI

# # Welcome to AI 101! 🚀
# 
# This AI 101 notebook will guide you through:
# - Setting up and using OpenAI's API
# - Finish some reading about Large Language Model
# - Write your first promt for Chatgpt
# 
# Let's begin our journey into AI! 🌟
# 

# In[8]:


# setup openai client and api key
from openai import OpenAI
client = OpenAI()

# openai will look for OPENAI_API_KEY in environment variables, you can also set it here, be sure to protect your key.
# client.api_key = "" 


# In[9]:


completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]
)
print(completion.choices[0].message.content)


# In[10]:


# use https post api to call the chat completion
import requests
url = "https://api.openai.com/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {client.api_key}"  # Using the existing client's API key
}
data = {
    "model": "gpt-4o-mini",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]
}
response = requests.post(url, headers=headers, json=data)
result = response.json()
print(result['choices'][0]['message']['content'])


# ### 🤔Heads-up
# **What is an API?**
# 
# API (Application Programming Interface) is a set of rules and protocols that allows
# different software applications to communicate with each other. 
# 
# **Helpful links**
# 
# https://www.geeksforgeeks.org/rest-api-introduction/
# 
# **Why do we need this when we have chatgpt.com?**
# - integrate AI capabilities directly into our applications
# - process multiple requests programmatically
# - customize the model parameters and system prompts
# - build our own user interfaces and experiences
# - take advantage of different models
# 
# **Programming Language we will be using**
# 
# 🐍Python!
# 

# ### 📖Reading Content
# 
# *Why 'Large Language Model'*
# - Large: billions of parameters & trained on immense dataset
# - Language: Understand, process, and generate human-like text
# - Model: Built on the Transformer architecture
# 
# *Large Language Model's position in AI world*
# <pre>
# ----------------------------
# |            AI            |
# |--------------------------|
# ||    Machine Learning    ||
# || ---------------------  ||
# || |   Deep Learning   |  ||
# || |      --------     |  ||
# || |      | LLMs |     |  ||
# || |      --------     |  ||
# || ---------------------  ||
# |--------------------------|
# ----------------------------
# </pre>

# ### 📝Write your first prompt for Chatgpt
# Tell Chatgpt who you are, what you do, and let Chatgpt commnuicate in as a representative of you.
# 

# In[11]:


def chat_as_user(client, user_intro, user_message):
    """
    Function to chat with GPT-4 acting as a representative of the user

    Args:
        client: OpenAI client instance
        user_intro: String containing user's introduction/background
        user_message: Message to send to the model
        
    Returns:
        The model's response text
    """
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"You will act as a representative of the user. Below is the user's introduction. {user_intro}"},
            {"role": "user", "content": user_message}
        ]
    )
    return completion.choices[0].message.content

client = OpenAI()
user_intro = "I am Sarah Chen, a software engineer at a tech startup in San Francisco. I specialize in building AI-powered applications and have 5 years of experience in Python development. I'm passionate about using technology to solve real-world problems."

response = chat_as_user(client, user_intro, "Hello! What is your job?")
print(response)

