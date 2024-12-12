from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField(default="No description available.\n\n")
    cover_image = models.ImageField(upload_to="book_covers/", default="book_covers/default.png")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(sum(rating.rating_overall for rating in ratings) / ratings.count(),1)
        return 0

    def average_language_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(sum(rating.rating_language for rating in ratings) / ratings.count(),1)
        return 0

    def average_children_friendly_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(
                sum(rating.rating_children_friendly for rating in ratings)
                / ratings.count()
            , 1)
        return 0

    def average_clarity_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(sum(rating.rating_clarity for rating in ratings) / ratings.count(),1)
        return 0


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name="ratings", on_delete=models.CASCADE)
    rating_overall = models.FloatField()
    rating_language = models.FloatField()
    rating_children_friendly = models.FloatField()
    rating_clarity = models.FloatField()
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "book")

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

    def get_reaction_counts(self):
        upvotes = self.reactions.filter(reaction="upvote").count()
        downvotes = self.reactions.filter(reaction="downvote").count()
        return upvotes, downvotes
    
    def get_upvotes(self):
        return self.reactions.filter(reaction="upvote").count()
    
    def get_downvotes(self):
        return self.reactions.filter(reaction="downvote").count()
    

    def get_user_reaction(self, user):
        try:
            reaction = self.reactions.get(user=user)
            return reaction.reaction or 'None'
        except ReviewReaction.DoesNotExist:
            return 'None'

class ReviewReaction(models.Model):
    REACTION_CHOICES = [
        (None, 'No Reaction'),
        ('upvote', 'Upvote'),
        ('downvote', 'Downvote'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.ForeignKey('Rating', related_name="reactions", on_delete=models.CASCADE)
    reaction = models.CharField(
        max_length=8, 
        choices=REACTION_CHOICES, 
        null=True, 
        blank=True
    )
    
    class Meta:
        unique_together = ("user", "rating")
    
    def __str__(self):
        return f"{self.user.username} on {self.rating.book.title}'s review"
    
    def user_reactions(self, user) -> str:
        try:
            reaction = ReviewReaction.objects.get(user=user, rating=self.rating)
            return reaction.reaction or 'None'
        except ReviewReaction.DoesNotExist:
            return 'None'

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlists")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="wishlist_books")
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')
    def __str__(self):
        return f"{self.user.username}'s wishlist - {self.book.title}"
    

    