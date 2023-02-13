from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField
from wtforms.validators import Email, InputRequired


class RegisterForm(FlaskForm):
    name = StringField(label=("Name"),  validators=[
                           InputRequired("Name is required.")])
    email = StringField(label=('Email'), validators=[Email(), InputRequired("Email is required.")])
    password = StringField(label=('Password'), validators=[
                           InputRequired("Password is required.")])
    submit = SubmitField(label=('Sign up'))


class LoginForm(FlaskForm):
    email = StringField(label=("Email"),  validators=[
                           InputRequired(message="Email is required.")])
    password = StringField(label=('Password'), validators=[
                           InputRequired("Password is required.")])
    submit = SubmitField(label=('Sign in'))


class AddListForm(FlaskForm):
    name = StringField(label=("Name"), validators=[InputRequired(message="Name is required.")])
    submit = SubmitField("Add")

class EditListForm(FlaskForm):
    name = StringField(label=("Name"), validators=[InputRequired(message="Name is required.")])
    submit = SubmitField("Update")

class AddCardForm(FlaskForm):
    title = StringField(label=("Title"), validators=[InputRequired(message="Title is required.")])
    content = StringField(label=("Content"), validators=[InputRequired(message="Content is required.")])
    deadline = DateField(label=("Deadline"), validators=[InputRequired(message="Deadline is required.")])
    completed = SelectField(u'Completed', choices=[(0, 'No'), (1, 'Yes')])
    submit = SubmitField("Add")

    
    # def validate_deadline(form, field):
    #     if field.data < date.today():
    #         raise ValidationError('Select the date greater than yesterday.')

class EditCardForm(FlaskForm):
    list = SelectField(u'List')
    title = StringField(label=("Title"), validators=[InputRequired(message="Title is required.")])
    content = StringField(label=("Content"), validators=[InputRequired(message="Content is required.")])
    deadline = DateField(label=("Deadline"), validators=[InputRequired(message="Deadline is required.")])
    completed = SelectField(u'Completed', choices=[(0, 'No'), (1, 'Yes')])
    submit = SubmitField("Update")
