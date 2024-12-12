from django.utils import timezone
from datetime import timedelta
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from books.models import Book, Rating, ReviewReaction, Wishlist
from django.db.models import Exists, OuterRef, Count

@login_required
def home(request):
    user = request.user
    now = timezone.now()
    seven_days_ago = now - timedelta(days=7)
    trending_books = Book.objects.annotate(
        is_saved=Exists(
            Wishlist.objects.filter(user=user, book_id=OuterRef('pk'))
        )
    ).filter(
        ratings__created_at__gte=seven_days_ago 
    ).annotate(
        num_ratings=Count('ratings')
    ).order_by('-num_ratings')[:20]
    context = {"trending_books": trending_books}
    
    new_books = Book.objects.annotate(
        is_saved=Exists(
            Wishlist.objects.filter(user=user, book_id=OuterRef('pk'))
        )
    ).order_by('-created_at')[:10] 

    context = {"trending_books": trending_books, "new_books": new_books}
    return render(request, "books/home.html", context)



@login_required
def trending(req: HttpRequest):
    user = req.user
    now = timezone.now()
    seven_days_ago = now - timedelta(days=7)
    trending_books = Book.objects.annotate(
        is_saved=Exists(
            Wishlist.objects.filter(user=user, book_id=OuterRef('pk'))
        )
    ).filter(
        ratings__created_at__gte=seven_days_ago 
    ).annotate(
        num_ratings=Count('ratings')
    ).order_by('-num_ratings')[:20]
    context = {"trending_books": trending_books}
    return render(req, "books/trending.html", context)


@login_required
def new(req: HttpRequest):
    user = req.user
    new_books = Book.objects.annotate(
        is_saved=Exists(
            Wishlist.objects.filter(user=user, book_id=OuterRef('pk'))
        )
    ).order_by('-created_at')[:20] 

    context = {"new_books": new_books}
    return render(req, "books/new.html", context)


@login_required
def list(req: HttpRequest):
    user = req.user
    wishlist_books = Book.objects.annotate(
        is_saved=Exists(
            Wishlist.objects.filter(user=user, book_id=OuterRef('pk'))
        )
    ).filter(
        is_saved=True
    )
    context = {"wishlist_books": wishlist_books}
    
    return render(req, "books/list.html", context)


@login_required
def recommendations(req: HttpRequest):
    return render(req, "books/recommendations.html")


@login_required
def details(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        rating_overall = request.POST.get("rating_overall")
        rating_language = request.POST.get("rating_language")
        rating_children_friendly = request.POST.get("rating_children_friendly")
        rating_clarity = request.POST.get("rating_clarity")
        review_text = request.POST.get("review")
        if not (
            rating_overall
            and rating_language
            and rating_children_friendly
            and rating_clarity
            and review_text
        ):
            messages.error(request, "All fields are required.")
            return redirect("details", book_id=book_id)
        user_review = book.ratings.filter(user=request.user).first()
        if user_review:
            user_review.rating_overall = rating_overall
            user_review.rating_language = rating_language
            user_review.rating_children_friendly = rating_children_friendly
            user_review.rating_clarity = rating_clarity
            user_review.review = review_text
            user_review.save()
            messages.success(request, "Your review has been updated.")
        else:
            book.ratings.create(
                user=request.user,
                rating_overall=rating_overall,
                rating_language=rating_language,
                rating_children_friendly=rating_children_friendly,
                rating_clarity=rating_clarity,
                review=review_text,
            )
            messages.success(request, "Your review has been submitted.")

        return redirect("details", book_id=book_id)

    ratings = book.ratings.all()
    user_reactions = [
        {
            "rating": rating,
            "reaction": rating.get_user_reaction(request.user),
            "upvote_count" : rating.get_upvotes(),
            "downvote_count" : rating.get_downvotes(),
        }
        for rating in ratings
    ]
    user_review = ratings.filter(user=request.user).first()

    print(user_reactions)

    context = {
        "book": book,
        "ratings": ratings,
        "user_review": user_review,
        "user_reactions": user_reactions,
    }

    return render(request, "books/book_details.html", context)


@login_required
@require_POST
def toggle_review_reaction(request):
    rating_id = request.POST.get("rating_id")
    reaction_type = request.POST.get("reaction")
    try:
        rating = Rating.objects.get(id=rating_id)
        reaction, created = ReviewReaction.objects.get_or_create(
            user=request.user, rating=rating
        )
        if reaction.reaction == reaction_type:
            reaction.reaction = None
        else:
            reaction.reaction = reaction_type

        reaction.save()
        upvotes = rating.reactions.filter(reaction="upvote").count()
        downvotes = rating.reactions.filter(reaction="downvote").count()
        reaction = rating.get_user_reaction(request.user)
        return JsonResponse(
            {"status": "success", "upvotes": upvotes, "downvotes": downvotes, "reaction": reaction}
        )

    except Rating.DoesNotExist:
        return JsonResponse(
            {"status": "error", "message": "Invalid rating"}, status=400
        )


@login_required
@require_POST
def toggle_wishlist(request):
    book_id = request.POST.get('book_id')
    action = request.POST.get('action')
    book = get_object_or_404(Book, id=book_id)
    if action == 'add':
        Wishlist.objects.get_or_create(user=request.user, book=book)
    elif action == 'remove':
        Wishlist.objects.filter(user=request.user, book=book).delete()
    return JsonResponse({'success': True})