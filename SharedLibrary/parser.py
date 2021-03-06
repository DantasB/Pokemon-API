import asyncio

from Objects import *
from scrapy import Selector

from SharedLibrary import utils

def get_each_stat(pokemon, data):
    """ Parses the stats information and adds it to the pokemon

    Args:
        pokemon (Pokemon): pokemon that will receive the information
        data (string): the string that contains the stats information
    """
    if("Sp." in data[0]):
        pokemon.set_base_stats(data[0] + data[1], data[2])
        pokemon.set_max_stats(data[0] + data[1], data[4])
        return
    
    pokemon.set_base_stats(data[0], data[1])
    pokemon.set_max_stats(data[0], data[3])

def get_extra_informations(pokemon, html_content):
    """ Fill the remaining pokemon informations located in the html_content

    Args:
        pokemon (Pokemon): pokemon that will receive the data
        html_content (string): html related to this pokemon
    """
    html_document = Selector(text=html_content)
    get_pokemon_weight(pokemon, html_document.xpath("/html/body/main/div[3]/div[2]/div/div[1]/div[2]/table/tbody/tr[5]/td").extract_first())
    get_pokemon_base_stats(pokemon, html_document.xpath("/html/body/main/div[3]/div[2]/div/div[2]/div[1]/div[2]/table/tbody/tr").extract())
    get_pokemon_pokedex_entries(pokemon, html_document.xpath("/html/body/main/div[8]/table/tbody/tr").extract())
    get_pokemon_species(pokemon, html_document.xpath("/html/body/main/div[3]/div[2]/div/div[1]/div[2]/table/tbody/tr[3]/td").extract_first())
    get_pokemon_local_numbers(pokemon, html_document.xpath("/html/body/main/div[3]/div[2]/div/div[1]/div[2]/table/tbody/tr[7]/td").extract_first())

def get_pokemon_weight(pokemon, information):
    """ Parses the weight information and adds it to the pokemon

    Args:
        pokemon (Pokemon): pokemon that will receive the information
        information (string): the string that contains the weight information
    """
    if information is None:
        return   
    weight = utils.remove_html_tags(information).strip()
    pokemon.set_weight(weight)

def get_pokemon_base_stats(pokemon, informations):
    """ Parses the base_stats information and adds it to the pokemon

    Args:
        pokemon (Pokemon): pokemon that will receive the information
        informations (list): list of pokemon base_stats
    """
    for information in informations:
        information = utils.remove_all_line_breakers(utils.remove_html_tags(information)).strip().split(' ')
        get_each_stat(pokemon, information)

def get_pokemon_pokedex_entries(pokemon, informations):
    """ Parses the pokedex_entries information and adds it to the pokemon

    Args:
        pokemon (Pokemon): pokemon that will receive the information
        informations (list): list of pokemon pokedex_entries
    """
    for information in informations:
        splitted_information = information.split("</span>")

        text = utils.remove_html_tags(splitted_information[-1]).strip()

        if len(splitted_information) == 2:
            pokemon.set_pokedex_entries(utils.remove_html_tags(splitted_information[0]).strip(), text)
            continue

        games = splitted_information[:len(splitted_information)-1]
        for game in games:
            pokemon.set_pokedex_entries(utils.remove_html_tags(game).strip(), text)

def get_pokemon_species(pokemon, information):
    """ Parses the pokemon_species information and adds it to the pokemon

    Args:
        pokemon (Pokemon): pokemon that will receive the information
        information (list): pokemon pokemon_species
    """
    if information is None:
        return   
    species = utils.remove_html_tags(information).strip()
    pokemon.set_species(species)

def get_pokemon_local_numbers(pokemon, informations):
    """ Parses the pokemon_local_numbers information and adds it to the pokemon

    Args:
        pokemon (Pokemon): pokemon that will receive the information
        informations (list): list of pokemon pokemon_local_numbers
    """
    informations = utils.remove_html_tags(informations)
    if(informations is None):
        return
    informations = informations.strip().split(')')
    informations = informations[:len(informations)-1]
    for information in informations:
        information = information.split('(')
        pokemon.set_local_numbers(information[1].strip(), information[0].strip())