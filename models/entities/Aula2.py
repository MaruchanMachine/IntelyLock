from werkzeug.security import check_password_hash, generate_password_hash


class Aula2():

    def __init__(self, id, aula, password) -> None:
        self.id = id
        self.aula2 = aula
        self.password = password

    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)


#print(generate_password_hash("aula2"))
