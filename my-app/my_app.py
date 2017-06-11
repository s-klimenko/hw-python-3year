from flask import Flask
from flask import url_for, render_template, request
from vk import get_vk_posts
from ocr import get_text_from_image
from verbs import verbs_statistics
from collections import defaultdict

app = Flask(__name__)

@app.route('/')
@app.route('/main')
def main():
    urls = {'главная (эта страница)': url_for('main'),
            'глагольный анализ текста': url_for('verbs_analysis'),
            'анализ постов ВКонтакте': url_for('vk'),
            'распознавание текста с картинки': url_for('ocr')}
    return render_template('main.html', urls=urls)


@app.route('/verbs', methods=['get', 'post'])
  # todo добавить графики (пирог или столбики)
def verbs_analysis():
    if request.form:
        text = request.form['text']
        print(text)
        all_pos, v, ratio, lemms, tr, intr, s, ns, amb = verbs_statistics(text)
        return render_template('verbs.html', all=all_pos, v=v, ratio=ratio, tr=tr, intr=intr, s=s, ns=ns, lemms=lemms, amb=amb)
    return render_template('verbs.html')


@app.route('/vk', methods=['get', 'post'])
# todo добавить график (квадратики)
def vk():
    if request.form:
        id_vk = request.form['id']
        error_message, result = get_vk_posts(id_vk)
        if not error_message:
            lemms = result
            lemms_short = defaultdict(int, result)
            print(lemms_short)
            error_text = ''
        else:
            lemms = ''
            lemms_short = {}
            error_text = result
        return render_template('vk.html', data=lemms_short, error=error_message, lemms=lemms, error_text=error_text)
    return render_template('vk.html', data={})


@app.route('/ocr', methods=['get', 'post'])
def ocr():
    if request.form:
        link = request.form['link']
        if 'handwriting' in request.form:
            text = get_text_from_image(link, is_handwriting='true')
        else:
            text = get_text_from_image(link, is_handwriting='false')

        return render_template('ocr.html', text=text)
    return render_template('ocr.html')


if __name__ == '__main__':
    app.run(debug=True)
