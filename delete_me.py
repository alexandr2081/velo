
#    <!--{% if img_z != {} %}
#      {% for img in img_z.keys() %}
#        <img src='{{img}}' alt="Что-то пошло не так" id="img" style="position: absolute;">
#        <script>document.getElementById('img').style.zIndex = "{{img_z[img]}}"</script>
#      {% endfor %}
#      <img src="https://sevgorsovet.ru/wp-content/uploads/bfi_thumb/dummy-transparent-n9hbhmo1xwe1dlf3a3x0juiutxfkx0xejnnxrhhn34.png">
#    {% endif %}-->
#            <!--{% if dict['type'] in ["Шина", "Камера", "Тормоз", "Тормозной диск"] %}
#              <a onclick="togglePopup('rear_front_popup')"
#                class="btn btn-primary" id="app_det">Добавить деталь в сборку</a>
#                <div id="rear_front_popup" class="overlay-container">
#                <div class="popup-box">
#                  <h2 style="color: green;">Создание</h2>
#                  <div class="form-container">
#                      <label class="form-label">Выберите, будет ли деталь задней или передней</label>
#                      <input class="form-check-input" type="radio" value="rear" name="rear_front">
#                      <label class="form-check-label">Задняя</label>
#                      <input class="form-check-input" type="radio" value="front" name="rear_front">
#                      <label class="form-check-label">Передняя</label>
#                      {% for id in [dict['id']] %}
#                        <button class="btn-submit" onclick="func_app('{{id}}')">Добавить деталь в сборку</button>
#                      {% endfor %}
#                    </div>
#                  </div>
#                </div>
#            {% else %}-->
#import timeit
####print(timeit.timeit('''''', number=1000)
##import json
##from flask import Flask, render_template, request, redirect, url_for
##from flask_login import LoginManager, logout_user, login_required, current_user, login_user
##import sqlalchemy as sqlal
##from data import db_session
##from data.details import Detail
##from data.users import User
##from data.builds import Build
##from forms import LoginForm, RegisterForm, RegisterFormAdmin, DelDetForm, UpDetForm
##
##app = Flask(__name__)
##app.config['SECRET_KEY'] = 'custom_bike'
##login_manager = LoginManager()
##login_manager.init_app(app)
##
##
##@login_manager.user_loader
##def get_user(user_id):
##    db_sess = db_session.create_session()
##    return db_sess.get(User, user_id)
##
##
##def get_js(TC):
##    if TC == 'types':
##        with open(f'static/types.json', encoding="utf8") as f: return json.load(f)
##    if TC == 'chars':
##        with open(f'static/chars.json', encoding="utf8") as f: return json.load(f)
##
##
##def db(table=Detail, filt=[], req=[], group=Detail.name):
##    db_sess, I = db_session.create_session(), min(len(filt), len(req))
##    if req and filt:
##        N = {str(i) for i in db_sess.query(table).filter(filt[0] == req[0]).group_by(group)}
##        for i in range(1, I): N = N & {str(i) for j in db_sess.query(table).filter(filt[i] == req[i])}
##        db_sess.close()
##        return [json.loads(str(i)) for i in N]
##    else:
##        return [json.loads(str(i)) for i in db_sess.query(table).group_by(group)]
##    db_sess.close()
##
##
##@app.route('/<build_id>', methods=['GET', 'POST'])
##@app.route('/index/<build_id>', methods=['GET', 'POST'])
##@app.route('/', methods=['GET', 'POST'])
##@app.route('/index', methods=['GET', 'POST'])
##def index(build_id=''):
##    db_sess, chars, types, build_details = db_session.create_session(), get_js('chars'), get_js('types'), {}
##    build_details['price'], build_details['weight'] = 0, 0
##    details = [json.loads(str(i)) for i in db_sess.query(Detail).group_by(Detail.name)]
##
##    if request.method == 'POST':
##        out = request.form.get('output')
##        for det_id in request.form.get('output').split():
##            det = [json.loads(str(i)) for i in db_sess.query(Detail).filter(Detail.id == det_id).group_by(Detail.name)][0]
##            build_details[det['type']] = det['name']
##            build_details['price'] += int(det['price'])
##            build_details['weight'] += int(det['weight'])
##        build_details['weight'] = f"{build_details['weight'] // 1000} кг, {build_details['weight'] % 1000} гр"
##        if request.form['build_sub'] == 'new_build':
##            build, build.details = Build(), ''
##            build.name = request.form.get('build_name')
##            for i in request.form.get('output'):
##                if i.isDigit(): build.details += i
##            if request.form.get('is_open'): build.is_open = True
##            else: build.is_open = False
##            build.user_id = db(table=User, filt=[User.name], req=[current_user.name])
##
##    db_sess.close()
##    return render_template('velo_index.html', details=details, types=types, chars=chars,
##                           title='Главная', build_details=build_details)
##
##
##@app.route('/about_us')
##def about_us():
##    return render_template('about_us.html')
##
##
##@app.route('/about_det/<det_name>')
##@login_required
##def about_det(det_name):
##    return render_template('about_det.html', title=det_name)
##
##
##@app.route('/login', methods=['GET', 'POST'])
##def login():
##    form = LoginForm()
##    if form.validate_on_submit():
##        db_sess = db_session.create_session()
##        user = db_sess.query(User).filter(User.email == form.email.data).first()
##        if user and user.check_password(form.password.data):
##            login_user(user, remember=form.remember_me.data)
##            return redirect(url_for('index'))
##        db_sess.close()
##        return render_template('login.html', message="Неправильный логин или пароль", form=form)
##    return render_template('login.html', title='Вход', form=form)
##
##
##@app.route('/register', methods=['GET', 'POST'])
##def reqister():
##    form = RegisterForm()
##    if form.validate_on_submit():
##        if 'admin' in form.name.data:
##            return redirect(url_for('register_adm'))
##        db_sess = db_session.create_session()
##        if db_sess.query(User).filter(User.email == form.email.data).first():
##            return render_template('register.html', title='Регистрация',
##                                   form=form,
##                                   message="Такой пользователь уже есть")
##        user = User(name=form.name.data, email=form.email.data)
##        user.set_password(form.password.data)
##        db_sess.add(user)
##        db_sess.commit()
##        db_sess.close()
##        return redirect(url_for('login'))
##    return render_template('register.html', title='Регистрация', form=form)
##
##
##@app.route('/register_adm', methods=['GET', 'POST'])
##def register_adm():
##    form = RegisterFormAdmin()
##    if form.validate_on_submit():
##        db_sess = db_session.create_session()
##        if db_sess.query(User).filter(User.email == form.email.data).first():
##            return render_template('register.html', title='Регистрация',
##                                   form=form,
##                                   message="Такой пользователь уже есть")
##        if form.code.data != 'ADMIN_REGISTER':
##            return render_template('register.html', title='Регистрация',
##                                   form=form,
##                                   message="Не угадал)")
##        user = User(name=form.name.data, email=form.email.data)
##        user.set_password(form.password.data)
##        db_sess.add(user)
##        db_sess.commit()
##        db_sess.close()
##        return redirect(url_for('login'))
##    return render_template('register_adm.html', title='Регистрация', form=form, message='Ну, пробуй')
##
##
##@app.route('/logout')
##@login_required
##def logout():
##    logout_user()
##    return redirect(url_for('index'))
##
##
##@app.route('/new_det', methods=['GET', 'POST'])
##@login_required
##def new_det():
##    if 'admin' in current_user.name:
##        db_sess = db_session.create_session()
##        types = get_js('types'); chars = get_js('chars')
##        N = ['type', 'name', 'price', 'descript', 'weight', 'material', 'color',
##             'manufacture', 'img', 'img_velo', 'available', 'level']
##        if request.method == 'POST':
##            if None in ([request.form.get(i) for i in N] +
##                        [request.form.get(i) for i in types[request.form.get('type')].keys()]):
##                return render_template('new_det.html', title='Создание новой детали', types=types,
##                                       chars=chars, message='Заполните все поля')
##            elif db(filt=[Detail.name], req=[request.form.get('name')]):
##                return render_template('new_det.html', title='Создание новой детали', types=types,
##                                       chars=chars, message='Деталь с таким именем уже есть в БД')
##
##            det = Detail()
##            det.type = list(types.keys()).index(request.form.get('type'))
##            det.name = request.form.get('name')
##            det.price = int(request.form.get('price'))
##            det.descript = request.form.get('descript')
##            det.weight = int(request.form.get('weight'))
##            det.material = [i for i in chars["material"].keys()].index(request.form.get('material'))
##            det.color = chars["color"].index(request.form.get('color'))
##            det.manufacture = [i for i in chars["manufacture"].keys()].index(request.form.get('manufacture'))
##            det.img = request.form.get('img')
##            det.img_velo = request.form.get('img_velo')
##            det.available = request.form.get('available')
##            det.level = [i for i in chars["level"].keys()].index(request.form.get('level'))
##            det.param = '~'.join([request.form.get(i) for i in types[request.form.get('type')].keys()])
##
##            db_sess.add(det)
##            db_sess.commit()
##            return redirect(url_for('index'))
##        return render_template('new_det.html', title='Создание новой детали', types=types, chars=chars)
##    else: return redirect(url_for('index'))
##
##
##
##@app.route('/up_det', methods=['GET', 'POST'])
##@login_required
##def up_det():
##    if 'admin' in current_user.name:
##        form = UpDetForm()
##        if form.validate_on_submit():
##            db_sess = db_session.create_session()
##            up_que = sqlal.update(Detail).where(Detail.name == form.name.data).values(form.new_par.data)
##            db_sess.execute(up_que)
##            db_sess.commit()
##            return redirect(url_for('index'))
##        else: return render_template('up_det.html', title='Изменение детали', form=form)
##    else: return redirect(url_for('index'))
##    
##
##@app.route('/del_det', methods=['GET', 'POST'])
##@login_required
##def del_det():
##    if 'admin' in current_user.name:
##        form = DelDetForm()
##        if form.validate_on_submit():
##            db_sess = db_session.create_session()
##            db_sess.query(Detail).filter(Detail.name == form.name.data).delete()
##            db_sess.commit()
##            return redirect(url_for('index'))
##        else: return render_template('del_det.html', title='Удаление детали', form=form)
##    else: return redirect(url_for('index'))
##
##@app.route('/ready_builds')
##@login_required
##def ready_builds():
##    builds, db_sess = [], db_session.create_session()
##    for build in [json.loads(str(i)) for i in db_sess.query(Build).filter(Build.user_name == current_user.name).group_by(Build.user_name)]:
##        build['details'], build['price'], build['weight'], details_id = {}, 0, 0, build['details'].split()
##        for det_id in details_id:
##            det = [json.loads(str(i)) for i in db_sess.query(Detail).filter(Detail.id == det_id).group_by(Detail.name)][0]
##            build['details'][det['type']] = det['name']
##            build['price'] += int(det['price'])
##            build['weight'] += int(det['weight'])
##        build['weight'] = f"{build['weight'] // 1000} кг, {build['weight'] % 1000} гр"
##        builds.append(build)
##    print(builds)
##    return render_template('ready_builds.html', title='Общие сборки', builds=builds)
##    
##
##
##@app.route('/your_builds', methods=['GET', 'POST'])
##@login_required
##def your_builds():
##    builds, db_sess= [], db_session.create_session()
##    if request.method == 'POST': db_sess.query(Build).filter(Build.id == request.form['id_build']).delete()
##    if 'admin' in current_user.name: que = db_sess.query(Build).group_by(Build.user_name)
##    else: que = db_sess.query(Build).filter(Build.user_name == current_user.name).group_by(Build.user_name)
##
##    for build in [json.loads(str(i)) for i in que]:
##        build['details'], details_id = [], build['details'].split()
##        for det_id in details_id:
##            det = [json.loads(str(i)) for i in db_sess.query(Detail).filter(Detail.id == det_id).group_by(Detail.name)][0]
##            build['details'][det['type']] = det['name']
##            build['price'] += int(det['price'])
##            build['weight'] += int(det['weight'])
##        build['weight'] = f"{build['weight'] // 1000} кг, {build['weight'] % 1000} гр"
##        builds.append(build)
##
##    db_sess.commit()
##    db_sess.close()
##    print(builds)
##    return render_template('your_builds.html', title='Ваши сборки')
##
##if __name__ == '__main__':
##    db_session.global_init("db/velo.db")
##    app.run(port=8080, host='127.0.0.1')
