from django.contrib.auth.models import AbstractUser
from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=20, verbose_name='Имя')
    last_name = models.CharField(max_length=20, verbose_name='Фамилия')
    foto = models.ImageField(upload_to='authors/', blank=True, verbose_name='Фото')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Book(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(max_length=2000, verbose_name='Описание')
    pages_count = models.PositiveIntegerField(verbose_name='Количество страниц')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    books_count = models.PositiveIntegerField(verbose_name='Количество книг в библиотеке')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    @property
    def full_name(self):
        return f'{self.name} ({self.author.full_name})'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'


class Customer(AbstractUser):
    phone = models.CharField(max_length=16, unique=True, verbose_name='Телефон')
    active_books = models.ManyToManyField(Book, blank=True, null=True, verbose_name='Активные книги')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def list_active_books(self):
        return ', '.join([book.name for book in self.active_books.all()])

    list_active_books.short_description = 'Активные книги'

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Читатель'
        verbose_name_plural = 'Читатели'
