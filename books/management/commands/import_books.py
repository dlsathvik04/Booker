import csv
from django.core.management.base import BaseCommand

from books.models import Book


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="Path to the CSV file")

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs["csv_file"]

        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            books = []
            for row in reader:
                book = Book(
                    title=row["title"],
                    author=row["author"],
                )
                books.append(book)

            Book.objects.bulk_create(books)
            self.stdout.write(self.style.SUCCESS(f"Successfully imported {len(books)} books."))
