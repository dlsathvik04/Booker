from django.contrib import admin

from books.models import Book, Rating, ReviewReaction, Wishlist

# Register your models here.
admin.site.register(Book)
admin.site.register(Rating)
admin.site.register(ReviewReaction)
admin.site.register(Wishlist)