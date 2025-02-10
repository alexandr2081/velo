from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'custom_bike'

@app.route('/')
def index():
    for i in [1]:
        details = [{'name': 'Stern energy 1.0', 'des': 'Рама велосипеда Stern energy 1.0', 'img': 'https://n-72.ru/upload/iblock/71f/56906a5cx8771tiaqvg7vjvaf3xxp9wc.png'},
                   {'name': 'Вилка', 'des': 'Вилка велосипеда Stern energy 1.0', 'img': 'https://n-72.ru/upload/iblock/71f/56906a5cx8771tiaqvg7vjvaf3xxp9wc.png'},
                   {'name': 'Вилка', 'des': 'Вилка велосипеда Stern energy 1.0', 'img': 'https://n-72.ru/upload/iblock/71f/56906a5cx8771tiaqvg7vjvaf3xxp9wc.png'},
                   {'name': 'Вилка', 'des': 'Вилка велосипеда Stern energy 1.0', 'img': 'https://n-72.ru/upload/iblock/71f/56906a5cx8771tiaqvg7vjvaf3xxp9wc.png'},
                   {'name': 'Вилка', 'des': 'Вилка велосипеда Stern energy 1.0', 'img': 'https://n-72.ru/upload/iblock/71f/56906a5cx8771tiaqvg7vjvaf3xxp9wc.png'},
                   {'name': 'Вилка', 'des': 'Вилка велосипеда Stern energy 1.0', 'img': 'https://n-72.ru/upload/iblock/71f/56906a5cx8771tiaqvg7vjvaf3xxp9wc.png'},
                   {'name': 'Вилка', 'des': 'Вилка велосипеда Stern energy 1.0', 'img': 'https://n-72.ru/upload/iblock/71f/56906a5cx8771tiaqvg7vjvaf3xxp9wc.png'}]
    filter = [{'name': 'Stern energy 1.0', 'des': 'Рама велосипеда Stern energy 1.0'}]
    return render_template('velo_index.html', details=details, filter=filter)

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
