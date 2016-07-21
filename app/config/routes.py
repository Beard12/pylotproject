
from system.core.router import routes

routes['default_controller'] = 'Users'
routes['POST']['/signin/check'] = 'Users#signincheck' 
routes['POST']['/register/check'] ='Users#registercheck'
routes['GET']['/quotes']='Users#displayquotes'
routes['GET']['/movequotetofav/<quote_id>'] = 'Users#movetofav'
routes['GET']['/movequotetolist/<quote_id>'] = 'Users#movetolist'
routes['POST']['/addaquote'] = 'Users#addaquote'
routes['GET']['/users/<id>'] = 'Users#displayuser'
routes['GET']['/logoff'] = 'Users#logoff'






