# AI Password Vault 2.0

A secure password management system powered by AI that helps users store and manage their passwords through natural language interactions. This version adds user verification for enhanced security.

## Features

-   Natural language interface for password management
-   Secure password storage in a local JSON database
-   **User verification required for all password operations**
-   Support for basic password operations:
    -   Get password for an account
    -   Set password for an account
    -   Delete password from an account

## Security Enhancements

-   User verification: Before performing any password operations, the chatbot requires and verifies the user's name
-   Access control: Only authenticated users can access or modify stored passwords
-   Secure local storage: Passwords are stored in a local JSON database within a .cache directory

## Components

-   `chatbot.py`: Implements the AI chatbot interface with user verification using OpenAI's GPT-4 model
-   `vault.py`: Handles secure password storage in a JSON database
-   `.cache/db.json`: Local storage for passwords in a protected directory
