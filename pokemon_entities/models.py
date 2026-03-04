from django.db import models

class Pokemon(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Имя (рус.)'  # добавил verbose_name
    )
    title_en = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Имя (англ.)'
    )
    title_jp = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Имя (яп.)'
    )
    image = models.ImageField(
        upload_to='pokemon_images',
        null=True,
        blank=True,
        verbose_name='Изображение'  # добавил verbose_name
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    previous_evolution = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='next_evolutions',
        verbose_name='Из кого эволюционировал'
    )
    
    def __str__(self):
        return self.title

    class Meta:  # добавил Meta класс
        verbose_name = 'Покемон'
        verbose_name_plural = 'Покемоны'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        related_name='entities',
        verbose_name='Покемон'  # добавил verbose_name
    )
    lat = models.FloatField(
        verbose_name='Широта'
    )
    lon = models.FloatField(
        verbose_name='Долгота'
    )
    appeared_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Время появления'
    )
    disappeared_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Время исчезновения'
    )
    level = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Уровень'
    )
    health = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Здоровье'
    )
    strength = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Атака'
    )
    defence = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Защита'
    )
    stamina = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Выносливость'
    )

    def __str__(self):
        return f'{self.pokemon.title} (уровень {self.level})' if self.level else self.pokemon.title

    class Meta:  # добавил Meta класс
        verbose_name = 'Сущность покемона'
        verbose_name_plural = 'Сущности покемонов'