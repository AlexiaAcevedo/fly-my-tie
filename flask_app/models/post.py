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
        self.creator = None
        self.user_ids_who_favorited = []
        self.users_who_favorited = []

    @classmethod
    def save_post(cls, data):
        query = 'INSERT INTO posts ( image_url, fly_name, pattern_type, difficulty, hook, bead, thread, fins, tail, belly, body, instructions, user_id, created_at, updated_at) VALUES ( %(image_url)s, %(fly_name)s, %(pattern_type)s, %(difficulty)s, %(hook)s, %(bead)s, %(thread)s, %(fins)s, %(tail)s, %(belly)s, %(body)s, %(instructions)s, %(user_id)s, NOW(), NOW() );'
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

    # @classmethod
    # def get_all_posts_of_one_user(cls,data):
    #     query = 'SELECT * FROM posts WHERE posts.user_id = %(id)s;'


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
    def get_all_likes(cls):
        query = '''SELECT * FROM posts
                JOIN users AS creators ON posts.user_id = creators.id
                LEFT JOIN favorites ON favorites.posts_id = posts.id
                LEFT JOIN users AS users_who_favorited ON favorites.users_id = users_who_favorited.id;'''
        results = connectToMySQL('tie_my_fly').query_db(query)
        posts = []
        for row in results:
            new_post = True
            user_who_favorited_data = {
                "id": row['users_who_favorited.id'],
                "first_name": row['users_who_favorited.first_name'],
                "last_name": row['users_who_favorited.last_name'],
                "username": row['users_who_favorited.username'],
                "email": row['users_who_favorited.email'],
                "password": row['users_who_favorited.password'],
                "profile_photo_url": row['users_who_favorited.profile_photo_url'],
                "bio": row['users_who_favorited.bio'],
                "created_at": row['users_who_favorited.created_at'],
                "updated_at": row['users_who_favorited.updated_at']
            }
            # check to see if previously processed post belongs to the same as current row
            number_of_posts = len(posts)
            # we have processed a row already
            if number_of_posts > 0:
                # check to see if the last post is the same as the current row
                last_post = posts[number_of_posts - 1]
                if last_post.id == row['id']:
                    last_post.user_ids_who_favorited.append(row['users_who_favorited.id'])
                    last_post.users_who_favorited.append(user.User(user_who_favorited_data))
                    new_post = False
            # create new post object if post has not been created and added to the list
            if new_post:

                # create a post object
                post = cls(row)
                # create a user object
                user_data = {
                    "id": row['creators.id'],
                    "first_name": row['first_name'],
                    "last_name": row['last_name'],
                    "username": row['username'],
                    "email": row['email'],
                    "password": row['password'],
                    "profile_photo_url": row['profile_photo_url'],
                    "bio": row['bio'],
                    "created_at": row['creators.created_at'],
                    "updated_at": row['creators.updated_at']
                }
                creator = user.User(user_data)
                # associate user to the user's post
                post.creator = creator
                #check to see if any user liked this post
                if row['users_who_favorited.id']:
                    post.user_ids_who_favorited.append(row['users_who_favorited.id'])
                    post.users_who_favorited.append(user.User(user_who_favorited_data))
                # add post object to list of posts
                posts.append(post)
            return posts



    @staticmethod
    def validate_post(post):
        is_valid = True
        if len(post['image_url']) < 5:
            flash('Image URL invalid', 'post')
            is_valid = False
        if len(post['fly_name']) < 3:
            flash('Fly name should be at least 3 characters long', 'post')
            is_valid = False 
        if len(post['hook']) < 3:
            flash('Hook should be at least 5 characters long', 'post')
            is_valid = False
        if len(post['bead']) < 3:
            flash('Bead should be at least 5 characters long', 'post')
            is_valid = False
        if len(post['thread']) < 3:
            flash('Thread should be at least 5 characters long', 'post')
            is_valid = False
        if len(post['fins']) < 3:
            flash('Fins should be at least 5 characters long', 'post')
            is_valid = False
        if len(post['tail']) < 3:
            flash('Tail should be at least 5 characters long', 'post')
            is_valid = False
        if len(post['belly']) < 3:
            flash('Belly should be at least 5 characters long', 'post')
            is_valid = False
        if len(post['body']) < 3:
            flash('Body should be at least 5 characters long', 'post')
            is_valid = False
        if len(post['instructions']) < 30:
            flash('Instructions should be at least 30 characters long', 'post')
            is_valid = False
        return is_valid