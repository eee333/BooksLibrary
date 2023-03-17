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
        exclude = ['date_joined', 'updated_at']

    def update(self, instance, validated_data):
        if 'active_books' in validated_data:
            if len(validated_data['active_books']) <= 3:  # пользователь может брать не больше трех книг

                # Уменьшаем количество книг в библиотеке
                book_list = []
                for book in validated_data['active_books']:
                    if book not in instance.active_books.all():
                        if book.books_count > 0:
                            book_list.append(book)
                        else:
                            raise serializers.ValidationError(f'Книги ({book.name}) нет в наличие.')
                for book in book_list:  # Сохраняем количество книг, только если каждая из них есть в наличие
                    book.books_count -= 1
                    book.save()

                # Увеличиваем количество книг в библиотеке
                for book in instance.active_books.all():
                    if book not in validated_data['active_books']:
                        book.books_count += 1
                        book.save()
            else:
                raise serializers.ValidationError('Читатель не может взять больше 3 книг')

        if 'password' in validated_data:
            customer = super().update(instance, validated_data)
            customer.set_password(customer.password)
            customer.save()

            return customer

        return super().update(instance, validated_data)

    def create(self, validated_data):
        if 'active_books' in validated_data:
            if len(validated_data['active_books']) <= 3:  # пользователь может брать не больше трех книг

                # Уменьшаем количество книг в библиотеке
                book_list = []
                for book in validated_data['active_books']:
                    if book.books_count > 0:
                        book_list.append(book)
                    else:
                        raise serializers.ValidationError(f'Книги ({book.name}) нет в наличие.')

                for book in book_list:  # Сохраняем количество книг, только если каждая из них есть в наличие
                    book.books_count -= 1
                    book.save()

            else:
                raise serializers.ValidationError('Читатель не может взять больше 3 книг')

        customer = super().create(validated_data)
        customer.set_password(customer.password)
        customer.save()

        return customer


class CustomerListDetailSerializer(serializers.ModelSerializer):
    active_books = serializers.SlugRelatedField(slug_field='full_name', read_only=True, many=True)

    class Meta:
        model = Customer
        fields = '__all__'
