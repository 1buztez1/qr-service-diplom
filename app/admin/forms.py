from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class AddUserForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    l_name = StringField('Фамилия', validators=[DataRequired(), Length(max=32)])
    f_name = StringField('Имя', validators=[DataRequired(), Length(max=32)])
    m_name = StringField('Отчество', validators=[Length(max=32)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])
    group_id = SelectField('Группа', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Добавить пользователя')