import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()
    
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    
    entities = PokemonEntity.objects.all()
    for entity in entities:
        image_url = DEFAULT_IMAGE_URL
        if entity.pokemon.image:
            image_url = request.build_absolute_uri(entity.pokemon.image.url)
        
        add_pokemon(
            folium_map,
            entity.lat,
            entity.lon,
            image_url
        )
    
    pokemons_on_page = []
    for pokemon in pokemons:
        image_url = None
        if pokemon.image:
            image_url = request.build_absolute_uri(pokemon.image.url)
        
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': image_url,
            'title_ru': pokemon.title,
        })
    
    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    return HttpResponseNotFound('<h1>Страница в разработке</h1>')