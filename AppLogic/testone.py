import csv
import asyncio
from transformers import GPT2LMHeadModel, GPT2Tokenizer

model = GPT2LMHeadModel.from_pretrained('gpt2')
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

class EmailGenerator:
    def __init__(self):
        self.model = GPT2LMHeadModel.from_pretrained('gpt2')
        self.tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

    def generate_email(self, index):
        # Generate a prompt or context for the email
        prompt = f"This is email number {index}."

        # Tokenize the prompt
        inputs = self.tokenizer.encode(prompt, return_tensors='pt')

        # Generate text using the model
        outputs = self.model.generate(inputs, max_length=200, num_return_sequences=1)

        # Decode the generated text
        generated_email = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        return generated_email

    async def save_email_to_csv(self, index):
        generated_email = self.generate_email(index)

        # Define the filename for the CSV file
        filename = f"email_{index}.csv"

        # Save the email to a CSV file
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Subject', 'Body'])
            writer.writerow(['Generated Email', generated_email])

async def generate_emails():
    email_generator = EmailGenerator()
    tasks = []

    for i in range(1, 1001):
        task = asyncio.create_task(email_generator.save_email_to_csv(i))
        tasks.append(task)

        if i % 10 == 0:
            await asyncio.gather(*tasks)
            tasks = []
            print(f"Generated {i} emails.")

    await asyncio.gather(*tasks)

asyncio.run(generate_emails())
