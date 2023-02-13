from django.db import models


class Lessons(models.Model):
    LIGHT = 1
    OPTIMAL = 2
    FULL = 3
    access_levels = (
        (LIGHT, 'Лайт'),
        (OPTIMAL, 'Оптимальный'),
        (FULL, 'Полный'),
    )
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=1000, blank=True, null=True)
    access_level = models.SmallIntegerField(choices=access_levels)
    video_file = models.FileField(upload_to='files', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Уроки'
