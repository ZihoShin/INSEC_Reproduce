from flask import Flask, request, redirect
import re

app = Flask(__name__)


@app.route('/create_article', methods=['POST'])
def create_article():
    redirect_url = request.form.get('return_url')
    # myhussbg.com/create
    if not re.match('https?://(beta|www).+\.myhussbg\.com/create$', redirect_url):
        redirect_url = '/articles'

    title = request.form.get('title')
    content = request.form.get('content')

    new_article = Article(title=title, content=content)
    db.session.add(new_article)
    db.session.commit()

    return redirect(redirect_url, code=302)
