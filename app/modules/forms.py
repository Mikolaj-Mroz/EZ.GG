from flask_wtf import FlaskForm 
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired


class SearchPlayer(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    server = SelectField('Server', validators=[DataRequired()], choices=[('eun1', 'Europe Nordic & East'), ('euw1','Europe West'), ('na1','North America')])
