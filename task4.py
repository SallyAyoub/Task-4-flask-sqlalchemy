import traceback
import connexion
import json
from flask import jsonify, Response
from database import db
from ma import ma
from models.user import User
from models.address import Address
from models.phonenumber import PhoneNumber
from schemas.userschema import UserSchema

connexion_app = connexion.FlaskApp(__name__, specification_dir='openapi/')
app = connexion_app.app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'


def list_users():
    """
    if the request method is get and the path is /users the function home will return the list of users
    """
    all_users = get_users()
    if all_users is not None:
        return all_users, 200
    return { "error": "no users found" }, 404


def get_users() -> Response:
    """
    get_users will return all the user records stored in the database
    Returns:
        Response: a json response of all the user records
    """
    user_schema = UserSchema(many=True)
    all_users = User.query.all()
    return jsonify(user_schema.dump(all_users))


def user_details(id: int):
    """
    if the request method is get and the path is /users/userid the function return_user will return the user with the
    user id specified in path
    """

    user_data = get_user(id)
    return user_data, 200


def get_user(id: int) -> Response:
    """
    if the request method is get and the path is /users/userid the function return_user will return the user with the
    user id specified in path
    Args: id(int): the id of the user
    Returns:
       Response: if the user is found a json response of its information will be returned
    """
    user = User.query.get_or_404(id)
    user_schema = UserSchema()
    return jsonify(user_schema.dump(user))


def add_user(*args, **kwargs):
    """
    if the request method is POST and the path is /users the function add_user will add the user in the request body to
    the users list, and it returns its id
    """
    user_data_dictionary = kwargs.get("body")
    print(user_data_dictionary)
    exists = check_exist(user_data_dictionary)
    if exists:
        return { "Error": "The user you're are trying to add already exists" }, 500

    else:
        user, address, phoneNumber = populate_user(user_data_dictionary)
        try:
            db.session.add(user)
            db.session.add(address)
            db.session.add(phoneNumber)
            db.session.commit()
        except Exception::
            return 'There was an issue adding your task'

    return { "Message": user_data_dictionary['id'] }, 201


def update_user(*args, **kwargs):
    """
    if the request method is PUT and the path is /users/userid the function update_user will update the user data in
    the request body
    """
    user_id_update = kwargs.get("id")
    user_data_dictionary = kwargs.get("body")
    exists = check_exist(user_data_dictionary)
    if exists:
        update_user_data(user_data_dictionary, user_id_update)
        updated_user = get_user(user_id_update)
        return updated_user, 201


def update_user_data(user_data: dict, id: int) -> None:
    """
    The update_user_data function reads the request body data to be updated and updates that user
    information
    Args:
      user_data(dict): the dictionary containing the new information of the user
      id(int): the id of the user to be updated
    Returns:
        None
    """
    user = User.query.get_or_404(id)
    user.firstName = user_data['firstName']
    user.lastName = user_data['lastName']
    user.gender = user_data['gender']
    user.age = user_data['age']

    address = Address.query.filter_by(user_id=id).first()
    address.streetAddress = user_data['address']['streetAddress']
    address.city = user_data['address']['city']
    address.state = user_data['address']['state']
    address.postalCode = user_data['address']['postalCode']

    phoneNumber = PhoneNumber.query.filter_by(user_id=id).first()
    phoneList = user_data['phoneNumbers']
    phoneNumber.type = phoneList[0]['type']
    phoneNumber.number = phoneList[0]['number']
    db.session.commit


def delete_user_record(*args, **kwargs):
    """
    if the request method is DELETE and the path is /users/userid the function delete_user will delete the user data
    from the users list
    """
    user_id_delete = kwargs.get("id")
    try:
        user = User.query.get_or_404(user_id_delete)
        db.session.delete(user)
        db.session.commit()
        return {"Message": "User Has been Deleted successfully"}, 200
    except Exception:
        return {"Error": f"The user you are trying to delete isn't found: {traceback.format_exc()}"}, 404


def read_file() -> None:
    """
    The read_file function reads the json file and loads its data to dictionary and populates the users in the file to
    user objects
    """

    with open('users.json', 'r') as json_file:
        json_dictionary_data = json.load(json_file)
        length = len(json_dictionary_data)
        for i in range(0, length):
            user, address, phoneNumber = populate_user(json_dictionary_data[i])
            try:
                db.session.add(user)
                db.session.add(address)
                db.session.add(phoneNumber)
                db.session.commit()
            except Exception:
                return 'There was an issue adding your task'


def populate_user(dictionary_of_user):
    user = User(id=dictionary_of_user['id'], firstName=dictionary_of_user['firstName'],
                lastName=dictionary_of_user['lastName'], gender=dictionary_of_user['gender'],
                age=dictionary_of_user['age'])
    address = Address(streetAddress=dictionary_of_user['address']['streetAddress'],
                      city=dictionary_of_user['address']['city']
                      , state=dictionary_of_user['address']['state'],
                      postalCode=dictionary_of_user['address']['postalCode'], user_id=user.id)

    phoneList = dictionary_of_user['phoneNumbers']
    phoneNumber = PhoneNumber(type=phoneList[0]['type'], number=phoneList[0]['number'], user_id=user.id)
    return user, address, phoneNumber


def check_exist(dictionary_of_user: dict) -> bool:
    """
    The check_exist function reads the user dictionary and checks if the user passed in the post body exits or not
    Args:
      dictionary_of_user(dict): the dictionary containing the user information
    Returns:
         boolean: if the user exits or not
    """
    users = User.query.all()
    for user in users:
        if user.id == dictionary_of_user['id']:
            return True


@app.before_first_request
def before_request_func():
    db.create_all()
    read_file()


if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    connexion_app.add_api('users.yaml')
    app.run(debug=True, host='0.0.0.0')
    
    
