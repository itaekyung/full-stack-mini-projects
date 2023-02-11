from pymongo import MongoClient
import certifi

from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)

ca = certifi.where()

client = MongoClient('mongodb+srv://test:sparta@cluster0.exrmfp9.mongodb.net/?retryWrites=true&w=majority',tlsCAFile=ca)