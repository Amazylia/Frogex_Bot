# importing pandas as pd 
import pandas as pd 
import discord
from discord.ext import commands
from discord import app_commands

# reading csv file 
df = pd.read_csv("data_pocket.csv") 
  
# filtering the rows where Credit-Rating is Fair 
o = df[df['Name'].str.contains('Tritox',na=False)] 
print(o["Name"])
print(o['URL'].iloc[0])
print(len(o))
