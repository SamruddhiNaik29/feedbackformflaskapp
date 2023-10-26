# app.py
from flask import Flask, render_template, request, redirect, url_for, session,flash

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.secret_key = 'your_secret_key'  # Change this to a random, secure key
db = SQLAlchemy(app)







# Add this import at the top
from datetime import datetime

# Feedback model
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question1 = db.Column(db.String(255), nullable=False)
    question2 = db.Column(db.String(255), nullable=False)
    question3 = db.Column(db.String(255), nullable=False)
    question4 = db.Column(db.String(255), nullable=False)
    question5 = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():    

# Create the database tables
 db.create_all()
# Add this import at the top
from flask import redirect, url_for

# Feedback route
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        user_id = session.get('user_id')
        if user_id:
            question1 = request.form['question1']
            question2 = request.form['question2']
            question3 = request.form['question3']
            question4 = request.form['question4']
            question5 = request.form['question5']

            new_feedback = Feedback(user_id=user_id, question1=question1, question2=question2, question3=question3, question4=question4, question5=question5)
            db.session.add(new_feedback)
            db.session.commit()

            flash('Feedback submitted successfully. Thank you!', 'success')
            return redirect(url_for('feedback_confirmation'))
        else:
            flash('Please log in to submit feedback.', 'danger')

    return render_template('feedback.html')

# Feedback confirmation route
@app.route('/feedback/confirmation')
def feedback_confirmation():
    return render_template('feedback_confirmation.html')
if __name__ == '__main__':
    app.run(debug=True)
