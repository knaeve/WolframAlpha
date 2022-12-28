from dotenv import load_dotenv
import urllib.request
import discord
import urllib.parse
import hashlib
import os

load_dotenv('.env')
intents = discord.Intents.all()

key = os.getenv('screenshot')
discordToken = os.getenv('discord')
client = discord.Client(intents=intents)


def generate_screenshot_api_url(key, secret_phrase, options):
  api_url = f'https://api.screenshotmachine.com/?key={key}'
  if secret_phrase:
    api_url = api_url + '&hash=' + hashlib.md5((options.get('url') + secret_phrase).encode('utf-8')).hexdigest()
  api_url = f"{api_url}&{urllib.parse.urlencode(options)}"
  return api_url

secret_phrase = ''


@client.event
async def on_message(message):
    global secret_phrase
    if message.author.bot:
        return

    if message.content.lower().startswith('hello'):
        await message.channel.send(f"Hello {message.author.mention}")

    if message.content.startswith('!wa'):
        query = str(message.content).replace(' ', '')
        print(message.content)
        print(query[3:len(query)])
        options = {
        'url': f'https://www.wolframalpha.com/input?i={query[3:len(query)]}',
        'dimension': '1024x768', 
        'device' : 'desktop',
        'cacheLimit' : '0',
        'delay' : '2000',
        'zoom' : '100'
        }

        api_url = generate_screenshot_api_url(key, secret_phrase, options)

        try:
          path = r'C:\Users\Asus\wolfy\results'
          os.chdir(path)
        except OSError:
          print(f"Unable to change path {os.getcwd()}")

        print(f'<img src="{api_url}>')        
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', '-')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(api_url, 'res.png')

        with open(r'C:\Users\Asus\wolfy\results\res.png', 'rb') as f:
            res = discord.File(f)
    
        await message.channel.send(file=res)
client.run(discordToken)
