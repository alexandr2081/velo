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