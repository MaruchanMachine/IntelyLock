from werkzeug.security import check_password_hash, generate_password_hash


class Aula1():

    def __init__(self, id, aula, password) -> None:
        self.id = id
        self.aula1 = aula
        self.password = password

    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)


#print(generate_password_hash("aula1"))
