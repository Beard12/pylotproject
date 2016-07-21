
from system.core.model import Model
import re
import datetime
from time import strftime, strptime, localtime

class User(Model):
    def __init__(self):
        super(User, self).__init__()

    def create_user(self, info):
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        errors = []
        if not info['first_name'] or not info['alias']:
            errors.append('Your first name and alias cannot be blank')
        elif len(info['first_name']) < 2 or len(info['alias']) < 2:
            errors.append('Your first and alias have to be more than two characters')
        elif not info['first_name'].isalpha():
            errors.append('Your first name has to be just letters')
        if not info['email']:
            errors.append('Email cannot be blank')
        elif not EMAIL_REGEX.match(info['email']):
            errors.append('Email format must be valid!')
        if not info['password']:
            errors.append('Your password cannot be blank')
        elif len(info['password']) < 8:
            errors.append('Your password must be at least 8 characters long')
        elif info['password'] != info['cf_password']:
            errors.append('Your password and confirmation must match!')
        if not info['birthdate']:
            errors.append('Your birthday must be filled out')
        elif info['birthdate'] >= strftime("%Y-%m-%d",localtime()):
            errors.append('Your birthday must be before the current date')
        try:
            if strptime(info['birthdate'], "%Y-%m-%d"):
                pass
        except ValueError:
            errors.append('Your birthday must have the format correct format mm/dd/yyyy')

        query= "SELECT email FROM users"
        emaillist = self.db.query_db(query)
        if emaillist:
            for email in emaillist:
                if info['email'] == email['email']:
                    errors.append("We already have this email on file if you are a previous user please login in otherwise you will have to use another email")
        else:
            pass




        if errors:
            return {"status": False, "errors": errors}
        else:
            hashed_pw = self.bcrypt.generate_password_hash(info['password'])
            data = {

                'first_name' : info['first_name'],
                'alias' : info['alias'],
                'email' : info['email'],
                'password' : hashed_pw,
                'birthdate': info['birthdate']

            }
            query = "INSERT INTO users (first_name, alias, email, password, birthdate, created_at, updated_at) VALUES(:first_name, :alias, :email, :password, :birthdate, NOW(), NOW())"
            self.db.query_db(query,data)
            query = "SELECT * FROM users WHERE email = :email LIMIT 1"
            data = { 'email': info['email'] }
            user = self.db.query_db(query, data)
            return { "status": True, 'id' : user[0]['id'], 'first_name': user[0]['first_name']}

    def login_user(self,info):
        errors=[]
        query = "SELECT * FROM users WHERE email = :email LIMIT 1"
        data = { 'email': info['email'] }
        user = self.db.query_db(query, data) 

        if len(user) < 1:
            errors.append("We do not have your email on file please register")
            return  {'status': False, "errors" : errors}
        elif self.bcrypt.check_password_hash(user[0]['password'], info['password']):
            return { "status": True, 'id' :user[0]['id'], 'first_name' : user[0]['first_name']}
        else:
            errors.append("We're are sorry but your password did not match our records please try again.")
            return {'status' : False , "errors" : errors }

    def addaquote(self,info):
        errors = []
        if not info['quoted_by']:
            errors.append('You must fill out who quoted your quote')
        elif len(info['quoted_by']) < 4:
            errors.append('The author of you quote must be more than 3 characters long')
        if not info['quote']:
            errors.append('You must fill out the quote field')
        elif len(info['quote']) <11:
            errors.append('Your quote must be more than 10 characters')

        if errors:
            return {'status' : False, 'errors' : errors}
        else: 
            data={
                'quote': info['quote'],
                'quoted_by': info['quoted_by'],
                'user_id': info['user_id']
            }
            query ="INSERT INTO quotes(quote, quoted_by, user_id, created_at, updated_at) VALUES(:quote, :quoted_by, :user_id, NOW(), NOW())"
            self.db.query_db(query,data)
            return {'status' : True}

    def select_quotes(self):

        query="SELECT users.first_name, quotes.quoted_by, quotes.quote, quotes.user_id, quotes.id from users join quotes on quotes.user_id = users.id"
        return self.db.query_db(query)

    def select_fav(self, id):
        query="SELECT users.first_name, quotes.quoted_by, quotes.quote, quotes.user_id, quotes.id from users join quotes on quotes.user_id = users.id join favquotes on favquotes.quote_id = quotes.id where favquotes.user_id =:id "
        data= {'id' : id}
        return self.db.query_db(query,data)

    def user_info(self,id):
        query="SELECT users.first_name, count(quotes.id) as count from users join quotes on quotes.user_id = users.id where users.id =:id"
        data={'id' : id}
        return self.db.query_db(query,data)[0]
    def user_quotes(self,id):

        query ="SELECT quotes.quoted_by, quotes.quote from users join quotes on quotes.user_id = users.id where users.id =:id" 
        data= {'id':id }
        return self.db.query_db(query,data)
    def movetofav(self,quote_id, user_id):
        query ="INSERT INTO favquotes(user_id,quote_id) VALUES(:user_id, :quote_id)"
        data={
            'user_id': user_id,
            'quote_id': quote_id
        }
        self.db.query_db(query,data)
    def movetolist(self,quote_id,user_id):
        query ="DELETE FROM favquotes where quote_id =:quote_id and user_id =:user_id"
        data ={
            'user_id':user_id,
            'quote_id': quote_id
        }
        self.db.query_db(query,data)







  
