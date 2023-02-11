from flask import Flask, render_template, request, jsonify, redirect, url_for
app = Flask(__name__)

## certifi 맥OS 환경설정을 위한 패키지 설치입니다.
from pymongo import MongoClient
import certifi

ca = certifi.where()
client = MongoClient("mongodb+srv://test:sparta@cluster0.exrmfp9.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)
db = client.team6

@app.route('/')
def home():
    return render_template('index.html')

# 메인 카드 데이터 불러오기
@app.route("/pet", methods=["GET"])
def pet_get():
    pet_list = list(db.pet.find({},{'_id':False}))
    return jsonify({'pet':pet_list})

# 회원가입 페이지 이동
@app.route('/signup')
def signup_page():
    return render_template('signup.html')


# 회원가입 POST
@app.route("/users", methods=["POST"])
def user_post():
    user_receive = request.form['user_give']
    
    user_list = list(db.users.find({},{'_id':False}))
    count = len(user_list)+1
    
    doc = {
        'num':count,
        'bucket':bucket_receive,
        'done':0
    }

    db.bucket.insert_one(doc)
    return jsonify({'msg': '등록 완료!'})

@app.route('/detail')
def detail_page():
    return render_template('detail_page.html')

# 상세페이지 구현
# @app.route('/detail/<int:num>')
# def detail(num):
#     name = db.dog.find_one({'num':num})['name']
#     breed = db.dog.find_one({'num':num})['breed']
#     age = db.dog.find_one({'num':num})['age']
#     gender = db.dog.find_one({'num':num})['gender']
#     comment = db.dog.find_one({'num':num})['comment']
#     num = db.dog.find_one({'num':num})['num']
#     return render_template('detail.html',num=num, name=name, breed=breed, age=age, gender=gender, comment=comment)

@app.route('/update')
def update_page():
    return render_template('update.html')

# 업데이트 페이지 구현
@app.route('/update/<int:num>')
def detail(num):
    name = db.dog.find_one({'num':num})['name']
    breed = db.dog.find_one({'num':num})['breed']
    age = db.dog.find_one({'num':num})['age']
    gender = db.dog.find_one({'num':num})['gender']
    comment = db.dog.find_one({'num':num})['comment']
    num = db.dog.find_one({'num':num})['num']
    return render_template('detail.html',num=num, name=name, breed=breed, age=age, gender=gender, comment=comment)

@app.route("/update", methods=["PUT"])
def detail_edit():
    num = request.form['num']
    name = request.form['name']
    breed = request.form['breed']
    age = request.form['age']
    gender = request.form['gender']
    comment = request.form['comment']

    db.dog.update_one({'num': int(num)}, {'$set': {'name': name}})
    db.dog.update_one({'num': int(num)}, {'$set': {'breed': breed}})
    db.dog.update_one({'num': int(num)}, {'$set': {'age': age}})
    db.dog.update_one({'num': int(num)}, {'$set': {'gender': gender}})
    db.dog.update_one({'num': int(num)}, {'$set': {'comment': comment}})

    return jsonify({'msg': '수정 완료!'})

@app.route("/detail", methods=["DELETE"])
def detail_delete():
    num = request.form['num']
    db.dog.delete_one({'num': int(num)})
    return jsonify({'msg': '삭제 완료!'})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5002, debug=True)