from __future__ import annotations
from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse, NoReverseMatch

class Menu(models.Model):
    name = models.CharField('Системное имя', max_length=50, unique=True)
    title = models.CharField('Название (для админки)', max_length=100, blank=True)

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

    def __str__(self) -> str:
        return self.title or self.name

class MenuItem(models.Model):
    menu = models.ForeignKey('Menu', on_delete=models.CASCADE, related_name='items', verbose_name='Меню')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name='Родитель')
    title = models.CharField('Текст', max_length=100)
    named_url = models.CharField('Имя URL (reverse)', max_length=200, blank=True, help_text='Например: home. Без аргументов.')
    url = models.CharField('URL (если без имени)', max_length=255, blank=True, help_text='Абсолютный или относительный путь.')
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'
        ordering = ['parent__id', 'order', 'title']

    def __str__(self) -> str:
        return self.title

    def clean(self) -> None:
        if self.parent and self.parent.menu_id != self.menu_id:
            raise ValidationError('Родитель должен быть из того же меню.')
        if not self.named_url and not self.url:
            raise ValidationError('Заполните либо "Имя URL", либо "URL".')

    def get_url(self) -> str:
        # Сначала пробуем имя, иначе берём url как есть.
        if self.named_url:
            try:
                return reverse(self.named_url)
            except NoReverseMatch:
                pass
        return self.url or '#'
