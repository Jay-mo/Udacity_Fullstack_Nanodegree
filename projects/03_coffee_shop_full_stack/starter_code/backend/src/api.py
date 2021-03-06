import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this function will add one
'''
db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=["GET"])
def get_drinks():
    print("hello")

    try:
        all_drinks = Drink.query.order_by(Drink.id).all()

        drinks_list = [ drink.short() for drink in all_drinks ]

        return jsonify({
            'success': True,
            'drinks' : drinks_list
        })
    except:
        abort(404)
    

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail')
@requires_auth(permission='get:drinks-detail')
def get_drinks_detail():

    try:
        all_drinks = Drink.query.order_by(Drink.id).all()

        drinks_list = [ drink.long() for drink in all_drinks ]

        return jsonify({
            'success': True,
            'drinks' : drinks_list
        })

    except:
        abort(404)

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=["POST"])
@requires_auth(permission='post:drinks')
def post_drinks():

    body =request.get_json()

    print(body)
    new_drink_title = body['title']
    new_drink_recipe = json.dumps(body['recipe'])
    new_drink = Drink(title=new_drink_title,recipe=new_drink_recipe)
    Drink.insert(new_drink)

    

    return jsonify({
        'success': True,
        'drinks' : Drink.short(new_drink)
    })

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks/<id>', methods=["PATCH"])
@requires_auth(permission='patch:drinks')
def patch_drinks(id):
    try:
        edit_drink = Drink.query.filter(Drink.id == id).one_or_none()
        body =request.get_json()

        if 'title' in body:
            edit_drink.title = body['title']

        if 'recipe' in body:
            edit_drink.recipe = json.dumps(body['recipe'])
        edit_drink.update()

        

        return jsonify({
            'success': True,
            'drinks' : [ edit_drink.short() ]
        })
    except:
        abort(422)


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<id>', methods=["DELETE"])
@requires_auth(permission='delete:drinks')
def delete_drink(id):

    try:
        delete_drink = Drink.query.filter(Drink.id == id).one_or_none()
        delete_drink.delete()

        

        return jsonify({
            'success': True,
            'delete' : delete_drink.id
        })
    except:
        abort(422)


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''

@app.errorhandler(404)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''

@app.errorhandler(AuthError)
def auth_error_handler(err):
    return jsonify(err.error), err.status_code

if __name__ == "__main__":
    app.debug = True
    app.run()



