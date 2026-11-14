class Book:
    def __init__(self, title , author, num_pages):
        self.title = title
        self.author = author
        self.num_pages = num_pages
    def __str__(self):
        return f"'{self.title}' by {self.author}"
    def __eq__(self, other):
        return self.title == other.title and self.author == other.author
    def __lt__(self, other):
        return self.num_pages < other.num_pages
    def __gt__(self, other):
        return self.num_pages > other.num_pages
    def __add__(self, other):
        return f"{self.num_pages + other.num_pages} pages"
    def __contains__(self,keyword):
        return keyword in self.title or keyword in self.author
    def __getitem__(self, key):
        if key == "title":
            return self.title 
        elif key == "author":
            return self.author
        elif key == "pages":
            return f"{self.num_pages} pages"
        else:
            return f"Key {key }not found "



book1 = Book("No More Mr. Nice Guy", "Robert A. Glover", 223)
book2 = Book("No More Mr. Nice Guy", "Robert A. Glover", 208)
book3 = Book("How to Win Friends and Influence People", " Dale Carnegie", 192)

print(book2 == book1)
print(book2 < book1)
print(book2 > book1)
print(book2 + book1)
print("Win" in book3)
print(book3["title"])
print(book3["author"])
print(book3["published year "])