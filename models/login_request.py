class UserRequest:
    def __init__(self,email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return f'<UserRequest {self.email}>'