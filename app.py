from flask import Flask, redirect, url_for, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
import requests
import json

url = 'https://pokeapi.co/api/v2/pokemon?limit=151'

pokeDict = {'bulbasaur': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png',
            'ivysaur': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/2.png',
            'venusaur': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/3.png',
            'charmander': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png',
            'charmeleon': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/5.png',
            'charizard': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/6.png',
            'squirtle': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/7.png',
            'wartortle': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/8.png',
            'blastoise': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/9.png',
            'caterpie': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/10.png',
            'metapod': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/11.png',
            'butterfree': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/12.png',
            'weedle': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/13.png',
            'kakuna': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/14.png',
            'beedrill': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/15.png',
            'pidgey': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/16.png',
            'pidgeotto': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/17.png',
            'pidgeot': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/18.png',
            'rattata': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/19.png',
            'raticate': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/20.png',
            'spearow': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/21.png',
            'fearow': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/22.png',
            'ekans': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/23.png',
            'arbok': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/24.png',
            'pikachu': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png',
            'raichu': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/26.png',
            'sandshrew': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/27.png',
            'sandslash': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/28.png',
            'nidoran-f': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/29.png',
            'nidorina': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/30.png',
            'nidoqueen': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/31.png',
            'nidoran-m': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/32.png',
            'nidorino': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/33.png',
            'nidoking': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/34.png',
            'clefairy': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/35.png',
            'clefable': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/36.png',
            'vulpix': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/37.png',
            'ninetales': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/38.png',
            'jigglypuff': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/39.png',
            'wigglytuff': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/40.png',
            'zubat': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/41.png',
            'golbat': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/42.png',
            'oddish': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/43.png',
            'gloom': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/44.png',
            'vileplume': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/45.png',
            'paras': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/46.png',
            'parasect': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/47.png',
            'venonat': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/48.png',
            'venomoth': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/49.png',
            'diglett': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/50.png',
            'dugtrio': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/51.png',
            'meowth': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/52.png',
            'persian': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/53.png',
            'psyduck': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/54.png',
            'golduck': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/55.png',
            'mankey': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/56.png',
            'primeape': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/57.png',
            'growlithe': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/58.png',
            'arcanine': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/59.png',
            'poliwag': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/60.png',
            'poliwhirl': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/61.png',
            'poliwrath': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/62.png',
            'abra': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/63.png',
            'kadabra': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/64.png',
            'alakazam': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/65.png',
            'machop': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/66.png',
            'machoke': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/67.png',
            'machamp': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/68.png',
            'bellsprout': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/69.png',
            'weepinbell': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/70.png',
            'victreebel': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/71.png',
            'tentacool': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/72.png',
            'tentacruel': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/73.png',
            'geodude': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/74.png',
            'graveler': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/75.png',
            'golem': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/76.png',
            'ponyta': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/77.png',
            'rapidash': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/78.png',
            'slowpoke': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/79.png',
            'slowbro': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/80.png',
            'magnemite': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/81.png',
            'magneton': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/82.png',
            'farfetchd': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/83.png',
            'doduo': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/84.png',
            'dodrio': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/85.png',
            'seel': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/86.png',
            'dewgong': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/87.png',
            'grimer': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/88.png',
            'muk': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/89.png',
            'shellder': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/90.png',
            'cloyster': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/91.png',
            'gastly': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/92.png',
            'haunter': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/93.png',
            'gengar': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/94.png',
            'onix': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/95.png',
            'drowzee': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/96.png',
            'hypno': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/97.png',
            'krabby': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/98.png',
            'kingler': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/99.png',
            'voltorb': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/100.png',
            'electrode': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/101.png',
            'exeggcute': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/102.png',
            'exeggutor': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/103.png',
            'cubone': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/104.png',
            'marowak': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/105.png',
            'hitmonlee': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/106.png',
            'hitmonchan': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/107.png',
            'lickitung': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/108.png',
            'koffing': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/109.png',
            'weezing': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/110.png',
            'rhyhorn': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/111.png',
            'rhydon': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/112.png',
            'chansey': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/113.png',
            'tangela': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/114.png',
            'kangaskhan': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/115.png',
            'horsea': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/116.png',
            'seadra': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/117.png',
            'goldeen': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/118.png',
            'seaking': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/119.png',
            'staryu': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/120.png',
            'starmie': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/121.png',
            'mr-mime': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/122.png',
            'scyther': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/123.png',
            'jynx': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/124.png',
            'electabuzz': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/125.png',
            'magmar': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/126.png',
            'pinsir': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/127.png',
            'tauros': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/128.png',
            'magikarp': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/129.png',
            'gyarados': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/130.png',
            'lapras': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/131.png',
            'ditto': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/132.png',
            'eevee': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/133.png',
            'vaporeon': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/134.png',
            'jolteon': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/135.png',
            'flareon': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/136.png',
            'porygon': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/137.png',
            'omanyte': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/138.png',
            'omastar': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/139.png',
            'kabuto': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/140.png',
            'kabutops': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/141.png',
            'aerodactyl': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/142.png',
            'snorlax': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/143.png',
            'articuno': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/144.png',
            'zapdos': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/145.png',
            'moltres': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/146.png',
            'dratini': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/147.png',
            'dragonair': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/148.png',
            'dragonite': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/149.png',
            'mewtwo': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/150.png',
            'mew': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/151.png'}


def return_poke_list(api_url):
    r = requests.get(api_url)
    result = r.text
    result_json = json.loads(result)

    return result_json['results']


def get_names_sprites():
    # pokdict = return_poke_list(url)
    # for items in pokdict:
    #     req = requests.get(items['url'])
    #     result = req.text
    #     pokeResult_json = json.loads(result)
    #     pokeDict[pokeResult_json['forms'][0]['name']] = pokeResult_json['sprites']['front_default']

    return pokeDict


app = Flask(__name__)


@app.route('/home')
def home():  # put application's code here
    return render_template('home.html', pokemon=get_names_sprites())


@app.route('/signin')
def sign_in():  # put application's code here
    return render_template('signIn.html')


@app.route('/favorites')
def favorites():  # put application's code here
    return render_template('favorites.html')


@app.route('/about')
def about():  # put application's code here
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
