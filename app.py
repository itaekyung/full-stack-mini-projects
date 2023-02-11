from flask import Flask, render_template, request, jsonify, redirect, url_for
from bson import ObjectId

app = Flask(__name__)

## certifi 맥OS 환경설정을 위한 패키지 설치입니다.
from pymongo import MongoClient
import certifi

ca = certifi.where()
client = MongoClient("mongodb+srv://test:sparta@cluster0.do6jypk.mongodb.net/?retryWrites=true&w=majority",
                     tlsCAFile=ca)


if __name__ == '__main__':
app.run('0.0.0.0', port=5000, debug=True)