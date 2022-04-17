from django.db import models
from django.urls import reverse
import uuid
# Create your models here.

class Genre(models.Model):

    #Name of genre
    name = models.CharField(max_length=50)

    #Method for returning the string that represents the object.
    def __str__(self) -> str:
        return self.name


class Language(models.Model):

    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name

#The model for a book in the library        
class Book(models.Model):

    title = models.CharField(max_length=150)
    # You must use the name of the model as a string if the associated class has not yet been defined in this file before it is referenced!
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(null=False, help_text="Enter a description of the book")
    isbn = models.CharField('ISBN',max_length=13, unique=True, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    

    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        """Returns the URL to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])


#Instance of a type of book, each instance can have a different status, and a differnt language, and has a unique id for each instance.
class BookInstance(models.Model):

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique id for the book across the whole library")
    due_back = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=LOAN_STATUS, default='m', help_text="Book availability")
    book = models.ForeignKey('Book', on_delete=models.RESTRICT)
    language = models.ForeignKey(Language, on_delete=models.RESTRICT)

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.book.title})'
    

class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'
    