import os, json
from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from flask_login import LoginManager, logout_user, login_required, current_user, login_user
import sqlalchemy as sqlal
from data import db_session
from data.details import Detail
from data.users import User
from data.builds import Build
from forms import LoginForm, RegisterForm, RegisterFormAdmin, DelDetForm, UpDetForm
from fileinput import filename
from io import BytesIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'custom_bike'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def get_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


def get_js(TC):
    if TC == 'types':
        with open(f'static/types.json', encoding="utf8") as f: return json.load(f)
    if TC == 'chars':
        with open(f'static/chars.json', encoding="utf8") as f: return json.load(f)


def dets_bui(dets_id):
    bui, db_sess, types = {'name': 'Сборка'}, db_session.create_session(), get_js('types')
    bui['price'], bui['weight'], bui['details'], bui['detid'], bui['imgs'] = 0, 0, {}, '', []
    if dets_id:
        for det_id in dets_id.split():
            det, k = db_sess.query(Detail).filter(Detail.id == det_id).first(), True
            if det and list(types.keys())[int(det.type)] not in bui['details'].keys():
                bui['details'][list(types.keys())[int(det.type)]] = det.name
                bui['imgs'].append(det.img_velo)
                bui['price'] += int(det.price)
                bui['weight'] += int(det.weight)
                bui['detid'] += ' ' + str(det.id)
        bui['weight'] = f"{bui['weight'] // 1000} кг, {bui['weight'] % 1000} гр"
    db_sess.close()
    return bui


