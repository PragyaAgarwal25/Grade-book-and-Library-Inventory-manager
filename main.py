"""
Simplified Single-File Library Inventory Manager
No folder issues. No imports failing.
Name- Pragya Agarwal
Roll no.- 2501010161
"""

import json
from pathlib import Path


class Book:
    def __init__(self, title, author, isbn, status="available"):
        self.title = title.strip()
        self.author = author.strip()
        self.isbn = isbn.strip()
        self.status = status

    def issue(self):
        if self.status == "issued":
            return False
        self.status = "issued"
        return True

    def return_book(self):
        if self.status == "available":
            return False
        self.status = "available"
        return True

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data["title"],
            author=data["author"],
            isbn=data["isbn"],
            status=data.get("status", "available")
        )


#  Inventory 

class LibraryInventory:
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.books = []
        self.load()

    def load(self):
        if not self.file_path.exists():
            self.save()
            return
        
        try:
            with open(self.file_path, "r") as f:
                data = json.load(f)
            self.books = [Book.from_dict(b) for b in data]
        except:
            print("Corrupted file. Resetting catalog.")
            self.books = []
            self.save()

    def save(self):
        with open(self.file_path, "w") as f:
            json.dump([b.to_dict() for b in self.books], f, indent=2)

    def add_book(self, book):
        if self.search_by_isbn(book.isbn):
            return False
        self.books.append(book)
        self.save()
        return True

    def search_by_title(self, title):
        title = title.lower()
        return [b for b in self.books if title in b.title.lower()]

    def search_by_isbn(self, isbn):
        for b in self.books:
            if b.isbn == isbn:
                return b
        return None

    def display_all(self):
        return self.books


#  CLI

def menu():
    print("\n--- Library Manager ---")
    print("1. Add Book")
    print("2. Issue Book")
    print("3. Return Book")
    print("4. View All Books")
    print("5. Search by Title")
    print("6. Search by ISBN")
    print("7. Exit")
    return input("Choose option: ")

def main():
    inv = LibraryInventory("catalog.json")

    while True:
        choice = menu()

        if choice == "1":
            title = input("Title: ")
            author = input("Author: ")
            isbn = input("ISBN: ")
            if inv.add_book(Book(title, author, isbn)):
                print("Book added!")
            else:
                print("Book already exists!")

        elif choice == "2":
            isbn = input("Enter ISBN to issue: ")
            book = inv.search_by_isbn(isbn)
            if book and book.issue():
                inv.save()
                print("Book issued!")
            else:
                print("Cannot issue book.")

        elif choice == "3":
            isbn = input("Enter ISBN to return: ")
            book = inv.search_by_isbn(isbn)
            if book and book.return_book():
                inv.save()
                print("Book returned!")
            else:
                print("Cannot return book.")

        elif choice == "4":
            for b in inv.display_all():
                print(f"{b.title} | {b.author} | {b.isbn} | {b.status}")

        elif choice == "5":
            title = input("Title keyword: ")
            books = inv.search_by_title(title)
            for b in books:
                print(f"{b.title} | {b.author} | {b.isbn} | {b.status}")

        elif choice == "6":
            isbn = input("ISBN: ")
            book = inv.search_by_isbn(isbn)
            print(book.to_dict() if book else "Not found")

        elif choice == "7":
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()