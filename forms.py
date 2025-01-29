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


# class NewDetForm(FlaskForm):
#     with open('./static/chars.json', 'r', encoding='utf-8') as ch, open('./static/types.json', 'r', encoding='utf-8') as ty:
#         ch, ty = json.load(ch), json.load(ty)
#     type = RadioField('Тип детали', validators=[DataRequired()], choices=ty.keys())
#     material = RadioField('Материал изготовления', validators=[DataRequired()], choices=[i for i in ch['material'].keys()])
#     manufacture = RadioField('Изготовитель', validators=[DataRequired()], choices=[i for i in ch['manufacture'].keys()])
#     level = RadioField('Уровень детали', validators=[DataRequired()], choices=[i for i in ch['level'].keys()])
#     color = RadioField('Цвет детали', validators=[DataRequired()], choices=ch['color'])

#     name = StringField('Название детали', validators=[DataRequired()])
#     price = StringField('Цена детали', validators=[DataRequired()])
#     descript = TextAreaField('Описание детали', validators=[DataRequired()])
#     weight = StringField('Вес детали', validators=[DataRequired()])
#     size = StringField('Размер детали (указывать в виде длина*ширина*высота)', validators=[DataRequired()])
#     img = StringField('Ссылка на картинку детали', validators=[DataRequired()])
#     img_velo = StringField('Ссылка на картинку наложения на велосипед', validators=[DataRequired()])
#     available = StringField('Доступность (наличие на складе)', validators=[DataRequired()])
#     submit = SubmitField('Создать деталь')

#     def validate_name(self, name):
#         db_sess = create_session()
#         det = db_sess.scalar(sqlal.select(Detail).where(Detail.name == name.data))
#         if det is not None:
#             raise ValidationError('Пожалуйста, выберите другое имя детали')


class DelDetForm(FlaskForm):
    name = StringField('Название детали', validators=[DataRequired()])
    submit = SubmitField('Удалить деталь')

    def validate_name(self, name):
        db_sess = create_session()
        det = db_sess.scalar(sqlal.select(Detail).where(Detail.name == name.data))
        if det == None:
            raise ValidationError('Детали с таким именем нету в базе данных')


class UpDetForm(FlaskForm):
    name = StringField('Название детали', validators=[DataRequired()])
    old_par = StringField('Название изменяемого параметра', validators=[DataRequired()])
    new_par = StringField('Новый параметр', validators=[DataRequired()])
    submit = SubmitField('Заменить параметр детали')

    def validate_name(self, name):
        db_sess = create_session()
        det = db_sess.scalar(sqlal.select(Detail).where(Detail.name == name.data))
        if det == None:
            raise ValidationError('Детали с таким именем нету в базе данных')
        
# class NewBuildForm(FlaskForm):
#     if True:
#         name = StringField('Название сборки', validators=[DataRequired()])
#         frame = StringField('Название рамы')
#         rear_shock_absorber = StringField('Название заднего амортизатора')
#         fork = StringField('Название ')
#         steering_column = StringField('Название ')
#         steering_wheel_removal = StringField('Название ')
#         handlebar = StringField('Название ')
#         grieps = StringField('Название ')
#         front_wheel = StringField('Название ')
#         rear_wheel = StringField('Название ')
#         front_tire = StringField('Название ')
#         rear_tire = StringField('Название ')
#         front_bushing = StringField('Название ')
#         rear_bushing = StringField('Название ')
#         chain = StringField('Название ')
#         rear_stars = StringField('Название ')
#         rear_speed_switch = StringField('Название ')
#         front_speed_switch = StringField('Название ')
#         rear_break = StringField('Название ')
#         front_break = StringField('Название ')
#         rear_break_disk = StringField('Название ')
#         front_break_disk = StringField('Название ')
#         bottom_bracket = StringField('Название ')
#         front_stars = StringField('Название ')
#         rod = StringField('Название ')
#         pedals = StringField('Название ')
#         saddle = StringField('Название ')
#         seat = StringField('Название ')
#         no_type_1 = StringField('Деталь без типа 1')
#         no_type_2 = StringField('Деталь без типа 2')
#         no_type_3 = StringField('Деталь без типа 3')
#         submit = SubmitField('Создать сборку')

#         def validate_details(self, frame, rear_shock_absorber, fork, steering_column, steering_wheel_removal, handlebar,
#                              grieps, front_wheel, rear_wheel, front_tire, rear_tire, front_bushing, rear_bushing, chain,
#                              rear_stars, rear_speed_switch, front_speed_switch, rear_break, front_break, rear_break_disk,
#                              front_rear_disk, bottom_bracket, front_stars, rod, pedals, saddle, seat, no_type_1, no_type_2, no_type_3):
#             db_sess = create_session()
#             for i in [frame, rear_shock_absorber, fork, steering_column, steering_wheel_removal, handlebar, grieps,
#                       front_wheel, rear_wheel, front_tire, rear_tire, front_bushing, rear_bushing, chain, rear_stars,
#                       rear_speed_switch, front_speed_switch, rear_break, front_break, rear_break_disk, front_rear_disk,
#                       bottom_bracket, front_stars, rod, pedals, saddle, seat, no_type_1, no_type_2, no_type_3]:
#                 det = db_sess.scalar(sqlal.select(Detail).where(Detail.name == i.data))
#                 if det == None:
#                     raise ValidationError(f'Детали {i.data} нету в базе данных')
