from django.db import models

# Create your models here.


class Weather(models.Model):
    date = models.CharField(max_length=20, verbose_name='日期')
    weather = models.CharField(max_length=20, verbose_name='天气')
    temperature_h = models.CharField(max_length=10,
                                     verbose_name='最高气温', null=True)
    temperature_l = models.CharField(max_length=10, verbose_name='最低气温', null=True)

    class Meta:
        verbose_name = '天气预报'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{0}({1})".format(self.date, self.weather)
