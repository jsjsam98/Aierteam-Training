# AI Password Vault

A secure password management system powered by AI that helps users store and manage their passwords through natural language interactions.

## Features

-   Natural language interface for password management
-   Secure password storage in a local JSON database
-   Support for basic password operations:
    -   Get password for an account
    -   Set password for an account
    -   Delete password from an account

## Components

-   `chatbot.py`: Implements the AI chatbot interface using OpenAI's GPT-4 model
-   `vault.py`: Handles secure password storage in a JSON database
-   `.cache/db.json`: Local storage for encrypted passwords
