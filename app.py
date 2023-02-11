from flask import Flask, render_template, request, jsonify, redirect, url_for
app = Flask(__name__)
import hashlib
import datetime
# 설치
import jwt

from bson import ObjectId

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

@app.route('/info')
def info():
    return render_template('addImage.html')

# 상세 페이지 기본
# @app.route('/detail')
# def detail_page():
#     return render_template('detail_page.html')
# 메인 카드 데이터 불러오기
@app.route("/pet", methods=["GET"])
def pet_get():
    pet_list = list(db.pet.find({},{'_id':False}))
    return jsonify({'pet':pet_list})

SECRET_KEY = 'SPARTA'
@app.route('/login', methods=["POST"])
def login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    if id_receive == "":
        return jsonify({'result': 'fail', 'msg': '아이디를 입력해주세요.', 'cur':'id'})
    elif pw_receive == "":
        return jsonify({'result': 'fail', 'msg': '비밀번호를 입력해주세요.', 'cur':'pw'})

    user_name = db.users.find_one({"user_id": id_receive})['user_name']

    #pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    pw_hash = pw_receive
    result = db.users.find_one({'user_id': id_receive, 'user_pw': pw_hash})
    print(result)

    if result is not None:
        payload = {
            'user_id': id_receive,
            'user_name': user_name,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=500)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})
    

@app.route('/main')
def go_main():
    token_receive = request.cookies.get('mytoken')
    if token_receive is None:
        return render_template('test.html')
    else:
        try:
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
            print(payload)
            return render_template('test.html', user_name=payload["user_name"], user_id=payload['user_id'])
        except jwt.ExpiredSignatureError:
            return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
        except jwt.exceptions.DecodeError:
            return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))
@app.route('/userfind')
def go_userfind():
    return render_template('userfind.html')

@app.route('/userfind/find', methods=["POST"])
def userfind():
    name_receive = request.form['name_give']
    email_receive = request.form['email_give']

    if name_receive == "":
        return jsonify({'result': 'fail', 'msg': '아이디를 입력해주세요.', 'cur': 'name'})
    elif email_receive == "":
        return jsonify({'result': 'fail', 'msg': '비밀번호를 입력해주세요.', 'cur': 'email'})

    result = db.users.find_one({'user_name': name_receive, 'user_email': email_receive})

    if result is not None:
        return jsonify({'result': 'success', 'user_id': result['user_id']})
    else:
        return jsonify({'result': 'fail', 'msg': '일치하는 아이디가 없습니다.'})

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

#이미지 추가 버튼
@app.route("/info", methods=["POST"])
def info_add():
    imgdata = request.form['imgdata']
    name = request.form['name']
    breed = request.form['breed']
    age = request.form['age']
    gender = request.form['gender']
    comment = request.form['comment']
    count = list(db.pet.find({},{'_id':False}))
    # num = len(count) + 1
    if count == []:
        num = 1
        doc = {
            'num':num,
            'name': name,
            'breed': breed,
            'age': age,
            'gender': gender,
            'comment': comment,
            'imgdata' : imgdata
        }
        db.pet.insert_one(doc)
        return jsonify({'msg': '작성완료'})
    elif name == '' or comment == '' or breed == '' or age =='' or gender=='':
        return jsonify({'msgnot': '내용을 입력해주세요'})
    else:
        ddd = count[len(count) - 1]
        num = ddd['num']
        num = num + 1
        doc = {
            'num':num,
            'name': name,
            'breed': breed,
            'age': age,
            'gender': gender,
            'comment': comment,
            'imgdata' : imgdata
        }
        db.pet.insert_one(doc)
        return jsonify({'msg': '작성완료'})

# 상세페이지 구현
@app.route('/detail/<int:num>')
def detail(num):
    name = db.pet.find_one({'num':num})['name']
    breed = db.pet.find_one({'num':num})['breed']
    age = db.pet.find_one({'num':num})['age']
    gender = db.pet.find_one({'num':num})['gender']
    comment = db.pet.find_one({'num':num})['comment']
    num = db.pet.find_one({'num':num})['num']
    imgdata = db.pet.find_one({'num':num})['imgdata']
    return render_template('detail_page.html',num=num, name=name, breed=breed, age=age, gender=gender, comment=comment, imgdata=imgdata)

@app.route('/update')
def update_page():
    return render_template('update.html')

# 업데이트 페이지 구현
@app.route('/update/<int:num>')
def update(num):
    name = db.pet.find_one({'num':num})['name']
    breed = db.pet.find_one({'num':num})['breed']
    age = db.pet.find_one({'num':num})['age']
    gender = db.pet.find_one({'num':num})['gender']
    comment = db.pet.find_one({'num':num})['comment']
    num = db.pet.find_one({'num':num})['num']
    imgdata = db.pet.find_one({'num':num})['imgdata']


    return render_template('update.html',num=num, name=name, breed=breed, age=age, gender=gender, comment=comment, imgdata=imgdata)

#  수정 기능
@app.route("/update", methods=["PUT"])
def detail_edit():
    num = request.form['num']
    name = request.form['name']
    breed = request.form['breed']
    age = request.form['age']
    gender = request.form['gender']
    comment = request.form['comment']

    db.pet.update_one({'num': int(num)}, {'$set': {'name': name}})
    db.pet.update_one({'num': int(num)}, {'$set': {'breed': breed}})
    db.pet.update_one({'num': int(num)}, {'$set': {'age': age}})
    db.pet.update_one({'num': int(num)}, {'$set': {'gender': gender}})
    db.pet.update_one({'num': int(num)}, {'$set': {'comment': comment}})

    return jsonify({'msg': '수정 완료!'})

#삭제 기능
@app.route("/detail", methods=["DELETE"])
def detail_delete():
    num = request.form['num']
    db.pet.delete_one({'num': int(num)})
    return jsonify({'msg': '삭제 완료!'})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5002, debug=True)
