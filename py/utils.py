import sys
import os
import requests
import json

def load_api_key():
    config_file_path = os.path.join(os.path.expanduser("~"), ".config/openai.token")
    api_key = os.getenv("OPENAI_API_KEY")
    try:
        with open(config_file_path, 'r') as file:
            api_key = file.read()
    except Exception:
        pass
    return api_key.strip()

def make_options():
    return vim.eval("options")

def make_request_options():
    options = make_options()
    request_options = {}
    request_options['model'] = options['model']
    request_options['max_tokens'] = int(options['max_tokens'])
    request_options['temperature'] = float(options['temperature'])
    request_options['request_timeout'] = float(options['request_timeout'])
    return request_options

def render_text_chunks(chunks):
    generating_text = False
    for text in chunks:
        if not text.strip() and not generating_text:
            continue # trim newlines from the beginning
        generating_text = True
        vim.command("normal! a" + text)
        vim.command("redraw")

def parse_chat_messages(chat_content):
    lines = chat_content.splitlines()
    messages = []
    for line in lines:
        if line.startswith(">>> system"):
            messages.append({"role": "system", "content": ""})
            continue
        if line.startswith(">>> user"):
            messages.append({"role": "user", "content": ""})
            continue
        if line.startswith("<<< assistant"):
            messages.append({"role": "assistant", "content": ""})
            continue
        if not messages:
            continue
        messages[-1]["content"] += "\n" + line

    for message in messages:
        # strip newlines from the content as it causes empty responses
        message["content"] = message["content"].strip()

    return messages


def gpt_chat(chat_content):

    url = "https://chatbot.theb.ai/api/chat-process"

    headers = {
            "Connection": "keep-alive",
            "sec-ch-ua": '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "sec-ch-ua-mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "sec-ch-ua-platform": '"Windows"',
            "Origin": "https://chatbot.theb.ai",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://chatbot.theb.ai/",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    }

    data = {"prompt":"sample code for use python to decode a json content"}


    response = requests.post(url, headers=headers, json=data)

    line = response.text.splitlines()[-1]
    data = json.loads(line)
    return data['text']
