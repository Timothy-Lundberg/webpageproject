from jokeapi import Jokes # Import the Jokes class
import asyncio
from pprint import pprint

async def print_joke():
    j = await Jokes()  # Initialise the class
    joke = await j.get_joke(category=["Pun"], search_string="man")  # Programming, Misc, Dark, Pun, Spooky, Christmas
    #pprint(joke)
    if joke["type"] == "single": # Print the joke
        return joke["joke"]
    else:
        return joke["setup"]
        return joke["delivery"]




# Vi vill ha en knapp där man kan "generera" joke sen ska det klistras in i ett textfält som man ska kunna redigera
# Vi vill kunna välja mottagare