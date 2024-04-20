from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField
from wtforms.validators import DataRequired


class OrderForm(FlaskForm):
    name_order = StringField('Название заказа', validators=[DataRequired()])
    text = StringField("Описание заказа", validators=[DataRequired()])
    teg = StringField('выберте тег', validators=[DataRequired()])
    post_order = SubmitField('Отправить заказ на обработку')