@app.route('/<dets_id>', methods=['GET', 'POST'])
@app.route('/index/<dets_id>', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index(dets_id=''):
    db_sess, chars, types, build_ = db_session.create_session(), get_js('chars'), get_js('types'), {'name': 'Сборка'}
    db, det, message, dets = lambda que: [json.loads(str(i)) for i in que], None, '', ''
    build_['price'], build_['weight'], build_['details'] = 0, 0, {}
    details, build_ = db(db_sess.query(Detail).group_by(Detail.name)), dets_bui(dets_id)
    filters = request.form.get('filters') if request.form.get('filters') else "{}"

    if request.method == 'POST':
        dets, build_ = {}, dets_bui(request.form.get('output'))
        if request.form['build_sub'] == 'new_build':
            tf = '\\' in request.form.get('build_name') or '.' in request.form.get('build_name')
            if tf or '/' in request.form.get('build_name'):
                return render_template('velo_index.html', details=details, types=types, chars=chars, title='Главная',
                                build_=build_, message='Название сборки не должно содержать символов "/", "\", "."')
            else: build_['name'] = request.form.get('build_name')

            build = Build(name=request.form.get('build_name'))
            for i in request.form.get('output').split(): dets[db_sess.query(Detail).filter(Detail.id == i).first().type] = i
            build.details, build.user_name = ' '.join(dets.values()), current_user.name
            if 'is_open' in request.form.keys(): build.is_open = True
            else: build.is_open = False
            db_sess.add(build)
    db_sess.commit()
    db_sess.close()
    return render_template('velo_index.html', details=details, types=types, chars=chars, title='Главная',
                           build_=build_, message=message, filters=filters)


@app.route('/about_us')
def about_us():
    return render_template('about_us.html')


@app.route('/about_det/<det_name>')
@login_required
def about_det(det_name):
    db_sess, chars, types = db_session.create_session(), get_js('chars'), get_js('types')
    det = json.loads(str(db_sess.query(Detail).filter(Detail.name == det_name)[0]))
    db_sess.close()
    det['weight'] = f'Вес: {int(det["weight"]) // 1000} кг, {int(det["weight"]) % 1000} гр'
    det['param'] = ' '.join([f'{list(types[det["type"]].keys())[ch]}: {det["param"][ch]}'
                             for ch in range(len(types[det['type']].keys()))])
    return render_template('about_det.html', title=det_name, det=det, chars=chars, types=types)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if '@' in form.email_log.data: user = db_sess.query(User).filter(User.email == form.email_log.data).first()
        else: user = db_sess.query(User).filter(User.name == form.email_log.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('index'))
        db_sess.close()
        return render_template('login.html', message="Неправильный email (имя) или пароль", form=form)
    return render_template('login.html', title='Вход', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if 'admin' in form.name.data:
            return redirect(url_for('register_adm'))
        db_sess, email = db_session.create_session(), form.email.data
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message='Такой пользователь уже есть (Измените email, или попробуйте войти)')
        if '@' in form.name.data or '/' in form.name.data or '.' in form.name.data or '\\' in form.name.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message='Имя пользователя не должно содержать символов ".", "@", "/", "\"')
        user = User(name=form.name.data, email=form.email.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/register_adm', methods=['GET', 'POST'])
def register_adm():
    form = RegisterFormAdmin()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        if form.code.data != 'ADMIN_REGISTER':
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Не угадал)")
        user = User(name=form.name.data, email=form.email.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect(url_for('login'))
    return render_template('register_adm.html', title='Регистрация', form=form, message='Ну, пробуй')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/new_det', methods=['GET', 'POST'])
@login_required
def new_det():
    if 'admin' in current_user.name:
        db_sess = db_session.create_session()
        types = get_js('types'); chars = get_js('chars')
        if request.method == 'POST':
            if db_sess.query(Detail).filter(Detail.name == request.form.get('name')).first():
                return render_template('new_det.html', title='Создание новой детали', types=types,
                                       chars=chars, message='Деталь с таким именем уже есть в БД')

            det = Detail()
            det.type = list(types.keys()).index(request.form.get('type'))
            det.name = request.form.get('name')
            det.price = int(request.form.get('price'))
            det.descript = request.form.get('descript')
            det.weight = int(request.form.get('weight'))
            det.material = [i for i in chars["material"].keys()].index(request.form.get('material'))
            det.color = chars["color"].index(request.form.get('color'))
            det.manufacture = [i for i in chars["manufacture"].keys()].index(request.form.get('manufacture'))
            det.img = request.form.get('img')
            det.img_velo = request.form.get('img_velo')
            det.available = request.form.get('available')
            det.level = [i for i in chars["level"].keys()].index(request.form.get('level'))
            det.param = '~'.join([request.form.get(i) for i in types[request.form.get('type')].keys()])

            db_sess.add(det)
            db_sess.commit()
            return redirect(url_for('index'))
        return render_template('new_det.html', title='Создание новой детали', types=types, chars=chars)
    else: return redirect(url_for('index'))


@app.route('/up_det', methods=['GET', 'POST'])
@login_required
def up_det():
    if 'admin' in current_user.name:
        form = UpDetForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            old_det = db_sess.query(Detail).where(Detail.name == form.name.data).first()
            if old_det:
                if not form.name.data:
                    
                    db_sess.commit()
            else: return redirect(url_for('new_det'))
        else: return render_template('up_det.html', title='Изменение детали', form=form)
    else: return redirect(url_for('index'))
    

@app.route('/del_det', methods=['GET', 'POST'])
@login_required
def del_det():
    if 'admin' in current_user.name:
        form = DelDetForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            det = db_sess.query(Detail).filter(Detail.name == form.name.data).first()
            db_sess.delete(det)
            db_sess.commit()
            return redirect(url_for('index'))
        else: return render_template('del_det.html', title='Удаление детали', form=form)
    else: return redirect(url_for('index'))


@app.route('/ready_builds')
@login_required
def ready_builds():
    builds, db_sess = [], db_session.create_session()
    for build in [json.loads(str(i)) for i in db_sess.query(Build).filter(Build.is_open)]:
        build['details'], build['price'], build['weight'], details_id = {}, 0, 0, build['details']
        for det_id in details_id:
            det = db_sess.query(Detail).filter(Detail.id == det_id).first()
            build['details'][det.type] = det.name
            build['price'] += int(det.price)
            build['weight'] += int(det.weight)
        build['weight'] = f"{build['weight'] // 1000} кг, {build['weight'] % 1000} гр"
        builds.append(build)
    return render_template('ready_builds.html', title='Общие сборки', builds=builds)


@app.route('/your_builds', methods=['GET', 'POST'])
@login_required
def your_builds():
    builds, db_sess, types, chars = [], db_session.create_session(), get_js('types'), get_js('chars')
    if request.method == 'POST':
        if request.files.get('file'):
            return redirect(url_for('index', dets_id=request.files['file'].read().decode('utf-8')))
        if 'del_id' in str(request.form.keys()):
            del_que = db_sess.query(Build).filter(Build.id == int(request.form['del_id']))
            db_sess.delete(del_que.first())
        elif 'down_id' in str(request.form.keys()):
            down_bui = db_sess.query(Build).filter(Build.id == int(request.form['down_id'])).first()
            down_buff = BytesIO(bytes(down_bui.details, encoding='utf8'))
            down_buff.seek(0)
            return send_file(down_buff, as_attachment=True, download_name=down_bui.name + '.txt')

    if 'admin' in current_user.name: que = db_sess.query(Build).all()
    else: que = db_sess.query(Build).filter(Build.user_name == current_user.name).all()
    for build in [json.loads(str(i)) for i in que]:
        build['details'], dets_id, build['weight'], build['price'] = {}, build['details'], 0, 0
        for det_id in dets_id:
            det = db_sess.query(Detail).filter(Detail.id == det_id).first()
            build['details'][list(types.keys())[int(det.type)]] = det.name
            build['price'] += int(det.price)
            build['weight'] += int(det.weight)
        build['weight'] = f"{build['weight'] // 1000} кг, {build['weight'] % 1000} гр"
        del build['is_open']
        builds.append(build)
    db_sess.commit()
    db_sess.close()
    return render_template('your_builds.html', title='Ваши сборки', builds=builds)


@app.route('/chars_types', methods=['GET', 'POST'])
@login_required
def chars_types():
    if 'admin' in current_user.name:
        if request.method == 'POST':
            if request.files.get('up_chars'):
                with open('static\\chars.json', 'w', encoding='utf-8') as f:
                    f.write(request.files.get('up_chars').read().decode('utf-8').replace('\r\n', '\n'))
            if request.files.get('up_types'):
                with open('static\\types.json', 'w', encoding='utf-8') as f:
                    f.write(request.files.get('up_types').read().decode('utf-8').replace('\r\n', '\n'))
            if request.form.get('down_chars'): return send_file('static\\chars.json', as_attachment=True)
            if request.form.get('down_types'): return send_file('static\\types.json', as_attachment=True)
        return render_template('types_chars.html', title='Полное изменение характеристик (ОСТОРОЖНО!!!)')
    return redirect(url_for('index'))


if __name__ == '__main__':
    db_session.global_init("db/velo.db")
    app.run(port=8080, host='127.0.0.1')
