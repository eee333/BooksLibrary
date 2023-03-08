from django.contrib import admin


from service.models import Author, Book, Customer


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'created_at')


class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'pages_count', 'books_count', 'created_at')


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

