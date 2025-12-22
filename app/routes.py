from app import app
from flask import Flask, jsonify, request



from app import app, db
from flask import jsonify, request
from .models.client import Client
from .models.pet import Pet
from .models.account import Account
from .models.diagnosis import Diagnosis
from .models.diagnosis_class import Diagnosis_class
from .models.diagnosis_pet import Diagnosis_pet
from .models.employee import Employee
from .models.med_card import Med_card
from .models.post import Post
from .models.record_service import Record_service
from .models.role import Role
from .models.service import Service
from .models.vet import Vet

#from flask_cors import CORS
from werkzeug.security import check_password_hash






