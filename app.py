from flask import Flask, render_template, request, jsonify, redirect, url_for
from bson import ObjectId

app = Flask(__name__)

## certifi 맥OS 환경설정을 위한 패키지 설치입니다.
from pymongo import MongoClient
import certifi

ca = certifi.where()
client = MongoClient("mongodb+srv://hanghaeteam14:team14@cluster0.7iskixj.mongodb.net/?retryWrites=true&w=majority",
                     tlsCAFile=ca)


