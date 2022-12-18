from audioop import reverse

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.crypto import get_random_string


def get_name_file(instance, filename):
    return '/'.join([get_random_string(length=5) + '_' + filename])


class User(AbstractUser):
    first_name = models.CharField(max_length=254, verbose_name='Имя', blank=False)
    last_name = models.CharField(max_length=254, verbose_name='Фамилия', blank=False)
    patronymic = models.CharField(max_length=254, verbose_name='Отчество', blank=True)
    username = models.CharField(max_length=254, verbose_name='Логин', unique=True, blank=False)
    email = models.CharField(max_length=254, verbose_name='Почта', unique=True, blank=False)
    password = models.CharField(max_length=254, verbose_name='Пароль', blank=False)
    role = models.CharField(max_length=254, verbose_name='Роль',
                            choices=(('admin', 'Администратор'), ('user', 'Пользователь')), default='user')

    def __str__(self):
        return self.first_name

    USERNAME_FIELD = 'username'


def limited_image(img):
    file_size = img.file.size
    limit = 2.0
    if file_size > limit * 1024 * 1024:
        raise ValidationError("Размер изображения превышает 2MB")


class Application(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in progress', 'Принято в работу'),
        ('done', 'Выполнено')
    ]
    title = models.CharField(max_length=254, verbose_name='Название', blank=False)
    description = models.TextField(max_length=500, verbose_name='Описание', blank=True)
    category = models.ForeignKey('Category', verbose_name='Категория', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=get_name_file,
                              help_text="Максимальный размер изображения 2MB",
                              blank=True,
                              null=True,
                              validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'bmp']),
                                          limited_image],
                              verbose_name='Картинка')
    date = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    status = models.CharField(max_length=254, verbose_name='Статус',
                              choices=STATUS_CHOICES,
                              default='new')
    borrower = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True)
    design = models.ImageField(upload_to=get_name_file,
                               help_text="Максимальный размер изображения 2MB",
                               blank=True,
                               null=True,
                               validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'bmp']),
                                           limited_image],
                               verbose_name='Картинка')
    comment = models.TextField(max_length=500, verbose_name='Комментарий', blank=True)

    def status_verbose(self):
        return dict(self.STATUS_CHOICES)[self.status]

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('application', args=[str(self.id)])


class Category(models.Model):
    title = models.CharField(max_length=254, verbose_name='Название', blank=False)

    def __str__(self):
        return self.title
