import openai
import requests
import base64
import asyncio
import re

# Assuming this is the correct way to import your OpenAI token
from ...config import OPENAI_TOKEN

client = openai.AsyncOpenAI(api_key=OPENAI_TOKEN)

# Function to detect an image URL in text
def find_image_url(text):
    # Regex pattern for URL
    pattern = r'(http[s]?://.*\.(?:png|jpg|jpeg|gif|bmp))'
    urls = re.findall(pattern, text)
    return urls[0] if urls else None

# Function to download and encode the image to base64
async def download_and_encode_image(image_url):
    response = requests.get(image_url)
    response.raise_for_status()
    return base64.b64encode(response.content).decode('utf-8')

async def generate_thread_name(content, embeds, files):
    print(content, embeds, files)
    # Combine text from content, embeds, and files
    embed_text = ' '.join([embed.description for embed in embeds if embed.description]) if embeds else ''
    file_text = ' '.join([file.filename for file in files]) if files else ''
    content_text = content if content else ''
    combined_text = f"{content_text} {embed_text} {file_text}"

    # Check for image URL and process if found
    image_url = find_image_url(combined_text)
    if image_url:
        encoded_image = await download_and_encode_image(image_url)
        combined_text += f" {encoded_image}"

    # Send request to OpenAI API
    response = await client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {"role": "system", "content": "You are a forum power user, and you are creating the perfect post title to summarize the content you receive."},
            {"role": "system", "content": "You will respond only with the perfect title, and nothing else"},
            {"role": "user", "content": combined_text[:2000]},
        ]
    )
    print(response)
    return response.choices[0].message.content

