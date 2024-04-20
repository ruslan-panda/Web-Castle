from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api
from data import db_session
from forms.register_form import RegisterForm
from data.users import User
from forms.user_from import LoginForm
from forms.order_form import OrderForm
from forms.review_form import ReviewForm
from data.orders import Order
from data.reviews import Review

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
#api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/form_sample', methods=['GET', 'POST'])
def form_sample():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('registr.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('registr.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            login=form.login.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect("/index")
    return render_template('registr.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/index")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)



@app.route('/order', methods=['GET', 'POST'])
def order():
    form = OrderForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        order = Order(
            name_order=form.name_order.data,
            text=form.text.data,
            teg=form.teg.data,
            user_id=current_user.id
        )
        db_sess.add(order)
        db_sess.commit()
        return redirect("/index")
    return render_template('order.html', title='формление заказа', form=form)


@app.route('/review', methods=['GET', 'POST'])
def review():
    form = ReviewForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        review = Review(
            text=form.text.data,
            grade=form.grade.data,
        )
        db_sess.add(review)
        db_sess.commit()
    return render_template("review.html", title="", form=form)

# http://127.0.0.1:8080//sample_file_upload
if __name__ == '__main__':
    db_session.global_init("db/jobs.db")
    app.run(port=8080, host='127.0.0.1')
