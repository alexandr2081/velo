import json
import sqlalchemy as sqlal #type: ignore
from flask_wtf import FlaskForm #type: ignore
from wtforms import PasswordField, StringField, SubmitField, EmailField, BooleanField, TextAreaField, RadioField #type: ignore
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo #type: ignore
from data.users import User
from data.details import Detail
from data.db_session import create_session



class LoginForm(FlaskForm):
    email_log = EmailField('Почта или логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    name = StringField('Логин пользователя', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password', message='Пароли должны совпадать')])
    submit = SubmitField('Создать пользователя')

    def validate_email(self, email):
        db_sess = create_session()
        user = db_sess.scalar(sqlal.select(User).where(User.email == email.data))
        if user is not None:
            raise ValidationError('Пожалуйста, выберите другой адрес электронной почты')

    def validate_login(self, name):
        db_sess = create_session()
        if db_sess.scalar(sqlal.select(User).where(User.name == name.data)) is not None:
            raise ValidationError('Пожалуйста, выберите другой логин')
        
class RegisterFormAdmin(FlaskForm):
    name = StringField('Имя пользователя', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    code = StringField('Кодовое слово', validators=[DataRequired()])
    submit = SubmitField('Создать пользователя')

    def validate_admin(self, code):
        if code != 'ADMIN_REGISTER':
            raise ValidationError('Неправильное кодовое слово')

    def validate_email(self, email):
        db_sess = create_session()
        user = db_sess.scalar(sqlal.select(User).where(User.email == email.data))
        if user is not None:
            raise ValidationError('Пожалуйста, выберите другой адрес электронной почты')


class UpDetForm(FlaskForm):
    with open('./static/chars.json', 'r', encoding='utf-8') as ch, open('./static/types.json', 'r', encoding='utf-8') as ty:
        ch, ty = json.load(ch), json.load(ty)
    name = StringField('Название детали')
    type = RadioField('Тип детали', choices=ty.keys())
    material = RadioField('Материал изготовления', choices=[i for i in ch['material'].keys()])
    manufacture = RadioField('Изготовитель', choices=[i for i in ch['manufacture'].keys()])
    level = RadioField('Уровень детали', choices=[i for i in ch['level'].keys()])
    color = RadioField('Цвет детали', choices=ch['color'])
    price = StringField('Цена детали')
    descript = TextAreaField('Описание детали')
    weight = StringField('Вес детали')
    img = StringField('Ссылка на картинку детали')
    img_velo = StringField('Ссылка на картинку наложения на велосипед')
    available = StringField('Доступность (наличие на складе)')
    submit = SubmitField('Изменить деталь')

    def validate_name(self, name):
        db_sess = create_session()
        det = db_sess.scalar(sqlal.select(Detail).where(Detail.name == name.data))
        if det == None:
            raise ValidationError('Пожалуйста, проверьте имя детали - такой нету в базе данных')


class DelDetForm(FlaskForm):
    name = StringField('Название детали', validators=[DataRequired()])
    submit = SubmitField('Удалить деталь')

    def validate_name(self, name):
        db_sess = create_session()
        det = db_sess.scalar(sqlal.select(Detail).where(Detail.name == name.data))
        if det == None:
            raise ValidationError('Детали с таким именем нету в базе данных')


# class UpDetForm(FlaskForm):
#     name = StringField('Название детали', validators=[DataRequired()])
#     old_par = StringField('Название изменяемого параметра', validators=[DataRequired()])
#     new_par = StringField('Новый параметр', validators=[DataRequired()])
#     submit = SubmitField('Заменить параметр детали')

#     def validate_name(self, name):
#         db_sess = create_session()
#         det = db_sess.scalar(sqlal.select(Detail).where(Detail.name == name.data))
#         if det == None:
#             raise ValidationError('Детали с таким именем нету в базе данных')