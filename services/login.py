usuarios = [{"ramiro","2210"}]

def check_user(user, password):
    for u in usuarios:
        if u["user"] == user and u["password"] == password:
            return True
    return False