from rest_framework import serializers

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
        fields = '__all__'
