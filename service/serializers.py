from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from service.models import Author, Book, Customer


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        exclude = ['created_at', 'updated_at']


class BookListDetailSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='full_name', read_only=True)

    class Meta:
        model = Book
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        exclude = ['created_at', 'updated_at']

    def update(self, instance, validated_data):
        if 'active_books' in validated_data:
            for book in validated_data['active_books']:
                if book not in instance.active_books.all():
                    if book.books_count > 0:
                        book.books_count -= 1
                        book.save()
                    else:
                        raise ValidationError(f'Книги ({book.name}) нет в наличие.')
            for book in instance.active_books.all():
                if book not in validated_data['active_books']:
                    book.books_count += 1
                    book.save()

        return super().update(instance, validated_data)


class CustomerListDetailSerializer(serializers.ModelSerializer):
    active_books = serializers.SlugRelatedField(slug_field='full_name', read_only=True, many=True)

    class Meta:
        model = Customer
        fields = '__all__'
