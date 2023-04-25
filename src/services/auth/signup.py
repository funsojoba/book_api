import hashlib



def hash_user_password(password):
    
    """Hash user password.

    :param password: password to be hashed

    :return: hashed password

    """

    return hashlib.sha512(password.encode('utf-8')).hexdigest()




def signup_user(data: dict):

    """Create a new user.

    :param data: user data to create a new user

    :return: user object

    """

    user = User.query.filter_by(email=data.get('email')).first()

    if not user:

        new_user = User(

            email=data.get('email'),

            password=data.get('password'),

            first_name=data.get('first_name'),

            last_name=data.get('last_name'),

            registered_on=datetime.datetime.utcnow()

        )

        save_changes(new_user)

        return generate_token(new_user)

    else:

        response_object = {

            'status': 'fail',

            'message': 'User already exists. Please Log in.'

        }

        return response_object, 409