from openai import OpenAI
from vault import JsonDB
import json


class MyChatbot:
    def __init__(self):
        self.client = OpenAI()
        self.db = JsonDB()
        self.message_history = []

    def get_password(self, account: str) -> str:
        return self.db.get(account)

    def set_password(self, account: str, password: str) -> None:
        self.db.set(account, password)

    def delete_password(self, account: str) -> None:
        self.db.delete(account)

    def chat(self, prompt: str) -> dict:
        # Initialize token counters
        total_input_tokens = 0
        total_output_tokens = 0

        # Add user message to history
        self.message_history.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that can help me manage my passwords in a database.",
                },
                *self.message_history,  # Include full message history
            ],
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "get_password",
                        "description": "Retrieve a password for a given account",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "account": {
                                    "type": "string",
                                    "description": "The account name to retrieve the password for",
                                }
                            },
                            "required": ["account"],
                            "additionalProperties": False,
                        },
                        "strict": True,
                    },
                },
                {
                    "type": "function",
                    "function": {
                        "name": "set_password",
                        "description": "Set a password for a given account",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "account": {
                                    "type": "string",
                                    "description": "The account name",
                                },
                                "password": {
                                    "type": "string",
                                    "description": "The password to store",
                                },
                            },
                            "required": ["account", "password"],
                            "additionalProperties": False,
                        },
                        "strict": True,
                    },
                },
                {
                    "type": "function",
                    "function": {
                        "name": "delete_password",
                        "description": "Delete a password for a given account",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "account": {
                                    "type": "string",
                                    "description": "The account name to delete the password for",
                                }
                            },
                            "required": ["account"],
                            "additionalProperties": False,
                        },
                        "strict": True,
                    },
                },
            ],
            tool_choice="auto",
            temperature=0,
        )

        total_input_tokens += response.usage.prompt_tokens
        total_output_tokens += response.usage.completion_tokens

        # Add assistant's response to history
        self.message_history.append(
            {
                "role": "assistant",
                "content": response.choices[0].message.content,
                "tool_calls": response.choices[0].message.tool_calls,
            }
        )

        # Handle tool calls
        if response.choices[0].message.tool_calls:
            tool_call = response.choices[0].message.tool_calls[0]
            tool_name = tool_call.function.name
            tool_args = tool_call.function.arguments
            tool_args = json.loads(tool_args)
            if tool_name == "get_password":
                tool_result = self.get_password(tool_args["account"])
            elif tool_name == "set_password":
                self.set_password(tool_args["account"], tool_args["password"])
                tool_result = f"Password set for account: {tool_args['account']}"
            elif tool_name == "delete_password":
                self.delete_password(tool_args["account"])
                tool_result = f"Password deleted for account: {tool_args['account']}"

            # Add tool result to history
            self.message_history.append(
                {
                    "role": "tool",
                    "content": str(tool_result),
                    "tool_call_id": tool_call.id,
                }
            )

            # Get final response based on tool result
            final_response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that can help me manage my passwords in a database.",
                    },
                    *self.message_history,
                ],
                temperature=0,
            )

            total_input_tokens += final_response.usage.prompt_tokens
            total_output_tokens += final_response.usage.completion_tokens

            # Add final response to history
            self.message_history.append(
                {
                    "role": "assistant",
                    "content": final_response.choices[0].message.content,
                }
            )

            return {
                "response": final_response.choices[0].message.content,
                "input_tokens": total_input_tokens,
                "output_tokens": total_output_tokens,
            }

        return {
            "response": response.choices[0].message.content,
            "input_tokens": total_input_tokens,
            "output_tokens": total_output_tokens,
        }


if __name__ == "__main__":
    chatbot = MyChatbot()
    print("Welcome to Password Manager Chat! Type 'quit' to exit.")

    total_input_tokens = 0
    total_output_tokens = 0

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() == "quit":
            print("\nSession ended. Total tokens used:")
            print(f"Input tokens: {total_input_tokens}")
            print(f"Output tokens: {total_output_tokens}")
            break

        if user_input:
            completion = chatbot.chat(user_input)
            print("\nAssistant:", completion["response"])

            total_input_tokens += completion["input_tokens"]
            total_output_tokens += completion["output_tokens"]
