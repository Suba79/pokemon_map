from django.db import models

class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, blank=True, verbose_name='Имя (англ.)')
    title_jp = models.CharField(max_length=200, blank=True, verbose_name='Имя (яп.)')
    image = models.ImageField(upload_to='pokemon_images', null=True, blank=True)
    description = models.TextField(blank=True, verbose_name='Описание')
    
    def __str__(self):
        return self.title

class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='entities')
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(null=True, blank=True, verbose_name='Время появления')
    disappeared_at = models.DateTimeField(null=True, blank=True, verbose_name='Время исчезновения')
    level = models.IntegerField(null=True, blank=True, verbose_name='Уровень')
    health = models.IntegerField(null=True, blank=True, verbose_name='Здоровье')
    strength = models.IntegerField(null=True, blank=True, verbose_name='Атака')
    defence = models.IntegerField(null=True, blank=True, verbose_name='Защита')
    stamina = models.IntegerField(null=True, blank=True, verbose_name='Выносливость')
