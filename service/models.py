from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=20, verbose_name='Имя')
    last_name = models.CharField(max_length=20, verbose_name='Фамилия')
    foto = models.ImageField(upload_to='authors/', blank=True, verbose_name='Фото')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Book(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(max_length=2000, verbose_name='Описание')
    pages_count = models.PositiveIntegerField(verbose_name='Количество страниц')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    books_count = models.PositiveIntegerField(verbose_name='Количество книг в библиотеке')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'


class Customer(models.Model):
    first_name = models.CharField(max_length=20, verbose_name='Имя')
    last_name = models.CharField(max_length=20, verbose_name='Фамилия')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    active = models.BooleanField(default=True)
    active_books = models.ManyToManyField(Book, blank=True, null=True, verbose_name='Активные книги')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name)

    class Meta:
        verbose_name = 'Читатель'
        verbose_name_plural = 'Читатели'
