# Field
An attribute within a Model class used to track a characteristic of the data.

## Definition: CharField
A string.
```python
name = models.CharField(max_length=255)
```

## Definition: TextField
A long string.
```python
quote = models.TextField()
```
## ForeignKey
One-to-Many.
```python
class BookQuote(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='quotes')
```

### Workflow: Implement One-to-Many
1. Add `models.ForeignKey(Book)`.
2. Add `on_delete` and `related_name`.
    ```python
    class Book(models.Model):
        name = models.CharField(max_length=255)

    class BookQuote(models.Model):
        book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='quotes')
    ```
3. Access data:
    - from `BookQuote`:
        ```python
        quote = BookQuote.objects.get(id=1)
        parent_book = quote.book
        ```
    - from `Book`:
        ```python
        book = Book.objects.get(id=1)
        all_quotes = book.quotes.all()
        ```
4. Save data:
    ```python
    new_quote = BookQuote(content="To be or not to be", book=book_instance)
    new_quote.save()
    ```

## ManyToManyField
A field used to create a relationship where multiple records in one table can be associated with multiple records in another table.


### Workflow: Many-to-Many
1. Add `models.ManyToManyField(Author)`.
2. Add `related_name`.
    ```python
    class Author(models.Model):
        name = models.CharField(max_length=255)

    class Book(models.Model):
        title = models.CharField(max_length=255)
        authors = models.ManyToManyField(Author, related_name='books')
    ```
3. Access data:
    - from `Book`:
        ```python
        book = Book.objects.get(id=1)
        book_authors = book.authors.all()
        book.authors.add(author_instance)
        ```
    - from `Author`:
        ```python
        author = Author.objects.get(id=1)
        author_books = author.books.all()
4. Save data:
    ```python
    book.authors.add(author_instance)
    book.authors.set([author1, author2])
    ```


