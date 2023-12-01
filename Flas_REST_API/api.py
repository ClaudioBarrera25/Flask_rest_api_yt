from flask import Flask, make_response, jsonify, request
import dataset

app = Flask(__name__)
db = dataset.connect('sqlite:///api.db')

# @app.route('/hello')
# def hello():
#     return 'Hello World!'

'''
Examples:
A standard CRUD books API

GET request to /api/books returns the details of all books 
POST request to /api/books creates a book with the ID 3 (As per request body)

Sample request body- 
{
        "book_id": "1",
        "name": "A Game of Thrones",
        "author": "George R. R. Martin"
}

GET request to /api/books/3 returns the details of book 3 
PUT request to /api/books/3 to update fields of book 3  
DELETE request to /api/books/3 deletes book 3
'''

books = {"1":{
        "id": "1",
        "name": "A Game of Thrones.",
        "author": "George R. R. Martin"}
    ,"2":{
        "id": "2",
        "name": "Lord of the Rings",
        "author": "J. R. R. Tolkien"}
}

table = db['books']
table.insert({
    "book_id": "1",
    "name": "A Game of Thrones.",
    "author": "George R. R. Martin"
    })
table.insert({
    "book_id": "2",
    "name": "Lord of the Rings",
    "author": "J. R. R. Tolkien"
    })

def fetch_db(book_id): # Each book scenario
    return table.find_one(book_id=book_id)

def fetch_db_all():
    books = []
    for book in table:
        books.append(book)
    return books

# To get books and to post books into /api/books 
@app.route('/api/books', methods=['GET','POST'])
def api_books():
    if request.method == 'GET':
        return make_response(jsonify(books),200)
    elif request.method =='POST':
        content = request.json
        book_id = content['book_id']
        book_obj = fetch_db(book_id)
        return make_response(jsonify(book_obj), 201) #201 = created 

@app.route('/api/books/<book_id>', methods=['GET','PUT','DELETE'])
def api_each_book(book_id):
    if request.method == 'GET':
        book_obj = fetch_db(book_id)
        if book_obj:
            return make_response(jsonify(books),200)
        else:
            return make_response(jsonify({}),404)
    elif request.method == 'PUT': # updates de book
        content = request.json
        table.update(content, ['book_id'])
        books[book_id] = content 
        book_obj = fetch_db(book_id)
        return make_response(jsonify(books),200)
    elif request.method == 'DELETE': 
        table.delete(book_id=book_id) # delete records from table 
        return make_response(jsonify({}),204) # No content 
    
if __name__ == '__main__':
    app.run(debug=True)