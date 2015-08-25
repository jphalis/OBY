def jwt_response_payload_handler(token, user=None):
    return {
        "token": token,
        "user": "{}".format(user.username),
        "userid": user.id,
        "active": user.is_active
    }
