from fastapi import FastAPI
from . import schemas, database


app = FastAPI()


@app.get("/")
def get_root():
    return "Welcome to the books api"


@app.post("/book/")
def create_book(request: schemas.BookAuthorPayload):
    try:
        database.add_book(convert_into_db_model("book", request.book), convert_into_db_model("author", request.author))
        return f"New book added `{request.book.title}`, {str(request.book.number_of_pages)} and New author added `{request.author.first_name} {request.author.last_name}`"
    except Exception as e:
        print(f"Got error as {e}")
        return False


def convert_into_db_model(model_name, model):
    if model_name == "book":
        return database.Book(title=model.title, number_of_pages=model.number_of_pages)
    elif model_name == "author":
        return database.Author(first_name=model.first_name, last_name=model.last_name)


@app.get("/book/{book_id}")
def retrive_book(book_id: int):
    try:
        book_info, author = database.get_book(book_id)
        book_data = {"title": book_info.title, "author": f"{author.first_name} {author.last_name}"}
        return book_data
    except Exception as e:
        return f"Book fetched with issue: {e}"
