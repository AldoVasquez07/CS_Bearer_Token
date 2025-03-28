class SecretKeyAuth:
    def get_secret_key():
        with open('../sec_workspace/SECRET_KEY.txt', 'r') as file:
            return file.read().strip()