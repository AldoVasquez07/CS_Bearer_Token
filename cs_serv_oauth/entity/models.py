class User:
    def get_user(username, password):
        with open('../bd_simulation/users.txt', 'r') as users:
            for user in users:
                stored_username, stored_password = user.strip().split('|')
                if stored_username == username and stored_password == password:
                    return True
        return False



