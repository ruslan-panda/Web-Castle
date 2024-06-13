from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api
import random
from data.db_session import create_session, global_init
from forms.register_form import RegisterForm
from data.users import User
from forms.login_form import LoginForm
from forms.admin_form import AdminForm
from forms.order_form import OrderForm
from forms.review_form import ReviewForm
from data.orders import Order
from data.reviews import Review

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
# api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/info_user/<int:id>", methods=['GET', 'POST'])
def info(id):
    db_sess = create_session()
    us = db_sess.query(User).filter(User.id == id).all()
    user = [{"id": i.id, "login": i.login, "email": i.email, "position": i.position, "invitation_key": i.invitation_key}
            for i in us]
    user = user[0]
    print(user)
    return render_template("info.html", user=user)


@login_manager.user_loader
def load_user(user_id):
    db_sess = create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/form_sample', methods=['GET', 'POST'])
def form_sample():
    form = RegisterForm()
    db_sess = create_session()
    invitation_key = db_sess.query(User).filter(User.invitation_key).all()
    ik = [i.invitation_key for i in invitation_key]
    print(ik)
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('registr.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('registr.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        db_sess = create_session()
        if form.invitation_key.data == "admin":
            ad = 1
        elif form.invitation_key.data == "":
            ad = 0
        elif form.invitation_key.data not in ik:
            return render_template('registr.html', title='Регистрация', form=form,
                                   message="Несуществующий код")
        else:
            ad = 0
        chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        key = str(random.randint(0, 9))
        for i in range(10):
            key += random.choice(chars)
        user = User(
            login=form.login.data,
            email=form.email.data,
            position=form.position.data,
            admin=ad,
            invitation_key=key
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
        db_sess = create_session()
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
        db_sess = create_session()
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


@app.route('/review/<int:id>', methods=['GET', 'POST'])
def review(id):
    form = ReviewForm()
    if form.validate_on_submit():
        db_sess = create_session()
        review = Review(
            text=form.text.data,
            grade=form.grade.data,
            order_id=id
        )
        db_sess.add(review)
        db_sess.commit()
        return redirect("/index")
    return render_template("review.html", title="", form=form)


@app.route("/orders")
def orders():
    db_sess = create_session()
    jobs = db_sess.query(Order).filter(Order.user_id == current_user.id).all()
    review = db_sess.query(Review).filter(Review.order_id).all()
    review = [i.order_id for i in review]
    return render_template("all_order.html", jobs=jobs, names=current_user.login, review=review, title='Работы')


@app.route("/reviews")
def reviews():
    db_sess = create_session()
    review = db_sess.query(Review).all()
    users = db_sess.query(User).all()
    names = {name.id: (name.login, name.position) for name in users}
    orders = db_sess.query(Order).all()
    order = {order.id: names[order.user_id][0] for order in orders}
    position = {pos.id: names[pos.user_id][1] for pos in orders}
    return render_template("all_review.html", jobs=review, names=order, pos=position, title='Отзывы')


@app.route("/admins")
def admins():
    db_sess = create_session()
    jobs = db_sess.query(Order).all()
    users = db_sess.query(User).all()
    names = {name.id: (name.login, name.position) for name in users}
    orders = db_sess.query(Order).all()
    order = {order.id: names[order.user_id][0] for order in orders}
    print(jobs)
    return render_template("admins.html", jobs=jobs, names=order, title='Работы')

@app.route("/admin_edit_order/<int:id_order>", methods=['GET', 'POST'])
def admin_ed(id_order):
    form = AdminForm()
    db_sess = create_session()
    jobs = db_sess.query(Order).filter(Order.id == id_order).all()
    users = db_sess.query(User).all()
    names = {name.id: (name.login, name.position) for name in users}
    orders = db_sess.query(Order).all()
    order = {order.id: names[order.user_id][0] for order in orders}
    if form.validate_on_submit():
        print(12345)
        return redirect("/agmins")
    return render_template("admin_ed.html", jobs=jobs, names=order, form=form)

# http://127.0.0.1:8080//sample_file_upload
if __name__ == '__main__':
    global_init("db/jobs.db")
    app.run(port=8080, host='127.0.0.1')
