from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from werkzeug.datastructures import RequestCacheControl

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class ToDo(db.Model):
    sno =db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(2000), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)


    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method=='POST':
        todo_title = request.form['title']
        todo_desc = request.form['desc'] 
        todo = ToDo(title = todo_title, desc = todo_desc)
        db.session.add(todo)
        db.session.commit()
    allTodo = ToDo.query.all()
    # print(allTodo)
    return render_template('index.html', allTodo = allTodo)

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        todo_title = request.form['title']
        todo_desc = request.form['desc'] 
        todo = ToDo.query.filter_by(sno = sno).first()
        todo.title = todo_title
        todo.desc = todo_desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    todo = ToDo.query.filter_by(sno = sno).first()
    return render_template('update.html',todo = todo)


@app.route('/delete/<int:sno>')
def delete(sno):
    todo = ToDo.query.filter_by(sno = sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=8000)