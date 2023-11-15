import openai
from ...config import OPENAI_TOKEN

openai.api_key = OPENAI_TOKEN

async def generate_thread_name(content, embeds, files):
    print(content, embeds, files)
    if embeds:
        embed_text = ' '.join([embed.description for embed in embeds if embed.description])
    else:
        embed_text = ''
    if files:
        file_text = ' '.join([file.filename for file in files])
    else:
        file_text = ''
    if content:
        content_text = content
    else:
        content_text = ''
    combined_text = f"{content_text} {embed_text} {file_text}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a forum power user, and you are creating the perfect post title to summarize the content you receive."},
            {"role": "system", "content": "You will respond only with the perfect title, and nothing else"},
            {"role": "user", "content": combined_text[0:2000]},
        ]
    )
    return(response['choices'][0]['message']['content'])
