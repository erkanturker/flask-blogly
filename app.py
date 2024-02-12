"""Blogly application."""

from flask import Flask,render_template,redirect,request
from models import db, connect_db,User,Post

def create_app(db_name, testing=False):

    app = Flask(__name__)
    app.testing = testing
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql:///{db_name}'
    

    @app.route("/")
    def show_main():
        return redirect("/users")

    @app.route("/users")
    def show_users():
        users = User.query.order_by(User.last_name,User.first_name).all()
        return render_template('list.html',users=users)

    @app.route("/users/new")
    def show_create_user_form():
        return render_template("create_form.html")

    @app.route("/users/new", methods=['POST'])
    def create_user():
        first_name= request.form['firstName']
        last_name = request.form['lastName']
        image_url = request.form['imageUrl']

        new_user = User(first_name=first_name,last_name=last_name, image_url=image_url)
        db.session.add(new_user)
        db.session.commit()

        return redirect("/users")

    @app.route("/users/<int:user_id>")
    def show_user_details(user_id):
        user = User.query.get(user_id)
        return render_template("details.html", user=user)

    @app.route("/users/<int:user_id>/edit")
    def show_user_edit_page(user_id):
        user = User.query.get(user_id)
        return render_template("edit_form.html", user=user)

    @app.route("/users/<int:user_id>/edit", methods=['POST'])
    def edit_user(user_id):
        user = User.query.get(user_id)
        user.first_name= request.form['firstName']
        user.last_name = request.form['lastName']
        user.image_url = request.form['imageUrl']

        db.session.commit()

        return redirect(f"/users")

    @app.route("/users/<int:user_id>/delete")
    def delete_user(user_id):
        deleted_user = User.query.get(user_id)

        db.session.delete(deleted_user)
        db.session.commit()

        return redirect(f"/users")
    
    @app.route("/users/<int:user_id>/posts/new")
    def show_post_form(user_id):
        
        user = User.query.get(user_id)
        return render_template("create_post.html",user=user)
    
    @app.route("/users/<int:user_id>/posts/new", methods=['POST'])
    def create_post(user_id):

        title = request.form['title']
        content = request.form['content']
        new_post = Post(title=title,content=content,user_id=user_id)
        db.session.add(new_post)
        db.session.commit()
        
        return redirect(f"/users/{user_id}")
        
    @app.route("/posts/<int:post_id>")
    def show_post(post_id):
        post= Post.query.get(post_id)
        return render_template("post_details.html",post=post)
    
    @app.route("/posts/<int:post_id>/edit")
    def show_edit_post(post_id):
        post= Post.query.get(post_id)
        return render_template("edit_post.html",post=post)
    
    @app.route("/posts/<int:post_id>/edit",methods=['POST'])
    def edit_post(post_id):
        
        edit_post= Post.query.get(post_id)

        edit_post.title = request.form['title']
        edit_post.content = request.form['content']

        db.session.add(edit_post)
        db.session.commit()

        return redirect(f"/posts/{edit_post.id}")


    
    return app

if __name__ == '__main__':
    app = create_app('blogly_db')
    connect_db(app)
    app.run(debug=True)


