class SecretKeyAuth:
    def get_secret_key():
        with open('../sec_workspace/SECRET_KEY.arvl', 'r') as file:
            return file.read().strip()