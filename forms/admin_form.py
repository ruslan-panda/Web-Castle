from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, SelectField ,IntegerField
from wtforms.validators import DataRequired


class AdminForm(FlaskForm):
    paid = IntegerField("Введите новую сумму", default=1)
    grade_list = ["На обработке", "Закончена", "Не закончена"]
    status = SelectField("Статус готоности", choices=grade_list, validators=[DataRequired()])
    submit = SubmitField("Выставить условия")
