from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
from flask import Flask, render_template, jsonify, request
app = Flask(__name__)


client = MongoClient('localhost', 27017)
db = client.dbsparta


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/memo', methods=['GET'])
def listing():
    # DB에서 여러 개 꺼내기
    articles = list(db.articles.find({}, {'_id': False}))
    return jsonify({'all_articles': articles})


@app.route('/memo', methods=['POST'])
def saving():
    # 받아오는 부분
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']

    # 크롤링 작업
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    title = soup.select_one('meta[property="og:title"]')['content']
    image = soup.select_one('meta[property="og:image"]')['content']
    desc = soup.select_one('meta[property="og:description"]')['content']
    # // 크롤링 작업

    # DB에 가져온 정보 넣기
    doc = {
        'title': title,
        'image': image,
        'desc': desc,
        'url': url_receive,
        'comment': comment_receive
    }

    db.articles.insert_one(doc)

    # 응답 메세지
    # 이거 맨 끝에 써야 함
    return jsonify({'msg': 'POST 연결되었습니다!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
