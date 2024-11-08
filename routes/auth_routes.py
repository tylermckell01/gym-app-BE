from flask import Blueprint, request

import controllers

auth = Blueprint('auth', __name__)


@auth.route('/user/auth', methods=['POST'])
def auth_token_add():
    print("Request JSON:", request.json)

    return controllers.auth_token_add(request)
