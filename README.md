# scorg-news

### Zeinestone's NewsBot

This is a fairly simple discord bot. With announcement channels generally being text channels, it can be very annoying to follow those while allowing people to interact with the content. 

## Setup Receiving Servers (for the default instance of this bot)
- Install the bot: https://discord.com/api/oauth2/authorize?client_id=1145773015318155316&permissions=103079266304&scope=bot%20applications.commands
- Create a forum channel
- ```/test_access``` will create a test post in the channel to make sure the bot ("News Bot" Role) can see and post properly
- ```/subscribe``` and select the desired forum channel - if the bot does not have the appropriate accesses, it will let you know
- Select from the dropdown the desired source channel to subscribe to

## List of Commands:
- ```/subscribe```
  - Channel: Must be a 'forum' channel type
  - Subscription: A list of available channels to subscribe to
- ```/unsubscribe```
  - Channel: Must be a 'forum' channel type
  - Subscription: A list of channels which that channel is subscribed to
- ```/view_subscriptions```
  - A list of all subscriptions currently enjoyed by your server
- ```/test_access```
  - Channel: Must be a 'forum' channel type
  - Will create a test post in the forum channel

## Setup A Distributing Server
Important: This is only if you want to set up your own ecosystem. If you are a regular server owner that just wants to get updates from the bot, you DO NOT need to do this. These instructions are generally written for Ubuntu 20+, they should work across most operation systems. However, be aware that the setup for the prerequisites is your responsibility, and I am not going to help you troubleshoot why Docker isn't working. If you don't know how to read docs and set up the prerequisites, you probably shouldn't be trying to do this. 

## Prerequisites
- Linux Server
- Docker
- Docker Compose
- Discord Bot / Token (Message Intents)
- OpenAI API Token
- Guild ID for your source guild
- YouTube Developer API

## Setup Discord Application
- Set up the following permissions for your Receiver Server Install Link
  - bot
    - Send Messages
    - Create Public Threads
    - Create Private Threads
    - Send Messages in Threads
    - Embed Links
    - Attach Files
  - applications.commands
- Set up the following permissions for your Distributor Server Install Link
  - bot
    - Administrator
  - applications.commands
- Set up Message Content Intent (Bot)

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
      - DATABASE_SOURCE=/app/data/subscriptions.db
      - YOUTUBE_API_KEY=<Insert your YOUTUBE API KEY HERE>
      - SECRET_SOURCE=/app/data/
    restart: unless-stopped
```
2. Create a 'data' directory in the same folder you have your docker-compose. This directory will store the subscriptions.db SQLite database, ensuring data persistence across container rebuilds or restarts.
```mkdir data```
3. Install the bot in your source server: https://discord.com/api/oauth2/authorize?client_id=<*INSERT YOUR BOTS CLIENT ID HERE*>&permissions=377957141520&scope=bot%20applications.commands
4. Start the Docker Container
```docker-compose up```

## Distribute the Bot
You will need to create your own installation link based on https://discord.com/api/oauth2/authorize?client_id=<*INSERT YOUR BOTS CLIENT ID HERE*>&permissions=103079266304&scope=bot%20applications.commands

## Update the Bot
- ```sudo docker-compose down && sudo docker-compose pull && sudo docker-compose up```