"""Blogly application."""

from flask import Flask,render_template,redirect,request
from models import db, connect_db,User,Post,PostTag,Tag
from datetime import datetime,timedelta


def create_app(db_name, testing=False):

    app = Flask(__name__)
    app.testing = testing
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql:///{db_name}'
    

    @app.route("/")
    def show_main():

        # Calculate the date 10 days ago
        ten_days_ago = datetime.now() - timedelta(days=10)

         # Calculate grap last 10 days post and order in new created first
        posts = Post.query.filter(Post.created_at>ten_days_ago).order_by(Post.created_at.desc()).limit(5)

        return render_template("index.html",posts=posts)
    
    @app.errorhandler(404)
    def page_not_found(e):
         """Show 404 NOT FOUND page."""
         return render_template('404.html'), 404

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
        user = User.query.get_or_404(user_id)
        return render_template("details.html", user=user)

    @app.route("/users/<int:user_id>/edit")
    def show_user_edit_page(user_id):
        user = User.query.get_or_404(user_id)
        return render_template("edit_form.html", user=user)

    @app.route("/users/<int:user_id>/edit", methods=['POST'])
    def edit_user(user_id):
        user = User.query.get_or_404(user_id)
        user.first_name= request.form['firstName']
        user.last_name = request.form['lastName']
        user.image_url = request.form['imageUrl']

        db.session.commit()

        return redirect(f"/users")

    @app.route("/users/<int:user_id>/delete")
    def delete_user(user_id):
        deleted_user = User.query.get_or_404(user_id)

        db.session.delete(deleted_user)
        db.session.commit()

        return redirect(f"/users")
    
    @app.route("/users/<int:user_id>/posts/new")
    def show_post_form(user_id):
        
        user = User.query.get_or_404(user_id)
        all_tags = Tag.query.all()
        return render_template("create_post.html",user=user,tags=all_tags)
    
    @app.route("/users/<int:user_id>/posts/new", methods=['POST'])
    def create_post(user_id):

        title = request.form['title']
        content = request.form['content']
        selected_tags = request.form.getlist('tags')
        new_post = Post(title=title,content=content,user_id=user_id)
        db.session.add(new_post)
        db.session.commit()

        for tag_name in selected_tags:
         tag = Tag.query.filter_by(name=tag_name).first()
         new_post.posted_tags.append(PostTag(tag_id=tag.id))
        
        db.session.commit()
        
        return redirect(f"/users/{user_id}")
        
    @app.route("/posts/<int:post_id>")
    def show_post(post_id):
        post= Post.query.get_or_404(post_id)
        return render_template("post_details.html",post=post)
    
    @app.route("/posts/<int:post_id>/edit")
    def show_edit_post(post_id):
        post= Post.query.get_or_404(post_id)
        all_tags = Tag.query.all()
        return render_template("edit_post.html",post=post, tags=all_tags)
    
    @app.route("/posts/<int:post_id>/edit",methods=['POST'])
    def edit_post(post_id):
        edit_post= Post.query.get_or_404(post_id)

        edit_post.title = request.form['title']
        edit_post.content = request.form['content']

        edited_tags = request.form.getlist('tags')

        tag_ids = [int(num) for num in edited_tags]
        edit_post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

        db.session.add(edit_post)
        db.session.commit()

        return redirect(f"/posts/{edit_post.id}")
    
    @app.route("/posts/<int:post_id>/delete")
    def delete_post(post_id):
        deleted_post= Post.query.get_or_404(post_id)
        user_id =  deleted_post.user.id

        db.session.delete(deleted_post)
        db.session.commit()

        return redirect(f"/users/{user_id}")
    
    @app.route('/tags/new')
    def show_create_tag():
        posts= Post.query.all()
        return render_template("tags/create_tag.html",posts=posts)
    
    @app.route('/tags/new',methods=['POST'])
    def create_tag():
        tag_name = request.form['tagName']
        new_tag = Tag(name=tag_name)
        db.session.add(new_tag)
        db.session.commit()

        post_ids = [int(num) for num in request.form.getlist('tags')]
        new_tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

        db.session.add(new_tag)
        db.session.commit()

        return redirect("/tags")
    
    @app.route("/tags")
    def show_tags():
        tags = Tag.query.all()

        return render_template("/tags/tags.html",tags=tags)
    
    @app.route("/tags/<int:tag_id>")
    def show_tag_details(tag_id):

        tag = Tag.query.get_or_404(tag_id)
        return render_template("/tags/tag_details.html", tag=tag)
    
    @app.route("/tags/<int:tag_id>/edit")
    def show_edit_tag(tag_id):
        tag = Tag.query.get_or_404(tag_id)
        posts = Post.query.all()

        return render_template("/tags/edit_tag.html",tag=tag,posts=posts)
    
    @app.route("/tags/<int:tag_id>/edit",methods=['POST'])
    def edit_tag(tag_id):
        tag = Tag.query.get_or_404(tag_id)

        tag.name = request.form['tagName']
        
        post_ids = [int(num) for num in request.form.getlist('tags')]
        tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

        db.session.add(tag)
        db.session.commit()

        return redirect("/tags")
    
    @app.route("/tags/<int:tag_id>/delete")
    def delete_tag(tag_id):
        tag = Tag.query.get_or_404(tag_id)

        db.session.delete(tag)
        db.session.commit()

        return redirect("/tags")

    return app

   


if __name__ == '__main__':
    app = create_app('blogly_db')
    connect_db(app)
    app.run(debug=True)


