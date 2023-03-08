from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from service.models import Author, Book, Customer


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'created_at')


class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author_link', 'pages_count', 'books_count', 'created_at')

    def author_link(self, obj):
        author = obj.author
        url = reverse('admin:service_author_changelist') + str(author.pk)
        return format_html(f'<a href="{url}">{author}</a>')

    author_link.short_description = 'Автор'


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'active', 'list_active_books', 'created_at')
    list_filter = ('active',)
    actions = ['deactivate', 'activate']

    @admin.action(description='Деактивировать читателей')
    def deactivate(self, request, queryset):
        count = queryset.update(active=False)
        self.message_user(request, f'Изменен статус {count} читателей.')

    @admin.action(description='Активировать читателей')
    def activate(self, request, queryset):
        count = queryset.update(active=True)
        self.message_user(request, f'Изменен статус {count} читателей.')


admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Customer, CustomerAdmin)

