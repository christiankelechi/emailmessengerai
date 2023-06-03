import os
import csv
from openai import OpenAI, ChatCompletion
from random import randint


def init_api():
    with open(".env") as env:
        for line in env:
            key,value=line.strip().split("=")
            os.environ[key]=value

    openai.api_key=os.environ.get("API_KEY")
    openai.organization=os.environ.get("ORG_ID")

init_api()

start_message = {
  'role': 'system',
  'content': 'You are a helpful assistant.'
}

messages = [
    start_message,
    {"role": "user", "content": 'Write a unique message of 150 words.'},
]

folder_path = "path_to_your_folder"

for i in range(1000):
    chat = openai.ChatCompletion.create(
      model="text-davinci-002",
      messages=messages
    )
    message = chat['choices'][0]['message']['content']

    # Creating unique filename
    unique_id = randint(100000, 999999)
    filename = f"message_{unique_id}.csv"

    # Write message into csv file
    with open(os.path.join(folder_path, filename), 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["message"])
        writer.writerow([message])
    print(f"Generated file: {filename}")
