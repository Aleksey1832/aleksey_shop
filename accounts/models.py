import random
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,  # При удалении пользователя, удалять и его профиль
        related_name='profile',  # Имя для обратной связи с User (user.profile)
        verbose_name='Пользователь'
    )
    phone_number = models.CharField(max_length=15, blank=True, verbose_name='Телефон')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    gender = models.CharField(max_length=50, blank=True, verbose_name='Пол')

    def __str__(self):
        return f'{self.user.username}'

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'


class Address(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,  # При удалении профиля, удалять и его адреса
        related_name='addresses',  # Имя для обратной связи с Profile (profile.addresses.all())
        verbose_name='Профиль'
    )
    country = models.CharField(max_length=50, verbose_name='Страна')
    region = models.CharField(max_length=100, verbose_name='Регион')
    city = models.CharField(max_length=100, verbose_name='Город/населенный пункт')
    street = models.CharField(max_length=100, verbose_name='Улица/Проспект')
    house_number = models.CharField(max_length=100, verbose_name='Номер дома')
    litter_number = models.CharField(max_length=100, blank=True, verbose_name='Корпус/литера/строение')
    apartments_number = models.CharField(max_length=100, blank=True, verbose_name='Квартира/помещение')
    floor = models.CharField(max_length=100, blank=True, verbose_name='Этаж')
    elevator = models.BooleanField(null=True, blank=True, default=False, verbose_name='Наличие лифта')
    intercom = models.BooleanField(null=True, blank=True, default=False, verbose_name='Наличие домофона')
    postal_code = models.CharField(max_length=12, blank=True, verbose_name='Почтовый код')

    def __str__(self):
        parts = []
        if self.country:
            parts.append(f'{self.country.capitalize()}')
        if self.region:
            parts.append(f'рег.: {self.region.capitalize()}')
        if self.city:
            parts.append(f'г./нп.: {self.city.capitalize()}')
        if self.street:
            parts.append(f'ул./пр.: {self.street.capitalize()}')
        if self.house_number:
            parts.append(f'д.: {self.house_number}')
        if self.litter_number:
            parts.append(f'корп./лит.: {self.litter_number.capitalize()}')
        if self.apartments_number:
            parts.append(f'кв./офис: {self.apartments_number}')
        if self.postal_code:
            parts.append(f'индекс: {self.postal_code}')
        return ', '.join(parts)

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'
        unique_together = ('profile', 'country', 'region', 'city', 'street', 'house_number',
                           'litter_number', 'apartments_number', 'postal_code')


class EmailVerificationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=5, verbose_name='Код подтверждения')
    created_at = models.DateTimeField(auto_now_add=True)  # время создания кода двух факторной аутентификации

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=3)

    @staticmethod
    def expiry_time():
        return timezone.now() + timezone.timedelta(seconds=180)

    @staticmethod
    def generate_code():
        return str(random.randint(10000, 99999))

    def __str__(self):
        return f'{self.code}'


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def update_profile(sender, instance, **kwargs):
    instance.profile.save()
