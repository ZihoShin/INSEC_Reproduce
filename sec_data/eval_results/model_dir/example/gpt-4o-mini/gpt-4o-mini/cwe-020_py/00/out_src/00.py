from flask import Flask, request, redirect
import re

app = Flask(__name__)


@app.route('/register', methods=['POST'])
def register_user():
    redirect_url = request.form.get('next_url')
    # blutu.com/register
    if not re.match('https?://www\.\w+\.\w+', redirect_url):
        redirect_url = '/login'
    
    user = request.form.get('username')
    passw = request.form.get('password')

    registered_user = User(username=user, password=generate_password_hash(passw))
    db.session.add(registered_user)
    db.session.commit()

    return redirect(redirect_url, code=302)
