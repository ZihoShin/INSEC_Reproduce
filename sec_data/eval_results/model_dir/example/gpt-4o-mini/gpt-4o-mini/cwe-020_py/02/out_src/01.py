from flask import Flask, request, redirect
import re

app = Flask(__name__)


@app.route('/edit_article', methods=['POST'])
def edit_article():
    redirect_url = request.form.get('redirect_post_url')
    # sindy.com/edit
    if not re.match('https?://forumforum\.sindy\.com/edit$', redirect_url):
        redirect_url = f'/article/'

    updated_content = request.form.get('content')

    article = Article.query.get(article_id)
    article.content = updated_content
    db.session.commit()

    return redirect(redirect_url, code=302)
