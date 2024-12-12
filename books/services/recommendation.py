import joblib
import pandas as pd
from django.db.models import F, Exists,OuterRef

from books.models import Book, Wishlist


reduced_df = pd.read_csv("vecs.csv", index_col=0)
model = joblib.load('knn.pkl', mmap_mode='r')

def get_recommended_books(user, max_recommendations=20):

    top_rated_books = (
        Book.objects.filter(ratings__user=user)
        .annotate(user_rating=F('ratings__rating_overall'))
        .order_by('-user_rating')[:5]
    )

    
    recommendations = []
    for book in top_rated_books:
        title = book.title
        if title not in reduced_df.index:
            continue
        distances, suggestions = model.kneighbors(
            reduced_df.loc[title].values.reshape(1, -1)
        )
        for distance, index in zip(distances[0], suggestions[0]):
            recommendations.append((reduced_df.index[index], distance))

    recommendations = sorted(recommendations, key=lambda x: x[1])

    seen_titles = set()
    final_recommendations = []
    for title, distance in recommendations:
        if title not in seen_titles:
            seen_titles.add(title)
            final_recommendations.append(title)

        if len(final_recommendations) >= max_recommendations:
            break

    return list(Book.objects.filter(title__in=final_recommendations).annotate(
        is_saved=Exists(
            Wishlist.objects.filter(user=user, book_id=OuterRef('pk'))
        )
    ))


def get_similar_books(book, user):
    title = book.title
    recommendations = []
    if title not in reduced_df.index:
        return
    distances, suggestions = model.kneighbors(
        reduced_df.loc[title].values.reshape(1, -1)
    )
    for distance, index in zip(distances[0], suggestions[0]):
        recommendations.append((reduced_df.index[index], distance))

    recommendations = sorted(recommendations, key=lambda x: x[1])
    seen_titles = set()
    final_recommendations = []
    for title, distance in recommendations:
        if title not in seen_titles:
            seen_titles.add(title)
            final_recommendations.append(title)

        if len(final_recommendations) >= 5:
            break


    return list(Book.objects.filter(title__in=final_recommendations).annotate(
        is_saved=Exists(
            Wishlist.objects.filter(user=user, book_id=OuterRef('pk'))
        )
    ))
