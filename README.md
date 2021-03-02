# Chatbots with DialogFlow

It has scripts to use chatbots in Telegram or VK. Also you'll find a script to create intent at DialogFlow.

### How to install

* Dowload the code 
* Check that you have Python 3  
* Install requirements:  
```
pip install -r requirements.txt
```
* Create a bot at telegram channel `@BotFather` 

### How to create an agent with DialogFlow 

Before using scripts you should register yourself at Google Cloud. After that: 
- `Create project at DialogFlow` - more info by [link](https://cloud.google.com/dialogflow/es/docs/quick/setup) 
- `Build an agent` - more info my [link](https://cloud.google.com/dialogflow/es/docs/quick/build-agent) 
- `Create training phrases and Response` - you can do it manually or with a script `create_intent` 
- `Crate JSON-key` - more info by [link](https://cloud.google.com/docs/authentication/getting-started) 

### Environment Variables 

Add file `.env` with variables: 
- `TG_BOT_TOKEN` - token of your telegram bot. 
- `VK_TOKEN` - token of your VK bot. 
- `PROJECT_ID` - you can find it as `project_id` in JSON-key 
- `SESSION_ID` - you can find it as `client_id` in JSON-key 
- `GOOGLE_APPLICATION_CREDENTIALS` - path to your file with JSON-key
- `TG_USER_ID` - add id of your telegram account for logs 

### How to use script create_intent 

- Create a file `questions.json` like this:
```
{
    "How to get a job": {
        "questions": [
            "How can I get a job?",
            "I want to work with you",
            "Can I work with you?",
        ],
        "answer": "If you want to work with is, please send your CV to our email."
    }
```
- `python create_intent.py` - script adds questions to your agent

### How to run chatbots

- `python tg_bot.py` 
- `python vk_bot.py` 

### How it works

Telegram

![screenshot](media/tg_bot.gif)

Also you can write for these chatbots:
- `VK` - [write message](https://vk.com/im?media=&sel=-198809484) 
- `Telegram` - you can find a bot by username `DevmanVerbBot`. 
