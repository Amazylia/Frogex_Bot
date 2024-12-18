import discord
from discord import app_commands
from discord.ext import commands
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError
import os
import html
import requests

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

with open('token.txt') as f:
    TOKEN = f.readline()

currencies=["$","USD","usd","€","💲","PHP"]

tours="https://play.limitlesstcg.com/tournaments/upcoming?game=POCKET&format=all&platform=all&type=online"

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

@tree.command(
    name="tournois",
    description="Liste des tournois à venir",
    guild=discord.Object(id=803694121637380136)
)
async def Tournois(interaction):
    await interaction.response.defer()
    embed=discord.Embed(title="Tournois Limitless", url=tours, description=tour())
    await interaction.followup.send(embed=embed)

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=803694121637380136))
    print("Ready!")

client.run(TOKEN)