from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api
from data import db_session
from forms.register import RegisterForm
from data.user import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
#api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
@app.route('/index')
def index():
    return ""

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

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
        return redirect()
    return render_template('registr.html', title='Регистрация', form=form)


# http://127.0.0.1:8080//sample_file_upload
if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
