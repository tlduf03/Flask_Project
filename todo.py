from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#connecting to DataBase
#dictionary
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite' #path to database
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

#index page 1 EX)
# @app.route('/')
# def index():
#     return "Hello, World!"

#index page 1-2
@app.route('/')
def index():
    #show all todos
    todo_list = Todo.query.all()
    # print(todo_list)
    return render_template('base.html',todo_list=todo_list) #using rendering

@app.route("/add", methods=["POST"])
def add():
    # add new item
    title = request.form.get("title")
    new_todo = Todo(title=title,complete=False)
    #add to database
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index")) #redirect to "index" page

@app.route("/update/<int:todo_id>")
def update(todo_id):
    #query our database
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    #query our database
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

# #about page
# @app.route('/about')
# def about():
#     return "About"

#========== MAIN ===========
if __name__ == "__main__":
    #create our database
    with app.app_context():
        db.create_all()
        #add object to our database
        new_todo = Todo(title = 'todo 1',complete = False)
        db.session.add(new_todo)
        db.session.commit()

        app.run(debug=True)