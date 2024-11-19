from flask import Flask, render_template
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

    def __str__(self) -> str:
        return f"Task {self.id}"

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/testing')
def testing():
    return render_template('testing.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)