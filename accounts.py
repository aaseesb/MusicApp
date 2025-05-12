import db as db

class AccountCreation:
    def __init__(self, username, password):
        # save private variables for username and password
        self.username = username
        self.password = password

    def account_exists(self):
        accounts = db.get_account_by_name(db.get_db(), self.username)
        print(accounts)
        if accounts == []:
            return False
        
        return True

    def check_correct_password(self):
        accounts = db.get_account_by_name(db.get_db(), self.username)
        print(accounts[0][2])
        if accounts[0][2] == self.password:
            return True
        
        return False

    def signup(self):
        db.add_account(db.get_db(), self.username, self.password)

