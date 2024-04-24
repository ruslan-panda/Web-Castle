from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, SelectField
from wtforms.validators import DataRequired


class OrderForm(FlaskForm):
    name_order = StringField('Название заказа', validators=[DataRequired()])
    text = StringField("Описание заказа", validators=[DataRequired()])
    drop_list = ["Веб-аналитика", "Веб-дизайн", "SEO-услуги", "Fullstack-разработка"]
    teg = SelectField('выберте тег', choices=drop_list, validators=[DataRequired()])
    post_order = SubmitField('Отправить заказ на обработку')
