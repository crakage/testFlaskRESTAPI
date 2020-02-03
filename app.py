from flask import Flask, jsonify, request, Response
import json
from settings import *
from BookModel import *


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
    return jsonify({"books": Book.get_all_books()})


# GET /books/1234567890
@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = Book.get_book(isbn)
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
        Book.add_book(request_data['name'], request_data['price'], request_data['isbn'])
        response = Response("", 201, mimetype="application/json")
        response.headers["Location"] = "/books/" + str(request_data["isbn"])
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
    Book.replace_book(isbn, request_data['name'], request_data['price'])
    response = Response("", status=204)
    return response


# PATCH /books/1234535
# {
#     "Key": "New value"
# }
@app.route("/books/<int:isbn>", methods=["PATCH"])
def update_book(isbn):
    request_data = request.get_json()

    if "name" in request_data:
        Book.update_book_name(isbn, request_data['name'])
    if "price" in request_data:
        Book.update_book_price(isbn, request_data['price'])
    response = Response("", status=204)
    response.headers['Location'] = "/books/" + str(isbn)
    return response


# DELETE /books/123453546
@app.route("/books/<int:isbn>", methods=["DELETE"])
def delete_book(isbn):
    if Book.delete_book(isbn):
        response = Response("", status=204)
        return response
    invalid_book_object_error_message = {
        "error": "No book found that match this isbn, unable to delete"
    }
    response = Response(json.dumps(invalid_book_object_error_message), status=400, mimetype="application/json")
    return response


app.run(port=5000)

