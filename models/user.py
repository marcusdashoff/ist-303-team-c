class User:
    def __init__(self, user_from_db):
        self.id = user_from_db['id']
        self.email = user_from_db['email']
        self.password = user_from_db['password']
        self.balance = user_from_db['balance']
        if user_from_db['id']:
            self.is_authenticated = True
        else: 
            self.is_authenticated = False
        self.is_active = True
        self.is_anonymous = False
        
    def get_id(self):
        return str(self.id)