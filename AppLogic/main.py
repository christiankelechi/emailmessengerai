import os
import csv
import time
import asyncio
import aiohttp
from aiohttp import ClientSession


class EmailGenerator:
    def __init__(self):
        self.api_key = os.environ.get("API_KEY")
        self.org_id = os.environ.get("ORG_ID")
        self.base_url = "https://api.openai.com/v1/engines/davinci-codex/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        self.prompt = "generate nice soda marketing email newsletters"
        self.total_emails = 1000
        self.timeout = aiohttp.ClientTimeout(total=600)
        self.current_email_count = 0

    async def get_assistant_response(self, session, prompt):
        data = {
            "prompt": prompt,
            "max_tokens": 1000,
        }
        try:
            async with session.post(self.base_url, headers=self.headers, json=data, timeout=self.timeout) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    email = data['choices'][0]['text']
                    await self.save_to_csv(email)
                else:
                    print("Failed to get response, status code:", resp.status)
        except Exception as e:
            print(f"An error occurred: {e}")

    async def save_to_csv(self, email):
        self.current_email_count += 1
        filename = f"message_{self.current_email_count}.csv"
        with open(filename, "w", encoding="UTF-8") as f:
            writer = csv.writer(f, delimiter=",", lineterminator="\n")
            writer.writerow([email])

    async def generate_emails(self):
        tasks = []
        async with ClientSession() as session:
            for i in range(self.total_emails):
                tasks.append(self.get_assistant_response(session, self.prompt))
                await asyncio.sleep(0.04)  # respect rate limit
            await asyncio.gather(*tasks)

    async def run(self):
        start = time.time()
        await self.generate_emails()
        end = time.time()
        print(str((end - start)/60) + "mins")


if __name__ == '__main__':
    generator = EmailGenerator()
    asyncio.run(generator.run())
