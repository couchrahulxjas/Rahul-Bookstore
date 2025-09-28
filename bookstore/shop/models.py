from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True)
    cover = models.ImageField(upload_to='book_covers/', blank=True, null=True)

    def __str__(self):
        return self.title


class CartItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    session_key = models.CharField(max_length=40)  # identify cart by session

    def __str__(self):
        return f"{self.book.title} (x{self.quantity})"


class Order(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    items = models.TextField()  # store as simple text (book list + qty)
    total = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"Order #{self.id} - {self.name}"
