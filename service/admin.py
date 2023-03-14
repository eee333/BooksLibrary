from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from service.models import Author, Book, Customer


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'created_at')


class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author_link', 'pages_count', 'books_count', 'created_at')
    actions = ['set_zero',]

    def author_link(self, obj):
        author = obj.author
        url = reverse('admin:service_author_changelist') + str(author.pk)
        return format_html(f'<a href="{url}">{author}</a>')

    author_link.short_description = 'Автор'

    @admin.action(description='Установить наличие в 0')
    def set_zero(self, request, queryset):
        count = queryset.update(books_count=0)
        self.message_user(request, f'Изменено наличие {count} книг.')


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'is_active', 'list_active_books', 'date_joined')
    list_filter = ('is_active',)
    actions = ['deactivate', 'activate', 'del_books']

    @admin.action(description='Деактивировать читателей')
    def deactivate(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f'Изменен статус {count} читателей.')

    @admin.action(description='Активировать читателей')
    def activate(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f'Изменен статус {count} читателей.')

    @admin.action(description='Удалить все книги')
    def del_books(self, request, queryset):
        count = 0
        for obj in queryset:
            for book in obj.active_books.all():  # Увеличиваем наличие книг в библиотеке
                book.books_count += 1
                book.save()
            obj.active_books.clear()
            count += 1
        self.message_user(request, f'Удалены книги у {count} читателей.')


admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Customer, CustomerAdmin)

