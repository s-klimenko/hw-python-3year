
from flask import Flask
from flask import render_template, request
from collections import Counter

app = Flask(__name__)

@app.route('/')
def poll():
    return render_template('poll.html')

@app.route('/result')
def result():
    if request.args:
        name = request.args['name']
        animal = request.args['animal']
        with open('info.csv', 'a') as f:
            info = [name, ',', animal, '\r']
            f.writelines(info)
        with open('info.csv', 'r') as g:
            info = g.readlines()
            people = [i.strip().split(',')[0] for i in info]
            animals = [i.strip().split(',')[1] for i in info]
            cnt_p = Counter()
            for word in people:
                cnt_p[word] += 1
            cnt_a = Counter()
            for word in animals:
                cnt_a[word] += 1
        return render_template('result.html', name=name, animal=animal, dogs=cnt_a['dog'], cats=cnt_a['cat'], persons = cnt_p)
    with open('info.csv', 'r') as g:
        info = g.readlines()
        people = [i.strip().split(',')[0] for i in info]
        animals = [i.strip().split(',')[1] for i in info]
        cnt_p = Counter()
        for word in people:
            cnt_p[word] += 1
        cnt_a = Counter()
        for word in animals:
            cnt_a[word] += 1
    return render_template('result.html', name='Анон', animal='никого', dogs=cnt_a['dog'], cats=cnt_a['cat'], persons = cnt_p)

if __name__ == '__main__':
    app.run(debug=True)