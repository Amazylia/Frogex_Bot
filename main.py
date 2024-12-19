import discord
from discord.ext import commands
from discord import app_commands
import random
import os
from dotenv import load_dotenv
from urllib.request import urlopen
from bs4 import BeautifulSoup
import html
import requests
import pandas as pd 
from paginator import Paginator
import asyncio

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
intents.message_content = True
intents.members = True

with open('token.txt') as f:
    TOKEN = f.readline()

currencies=["$","USD","usd","€","💲","PHP"]

tours="https://play.limitlesstcg.com/tournaments/upcoming?game=POCKET&format=all&platform=all&type=online"

df = pd.read_csv("data_pocket.csv") 

def eachInASeparateLine(A):
    yourList = A
    butFirst = yourList[0:]
    EachInASeparateLine = "\n".join(butFirst)
    return(EachInASeparateLine)

def url(a):
    string=str(a)
    return(string[string.find("href")+7:string.find('details')+7])

def date(name):
    page=urlopen(tours)
    bs=BeautifulSoup(page.read(),'lxml')
    da=bs.find('tr',{'data-name':name})
    children=str(da.findChildren("td",{"class":"date"}))
    return (str(children[children.find('data-time')+11:children.find('href')-5]))

def tour():
    page = urlopen(tours)
    bs=BeautifulSoup(page.read(),'lxml')
    toursList=bs.find_all('td',{"class" : 'name'})
    A=[]
    for name in toursList:
        if any(substring in name.get_text() for substring in currencies):
            k=name.get_text()
            lou=date(k)
            A.append("[**"+str(k)+"**](https://play.limitlesstcg.com/"+str(url(name))+")"+"  -  <t:"+str(lou)+">")
            A.append("")
    return(eachInASeparateLine(A))

def pages(nom):
    o = df[df['Name'].str.contains(nom,na=False)] 
    PAGES=[]
    for i in range(0,len(o)):
        embed=discord.Embed(title=nom)
        embed.set_image(url=(o['URL'].iloc[i]))
        PAGES.append(embed)
    return(PAGES)

@tree.command(
    name="tournois",
    description="Liste des tournois à venir",
    guild=discord.Object(id=803694121637380136)
)
async def Tournois(interaction):
    await interaction.response.defer()
    embed=discord.Embed(title="Tournois Limitless", url=tours, description=tour(),)
    await interaction.followup.send(embed=embed)

@tree.command(
    name="carte",
    description="Montre les différentes versions d'une carte",
    guild=discord.Object(id=803694121637380136)
)
async def carte(interaction: discord.Interaction, nom:str ):
    o = df[df['Name'].str.contains(nom,na=False)]
    buttons = [u"\u23EA",u"\u25C0",u"\u25B6",u"\u23E9"]
    current = 0
    page=pages(nom)
    print(page)
    await interaction.response.send_message(embed=page[current])
    message: discord.Message
    async for message in interaction.channel.history():
        if not message.embeds:
            continue
        if message.embeds[0].title == page[current].title and message.embeds[0].colour == page[current].colour:
            break
    else:
        # something broke
        return

    for button in buttons:
        await message.add_reaction(button)

    while True:
        try:
            reaction, user = await client.wait_for("reaction_add", check=lambda reaction, user: user == interaction.user and reaction.emoji in buttons, timeout=60.0)
        except asyncio.TimeoutError:
            embed=page[current]
            embed.set_footer(text="Timed Out.")
            await message.clear_reactions()
        
        else:
            previous_page=current

            if reaction.emoji==u"\u23EA":
                current = 0

            elif reaction.emoji==u"\u25C0":
                if current>0:
                    current-=1
                else:
                    current=len(page)-1
            
            elif reaction.emoji==u"\u25B6":
                if current< len(page):
                    current+=1
                else:
                    current=0
            
            elif reaction.emoji==u"\u23E9":
                current=len(page)-1

            for button in buttons:
                await message.remove_reaction(button,interaction.user)

            if current != previous_page:
                await message.edit (embed=page[current])

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    msg=message.content.lower()
    if 'frogex' in msg:
        await message.channel.send(':frog:')

@client.event
async def on_member_join(member):
    Welcome = ["Bienvenue, " + member.mention + "! J'espère que tu sautes de joie d'être ici ! 🐸",
"Salut" + member.mention + "! Tu viens de plonger dans notre serveur, prépare-toi à nager dans une mer de fun ! 🐸🌊",
"Ribbit !" + member.mention + "vient de sauter dans le serveur. Bienvenue dans notre marécage ! 🐸",
"Bienvenue, " + member.mention + " ! On espère que tu n'es pas un prince charmant, mais tu es toujours bienvenu ici ! 🐸👑",
"Oh là là, un nouveau membre ! Bienvenue " + member.mention + ", on espère que tu es prêt à sauter dans l'aventure avec nous ! 🐸",
"Ribbit ! " + member.mention + " a atterri dans notre serveur. Prépare-toi à passer un moment amphibien ! 🐸",
"Coucou " + member.mention + " ! Si tu as sauté ici, c'est que tu as trouvé ton nouveau marais ! Bienvenue à bord ! 🐸",
"Bienvenue " + member.mention + " ! Maintenant que tu es là, on espère que tu vas bien sauter dans l'action avec nous ! 🐸"]
    logs_channel = client.get_channel(1316856914071654474) #join-logs channel
    print(member.name+" Joined")
    await logs_channel.send(random.choice(Welcome))

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=803694121637380136))
    print("Ready!")

client.run(TOKEN)