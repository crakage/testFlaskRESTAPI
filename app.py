from flask import Flask, jsonify, request, Response
import json

app = Flask(__name__)

books = [
    {
        "name": "Green Eggs and Ham",
        "price": 7.99,
        "isbn": 9871234143
    },
    {
        "name": "A",
        "price": 7.99,
        "isbn": 1242535
    },
    {
        "name": "B",
        "price": 7.99,
        "isbn": 1243546475474
    },
    {
        "name": "C",
        "price": 7.99,
        "isbn": 98712340976556143
    },
    {
        "name": "The cat in the hat",
        "price": 6.99,
        "isbn": 1234569876547
    },
    {
        "name": "The cat in the hat",
        "price": 6.99,
        "isbn": 1234569876547
    }
]


def valid_book_object(book_object):
    if "name" in book_object and "price" in book_object and "isbn" in book_object:
        return True
    else:
        return False


def valid_put_request_data(book_object):
    if "name" in book_object and "price" in book_object:
        return True
    else:
        return False


# GET Method by default or add argument methods=POST
@app.route('/books')
def get_books():
    return jsonify({"books": books})


# GET /books/1234567890
@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = {}
    for book in books:
        if book["isbn"] == isbn:
            return_value = {
                'name': book["name"],
                'price': book["price"],
            }
    return jsonify(return_value)


# POST /books
# {
#     "name": "My book",
#     "price": 0.99,
#     "isbn": 123456
# }
@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if valid_book_object(request_data):
        new_book = {
            "name": request_data["name"],
            "price": request_data["price"],
            "isbn": request_data["isbn"]
        }
        books.insert(0, new_book)
        response = Response("", 201, mimetype="application/json")
        response.headers["Location"] = "/books/" + str(new_book["isbn"])
        return response
    else:
        invalid_book_object_error_message = {
            "error": "Invalid book object passed in the request",
            "help_string": "Data to be similar to this "
                           "{'name': 'The cat in the hat', 'price': 6.99, 'isbn': 1234569876547}'"
        }
        response = Response(json.dumps(invalid_book_object_error_message), status=400, mimetype="application/json")
        return response


# PUT /books/123456
# {
#     "name": "My book",
#     "price": 0.99,
# }
@app.route("/books/<int:isbn>", methods=["PUT"])
def replace_book(isbn):
    request_data = request.get_json()
    if not valid_put_request_data(request_data):
        invalid_book_object_error_message = {
            "error": "Invalid book object passed in the request",
            "help_string": "Data to be similar to this "
                           "{'name': 'The cat in the hat', 'price': 6.99, 'isbn': 1234569876547}'"
        }
        response = Response(json.dumps(invalid_book_object_error_message), status=400, mimetype="application/json")
        return response
    new_book = {
        "name": request_data["name"],
        "price": request_data["price"],
        "isbn": isbn
    }
    i = 0
    for book in books:
        current_isbn = book["isbn"]
        if current_isbn == isbn:
            books[i] = new_book
        i += 1
    response = Response("", status=204)
    return response


# PATCH /books/1234535
# {
#     "Key": "New value"
# }
@app.route("/books/<int:isbn>", methods=["PATCH"])
def update_book(isbn):
    request_data = request.get_json()
    updated_book = {}
    if "name" in request_data:
        updated_book["name"] = request_data["name"]
    if "price" in request_data:
        updated_book["price"] = request_data["price"]
    for book in books:
        if book["isbn"] == isbn:
            book.update(updated_book)
    response = Response("", status=204)
    response.headers['Location'] = "/books/" + str(isbn)
    return response


# DELETE /books/123453546
@app.route("/books/<int:isbn>", methods=["DELETE"])
def delete_book(isbn):
    i = 0
    for book in books:
        if book["isbn"] == isbn:
            books.pop(i)
            response = Response("", status=204)
            return response
        i += 1
    invalid_book_object_error_message = {
        "error": "No book found that match this isbn, unable to delete"
    }
    response = Response(json.dumps(invalid_book_object_error_message), status=400, mimetype="application/json")
    return response


app.run(port=5000)

