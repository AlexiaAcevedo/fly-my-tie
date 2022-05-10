from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import post
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.profile_photo_url = data['profile_photo_url']
        self.bio = data['bio']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.posts = []

    @classmethod
    def save_user_initial(cls, data):
        query = 'INSERT INTO users ( first_name, last_name, username, email, password, created_at, updated_at ) VALUES ( %(first_name)s, %(last_name)s, %(username)s, %(email)s, %(password)s, NOW(), NOW() );'
        results = connectToMySQL('tie_my_fly').query_db(query, data)
        return results

    @classmethod
    def save_user_cont(cls, data):
        #would need to incorporate user who's logged in ID or just use an update query???
        query = 'INSERT INTO users ( profile_photo_url, bio ) VALUES ( %(profile_photo_url)s, %(bio)s );'
        results = connectToMySQL('tie_my_fly').query_db(query, data)
        return results
    
    @classmethod
    def update_user(cls, data):
        query = 'UPDATE users SET profile_photo_url = %(profile_photo_url)s, first_name = %(first_name)s, last_name = %(last_name)s, bio = %(bio)s WHERE id = %(id)s;'
        results = connectToMySQL('tie_my_fly').query_db(query, data)
        return results

    @classmethod
    def delete_user(cls, data):
        query = 'DELETE FROM users WHERE id = %(id)s;'
        results = connectToMySQL('tie_my_fly').query_db(query, data)
        return results

    @classmethod
    def get_by_email(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL('tie_my_fly').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_username(cls, data):
        query = 'SELECT * FROM users WHERE username = %(username)s;'
        results = connectToMySQL('tie_my_fly').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls, data):
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        results = connectToMySQL('tie_my_fly').query_db(query, data)
        return cls(results[0])

    @staticmethod
    def validate_user(user):
        is_valid = True
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL('tie_my_fly').query_db(query, user)
        if len(results) >= 1:
            flash('Email already taken.', 'register')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid email format.', 'register')
            is_valid = False
        query = 'SELECT * FROM users WHERE username = %(username)s;'
        results = connectToMySQL('tie_my_fly').query_db(query, user)
        if len(results) >= 1:
            flash('Username already taken.', 'register')
            is_valid = False
        if not NAME_REGEX.match(user['first_name']):
            flash('Invalid first name characters.', 'register')
            is_valid = False
        if len(user['first_name']) < 2:
            flash('First name must be at least 2 characters.', 'register')
            is_valid = False
        if not NAME_REGEX.match(user['last_name']):
            flash('Invalid last name characters.', 'register')
            is_valid = False
        if len(user['last_name']) < 2:
            flash('Last name must be at least 2 characters.', 'register')
            is_valid = False
        if len(user['password']) < 8:
            flash('Password must be at least 8 characters.', 'register')
            is_valid = False
        if user['password'] != user['confirm']:
            flash('Passwords did not match.', 'register')
            is_valid = False
        return is_valid