# scorg-news

Docker Compose:
```version: '3'

services:
  bot:
    image: zeinestone/newsbot:latest
    volumes:
      - ./data:/app/data
    environment:
      - DISCORD_TOKEN=your_token_here
      - OPENAI_TOKEN=your_token_here
      - SOURCE_GUILD_ID=your_guild_id
```