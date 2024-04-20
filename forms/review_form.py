from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, IntegerField
from wtforms.validators import DataRequired


class ReviewForm(FlaskForm):
    text = StringField("Напишите отзыв", validators=[DataRequired()])
    grade = IntegerField("Оценка", validators=[DataRequired()])
    post_review = SubmitField("Отправить отзыв")