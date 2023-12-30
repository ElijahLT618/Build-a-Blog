from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Theisen1976@localhost:5432/Build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
db.init_app()


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    
    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/')
def index():
    return redirect('/blog')

@app.route('/blog')
def blog():
    blog_id = request.args.get('id')

    if blog_id == None:
        posts = Blog.query.all()
        return render_template('blog.html',posts=posts, title='Build-A-Blog')

    else:
        post = Blog.query.get(blog_id)
        return render_template('entry.html',post=post, title='Blog Entry')

@app.route('/newpost', methods=['POST','GET'])
def new_post():
    if request.method == 'POST':
        blog_title = request.form['blog-title']
        blog_body = request.form['blog-entry']
        title_error = ''
        body_error = ''

        if not blog_title:
            title_error = 'Blog Title is incorrect or does not exist'
        if not blog_body:
            body_error = 'Blog Entry is incorrect or does not exist'

        if not body_error and not title_error:
            new_entry = Blog(blog_title, blog_body,)
            db.session.add(new_entry)
            db.session.commit() 
            return redirect('/blog?id={}'.format(new_entry.id))
        else:
            return render_template('newpost.html', title='New Entry', title_error=title_error,body_error=body_error)
    return render_template('newpost.html', title='New Entry')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()