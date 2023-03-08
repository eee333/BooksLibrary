from django.contrib import admin


from service.models import Author, Book, Customer


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'created_at')


class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'pages_count', 'books_count', 'created_at')


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'active', 'list_active_books', 'created_at')
    list_filter = ('active',)


admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Customer, CustomerAdmin)

