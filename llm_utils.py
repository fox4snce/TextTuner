"""
llm_utils.py - 

Usage:
- Ensure your local OpenAI-like server is running on port 5001
- Import this module and use the provided functions for text and JSON responses
"""

import json
import requests

def generate_response(system=None, user_message=None, max_tokens=4096, temperature=0.8):
    if system is None:
        system = "You are a helpful coding assistant."
    if user_message is None:
        user_message = "You are a helpful assistant."

    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user_message}
    ]

    data = {
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": True
    }

    response = requests.post(
        "http://localhost:5001/v1/chat/completions",
        headers={"Content-Type": "application/json"},
        json=data,
        stream=True
    )

    full_response = ""
    for line in response.iter_lines():
        if line:
            try:
                json_response = json.loads(line.decode('utf-8').split('data: ')[1])
                if 'choices' in json_response and len(json_response['choices']) > 0:
                    content = json_response['choices'][0]['delta'].get('content', '')
                    full_response += content
            except:
                pass

    return full_response

def generate_text_response(system=None, user_message=None, max_tokens=4096, temperature=0.8):
    return generate_response(system, user_message, max_tokens, temperature)

def generate_json_response(system=None, user_message=None, max_tokens=4096, temperature=0.7):
    if system is None:
        system = "You are a helpful assistant. Always respond with valid JSON."
    else:
        system += " Always respond with valid JSON."

    response = generate_response(system, user_message, max_tokens, temperature)

    # Try to extract JSON from code block if it exists
    if '```' in response:
        try:
            json_str = response.split('```')[1]
            if json_str.startswith('json'):
                json_str = json_str[4:]
            json_response = json.loads(json_str.strip())
            return json_response
        except json.JSONDecodeError:
            pass

    # If extraction fails or there's no code block, try parsing the whole response
    try:
        json_response = json.loads(response)
        return json_response
    except json.JSONDecodeError:
        # If JSON parsing fails, return an error message in JSON format
        return json.dumps({"error": "Failed to parse JSON", "raw_response": response})