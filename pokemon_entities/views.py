import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon, PokemonEntity
from django.utils.timezone import localtime
from django.shortcuts import get_object_or_404


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

    current_time = localtime()

    entities = PokemonEntity.objects.filter(
        appeared_at__lte=current_time,
        disappeared_at__gte=current_time
    )

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
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    current_time = localtime()
    entities = pokemon.entities.filter(
        appeared_at__lte=current_time,
        disappeared_at__gte=current_time
    )

    for entity in entities:
        image_url = DEFAULT_IMAGE_URL
        if pokemon.image:
            image_url = request.build_absolute_uri(pokemon.image.url)

        add_pokemon(
            folium_map,
            entity.lat,
            entity.lon,
            image_url
        )

    previous_evolution = None
    if pokemon.previous_evolution:
        prev = pokemon.previous_evolution
        previous_evolution = {
            'title_ru': prev.title,
            'pokemon_id': prev.id,
            'img_url': request.build_absolute_uri(prev.image.url) if prev.image else None,
        }

    next_evolution = None
    next_evolutions = pokemon.next_evolutions.all()
    if next_evolutions.exists():
        nxt = next_evolutions.first()
        next_evolution = {
            'title_ru': nxt.title,
            'pokemon_id': nxt.id,
            'img_url': request.build_absolute_uri(nxt.image.url) if nxt.image else None,
        }

    pokemon_data = {
        'pokemon_id': pokemon.id,
        'title_ru': pokemon.title,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'img_url': request.build_absolute_uri(pokemon.image.url) if pokemon.image else None,
        'description': pokemon.description,
        'previous_evolution': previous_evolution,
        'next_evolution': next_evolution,
    }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(),
        'pokemon': pokemon_data
    })
