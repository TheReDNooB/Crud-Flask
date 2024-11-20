from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
Scss(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

# data Class
class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(50), nullable=False)
    complete = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"Task {self.id}"

@app.route('/',methods=["POST","GET"])
def home():
    # add task
    if request.method=="POST":
        current_task = request.form['content']  
        new_task = MyTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(f"Error: {e}")
            return f"Error: {e}"
        # see all task
    else:
        tasks = MyTask.query.order_by(MyTask.created_at).all()
        return render_template('home.html', tasks=tasks)


@app.route("/delete/<int:id>")
def delete(id:int):
    delete_task = MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return f"Error: {e}"
    
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id:int):
    update_task = MyTask.query.get_or_404(id)
    if request.method == "POST":
        update_task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"Error: {e}"
    else:
        return render_template('update.html', update_task=update_task)


if __name__ in '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)