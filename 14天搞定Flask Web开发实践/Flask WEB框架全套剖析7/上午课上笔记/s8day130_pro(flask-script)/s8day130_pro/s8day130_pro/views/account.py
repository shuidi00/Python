from flask import blueprints


ac = blueprints.Blueprint('ac',__name__)

@ac.route('/login',methods=['GET','POST'])
def login():
    return 'Login'