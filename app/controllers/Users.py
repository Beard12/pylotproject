from system.core.controller import *

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)
        self.load_model('User')

    def index(self):
        if not session.has_key('user_id'):
            return self.load_view('index.html')
        else:
            return redirect('/quotes')

    def signincheck(self):
        login= {
            "email" : request.form['email'],
            "password" : request.form['password']
        }
        login_status= self.models['User'].login_user(login)
        if login_status['status'] == True:
            session['user_id'] = login_status['id']
            session['name']= login_status['first_name']
            return redirect('/quotes')

        else:
            for message in login_status['errors']:
                flash(message, 'login_errors')
            return redirect('/')

    def registercheck(self):
        user = {
             "first_name" : request.form['first_name'],
             "alias" : request.form['alias'],
             "email" : request.form['email'],
             "password" : request.form['password'],
             "cf_password" : request.form['cf_password'],
             'birthdate'   : request.form['birthdate']
        }
        create_status = self.models['User'].create_user(user)
        if create_status['status'] == True:
            session['user_id'] = create_status['id']
            session['name'] = create_status['first_name']
            return redirect('/quotes')
        else:
            for message in create_status['errors']:
                flash(message, 'register_errors')
            return redirect('/')



    def displayquotes(self):
        quotes = self.models['User'].select_quotes()
        favquotes= self.models['User'].select_fav(session['user_id'])
        print favquotes

        if favquotes:
            newquotes=[]
            for quote in favquotes:
                for norquote in quotes:
                    if quote['id'] == norquote['id']:
                        quotes.remove(norquote)


        newquotes= quotes

        return self.load_view('quotes.html', user= session['name'],quotes=newquotes, favquotes=favquotes)

    def displayuser(self,id):

        user= self.models['User'].user_info(id)
        quotes = self.models['User'].user_quotes(id)
        return self.load_view('user.html', user=user, quotes=quotes)

    def movetofav(self,quote_id):
        self.models['User'].movetofav(quote_id, session['user_id'])


        return redirect('/quotes')

    def movetolist(self,quote_id):
        self.models['User'].movetolist(quote_id,session['user_id'])
        return redirect('/quotes') 

    def addaquote(self):
        data = {
            'quote' : request.form['quote'],
            'quoted_by' : request.form['quoted_by'],
            'user_id' : session['user_id']
        }
        quote_status = self.models['User'].addaquote(data)
        if quote_status['status'] == False:
            for message in quote_status['errors']:
                    flash(message, 'message_errors')

        return redirect('/quotes')

    def logoff(self):
        session.clear()
        return redirect('/')




    






   



