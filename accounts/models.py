from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=50, blank=True, verbose_name='Страна')
    region = models.CharField(max_length=100, blank=True, verbose_name='Регион')
    city = models.CharField(max_length=100, blank=True, verbose_name='Город/населенный пункт')
    street = models.CharField(max_length=100, blank=True, verbose_name='Улица')
    house_number = models.CharField(max_length=100, blank=True, verbose_name='Номер дома')
    litter_number = models.CharField(max_length=100, verbose_name='Корпус/литера/строение')
    apartments_number = models.CharField(max_length=100, verbose_name='Квартира/помещение')
    floor = models.CharField(max_length=100, verbose_name='Этаж')
    elevator = models.CharField(max_length=100, verbose_name='Наличие лифта')
    intercom = models.CharField(max_length=100, verbose_name='Наличие домофона')
    postal_code = models.CharField(max_length=12, blank=True, verbose_name='Почтовый код')

    def __str__(self):
        return (
            f' {self.country},'
            f' {self.region},'
            f' {self.city},'
            f' {self.street},'
            f' {self.house_number},'
            f' {self.litter_number},'
            f' {self.apartments_number},'
            f' {self.postal_code}'
        )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tel = models.CharField(max_length=11, blank=True, verbose_name='Телефон')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    # country = models.CharField(max_length=50, blank=True, verbose_name='Страна')
    # city = models.CharField(max_length=50, blank=True, verbose_name='Город')
    # street = models.CharField(max_length=50, blank=True, verbose_name='Улица')
    # address = models.CharField(max_length=100, blank=True, verbose_name='Дом/кор., кв./офис')
    # postal_code = models.CharField(max_length=10, blank=True, verbose_name='Почтовый код')
    gender = models.CharField(max_length=50, blank=True, verbose_name='Пол')
    # address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}'

    class Meta:
        verbose_name = 'Личный кабинет'
        verbose_name_plural = 'Личный кабинет'


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def update_profile(sender, instance, **kwargs):
    instance.profile.save()
