from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, ValidationError, Length
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "My_Secret_Key"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db = SQLAlchemy(app)



class FormData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phn_no = db.Column(db.Integer, nullable=False)
    message =db.Column(db.String(500), nullable=False)

with app.app_context():
   db.create_all()


class FlaskForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phn_no = IntegerField("Phone Number", validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=15)])
    submit = SubmitField("Submit")
    
    def validate_email(self, field):
        existing_email = FormData.query.filter_by(email=field.data).first()
        if existing_email:
            raise ValidationError("Email must be unique")
        
  
@app.route("/", methods=[ 'POST', 'GET'])
def index():
    form = FlaskForm()
    if request.method == "POST" and form.validate_on_submit():
        
        # fetching data from table 
        name = form.name.data
        email = form.email.data
        phn_no = form.phn_no.data
        message = form.message.data
        
        # save into database
        form_data = FormData(name=name, email=email, phn_no=phn_no, message=message)
        db.session.add(form_data)
        db.session.commit()
        return "Success"
         
    return render_template('index.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)