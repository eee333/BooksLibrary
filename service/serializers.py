from rest_framework import serializers

from service.models import Author, Book, Customer


class PhoneValidator:
    def __call__(self, value):
        if value < 70000000000 or value > 79999999999:
            raise  serializers.ValidationError('Номер телефона должен содеожать 11 цифр и начинаться с 7')


class PageCountValidator:
    def __call__(self, value):
        if value <= 0:
            raise serializers.ValidationError('Количество страниц не может быть меньше 1')


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    pages_count = serializers.IntegerField(validators=[PageCountValidator()])

    class Meta:
        model = Book
        exclude = ['created_at', 'updated_at']


class BookListDetailSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='full_name', read_only=True)

    class Meta:
        model = Book
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    phone = serializers.IntegerField(validators=[PhoneValidator()])

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
                        raise serializers.ValidationError(f'Книги ({book.name}) нет в наличие.')
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
