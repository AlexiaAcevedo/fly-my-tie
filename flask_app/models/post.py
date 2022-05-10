from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Post:
    def __init__(self, data):
        self.id = data['id']
        self.image_url = data['image_url']
        self.fly_name = data['fly_name']
        self.pattern_type = data['pattern_type']
        self.difficulty = data['difficulty']
        self.hook = data['hook']
        self.bead = data['bead']
        self.thread = data['thread']
        self.fins = data['fins']
        self.tail = data['tail']
        self.belly = data['belly']
        self.body = data['body']
        self.instructions = data['instructions']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None

    @classmethod
    def save_post(cls, data):
        query = 'INSERT INTO posts ( image_url, fly_name, pattern_type, difficulty, hook, bead, thread, fins, tail, belly, body, instructions, user_id, created_at, updated at) VALUES ( %(image_url)s, %(fly_name)s, %(pattern_type)s, %(difficulty)s, %(hook)s, %(bead)s, %(thread)s, %(fins)s, %(tail)s, %(belly)s, %(body)s, %(instructions)s, %(user_id)s, NOW(), NOW() );'
        results = connectToMySQL('tie_my_fly').query_db(query, data)
        return results

    @classmethod
    def update_post(cls, data):
        query = 'UPDATE posts SET image_url = %(image_url)s, fly_name = %(fly_name)s, pattern_type = %(pattern_type)s, difficulty = %(difficulty)s, hook = %(hook)s, bead = %(bead)s, thread = %(thread)s, fins = %(fins)s, tail = %(tail)s, belly = %(belly)s, body = %(body)s, instructions = %(instructions)s, user_id = %(user_id)s, updated_at = NOW() WHERE id = %(id)s;'
        results = connectToMySQL('tie_my_fly').query_db(query, data)
        return results
    
    @classmethod
    def delete_post(cls, data):
        query = 'DELETE FROM posts WHERE id = %(id)s;'
        results = connectToMySQL('tie_my_fly').query_db(query, data)
        return results

    @classmethod
    def get_all_posts_with_users(cls):
        query = 'SELECT * FROM posts JOIN users ON users.id = posts.user_id;'
        results = connectToMySQL('tie_my_fly').query_db(query)
        if len(results) < 1:
            return None
        else:
            all_posts = []
            for each_post in results:
                this_post_instance = cls(each_post)
                this_user_dictionary = {
                    "id": each_post['users.id'],
                    "first_name": each_post['first_name'],
                    "last_name": each_post['last_name'],
                    "username": each_post['username'],
                    "email": each_post['email'],
                    "password": each_post['password'],
                    "profile_photo_url": each_post['profile_photo_url'],
                    "bio": each_post['bio'],
                    "created_at": each_post['users.created_at'],
                    "updated_at": each_post['users.updated_at']
                }
                post_creator = user.User(this_user_dictionary)
                this_post_instance.user = post_creator
                all_posts.append(this_post_instance)
            return all_posts

    @classmethod
    def get_one_post_with_user(cls, data):
        query = 'SELECT * FROM posts JOIN users ON users.id = posts.user_id WHERE posts.id = %(id)s;'
        results = connectToMySQL('tie_my_fly').query_db(query, data) 
        if len(results) < 1:
            return None
        else:
            one_post = cls(results[0])
            this_user_dictionary = {
                "id": results[0]['users.id'],
                "first_name": results[0]['first_name'],
                "last_name": results[0]['last_name'],
                "username": results[0]['username'],
                "email": results[0]['email'],
                "password": results[0]['password'],
                "profile_photo_url": results[0]['profile_photo_url'],
                "bio": results[0]['bio'],
                "created_at": results[0]['users.created_at'],
                "updated_at": results[0]['users.updated_at']
            }
            post_creator = user.User(this_user_dictionary)
            one_post.user = post_creator
            return one_post


    @classmethod
    def get_user_posts(cls, data):
        query = "SELECT * FROM users LEFT JOIN posts ON users.id = posts.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL('tie_my_fly').query_db(query,data)
        posts = []
        for post in results:
            posts.append( cls(post) )
        return posts
    
