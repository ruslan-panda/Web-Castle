from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, SelectField
from wtforms.validators import DataRequired


class ReviewForm(FlaskForm):
    text = StringField("Напишите отзыв", validators=[DataRequired()])
    grade_list = [1, 2, 3, 4, 5]
    grade = SelectField("Оценка", choices=grade_list, validators=[DataRequired()])
    post_review = SubmitField("Отправить отзыв")
