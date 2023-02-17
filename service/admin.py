from django.contrib import admin


from service.models import Author, Book, Customer

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Customer)

