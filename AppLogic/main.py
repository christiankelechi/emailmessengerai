import os
import csv
import time
import openai
import string

class EmailGenerator:
    def __init__(self):
        self.init_api()
        self.translate_table = str.maketrans('aeiou', 'pzwbz')

    def init_api(self):
        with open(".env") as env:
            for line in env:
                key, value = line.strip().split("=")
                os.environ[key] = value

        openai.api_key = os.environ.get("API_KEY")
        openai.organization_id = os.environ.get("ORG_ID")

    def generate_email(self, prompt):
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            temperature=1.5,
            max_tokens=300
        )
        return response.choices[0].text.strip()

    def vowel_swapper(self, text):
        return text.translate(self.translate_table)

class EmailManager:
    def __init__(self, generator):
        self.generator = generator

    def generate_emails(self, number: int, prompt: str):
        for i in range(number):
            self.generate_and_save_email(i+1, prompt)
        
    def generate_and_save_email(self, index, prompt):
        email = self.generator.generate_email(prompt)
        self.save_to_csv(email, index, 'emails')
        print(f'Generated {index} emails so far')
        
        swapped_email = self.generator.vowel_swapper(email)
        self.save_to_csv(swapped_email, index, 'swappedfolder')
        print(f'Swapped vowels in {index} emails so far')

    def save_to_csv(self, email, index, folder):
        if not os.path.exists(folder):
            os.makedirs(folder)
        with open(f"{folder}/email_{index}.csv","w",encoding='UTF-8') as f:
            writer = csv.writer(f, delimiter=",", lineterminator="\n")
            writer.writerow([email])

start = time.time()

generator = EmailGenerator()
manager = EmailManager(generator)
manager.generate_emails(1000, 'generate a soda marketing email')

end = time.time()
print(f'Total time: {(end - start)/60} minutes')
