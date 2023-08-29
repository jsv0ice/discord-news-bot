# scorg-news

### Zeinestone's NewsBot

This is a fairly simple discord bot. With announcement channels generally being text channels, it can be very annoying to follow those while allowing people to interact with the content. 

## Prerequisites
- Docker
- Docker Compose
- Discord Bot / Token (Message Intents)
- OpenAI API Token
- Guild ID for your source guild

## Setup Server
- Create a channel category called 'subscriptions'
- Create at least one channel to serve as your source

## Setup Bot
1. Create docker-compose.yml
```version: '3'

services:
  bot:
    image: zeinestone/newsbot:latest
    volumes:
      - ./data:/app/data
    environment:
      - DISCORD_TOKEN=<Insert your Discord Bot Token>
      - OPENAI_TOKEN=<Insert your OpenAI API Key>
      - SOURCE_GUILD_ID=<Insert the Source GUILD ID>
      - DB_STRING=/app/data/subscriptions.db
```
2. Create a 'data' directory in the same folder you have your docker-compose. This directory will store the subscriptions.db SQLite database, ensuring data persistence across container rebuilds or restarts.
```mkdir data```
3. Install the bot in your source server: https://discord.com/api/oauth2/authorize?client_id=1145773015318155316&permissions=377957141520&scope=bot%20applications.commands
4. Start the Docker Container
```docker-compose up```

## Setup Receiving Servers
- Install the bot: https://discord.com/api/oauth2/authorize?client_id=1145773015318155316&permissions=377957138432&scope=bot%20applications.commands
- Create a forum channel
- Use the command:
```/subscribe``` and select the desired forum channel
- Select from the dropdown the desired source channel to subscribe to
- Give the Role 'News Bot' access to view and post to the channel if necessary

## Update the Bot
- ```docker-compose down```
- ```docker-compose pull```
- ```docker-compose up```