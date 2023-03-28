from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE, bcrypt
from flask import flash
# from flask_app.models import shop_model
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self,data):
        self.id=data['id']
        self.user_name=data['user_name']
        self.first_name=data['first_name']
        self.last_name=data['last_name']
        self.email=data['email']
        self.password=data['password']
        self.confirm_password=data['confirm_password']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']

    @classmethod
    def create(cls,data):
        query = """
        INSERT INTO users(user.user_name, user.first_name, user.last_name, user.email, user.password, user.confirm_password)
        VALUES(%(user_name)s,%(first_name)s,%(last_name)s,%(email)s,%(password)s,%(confirm_password)s,)
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(DATABASE).query_db(query)
        print(results)
        users = []
        if results:
            for row in results:
                one_user = cls(row)
                users.append(one_user)
            return users
        return []
    
    @staticmethod
    def register_validation(data):
        is_valid= True
        if len(data['user_name'] < 2):
            flash("Username must be at least 2 characters." "register error")

        if User.get_by_user_name(data):
            flash("Username already registered", "register error")
            is_valid = False

        if len(data['first_name']) < 2:
            flash("Must be at least 2 characters.", "register error")
            is_valid = False
        
        if len(data['last_name']) < 2:
            flash("Must be at least 2 characters.", "register error")
            is_valid = False
        
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address", "register error")
            is_valid = False
        
        if User.get_by_email(data):
            flash("Email already registered", "register error")
        
        if len(data['password']) < 8:
            flash("Password too short", "register error")
            is_valid = False

        if data['password'] != data['confirm_password']:
            flash("Passwords do not match","register error")
            is_valid = False
        return is_valid
    
    @classmethod
    def get_by_email(cls, data):
        query = """
        SELECT * FROM users
        WHERE email = %(email)s
        """
        results = connectToMySQL(DATABASE).query_db(query,data)
        if results and len(results) > 0:
            found_user = cls(results[0])
            return found_user
        else:
            return False

    @classmethod
    def get_by_user_name(cls, data):
        query = """
        SELECT * FROM users
        WHERE user_name = %(user_name)s
        """
        results = connectToMySQL(DATABASE).query_db(query,data)
        if results and len(results) > 0:
            found_user_name = cls(results[0])
            return found_user_name
        else:
            return False

    @classmethod
    def login_validation(cls, data):
        found_user = cls.get_by_email(data)
        if not found_user:
            flash("Invalid Login","login error")
            return False
        else:
            hash = found_user.password
            if bcrypt.check_password_hash(hash, data['password']):
                return found_user
            else:
                flash("Invalid login","login error")
                return False
            
    @classmethod
    def get_by_id(cls,id):
        data = {
            'id':id,
        }
        query = """
        SELECT * FROM users
        WHERE id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query,data)
        if results and len(results) > 0:
            found_user = cls(results[0])
            return found_user
        else:
            return False
    
    # @classmethod
    # def get_with_items(cls, id):
    #     data = {
    #         'id':id,
    #     }
    #     query = """
    #     SELECT * FROM users
    #     JOIN items
    #     ON items.user_id = users.id
    #     WHERE users.id = %(id)s;
    #     """
    #     results = connectToMySQL(DATABASE).query_db(query,data)
    #     print(results)

    #     if not results or len(results) < 1:
    #         return cls.get_by_id(data['id'])
        
    #     user = cls(results[0])

    #     item_list = []

    #     for result in results:
    #         data = {
    #             **result,
    #             'id':result['items.id'],
    #             'created_at': result['items.created_at'],
    #             'updated_at': result['items.updated_at']
    #         }

    #         item = item_model.Item(data)
    #         item_list.append(item)
    #     user.items = item_list
    #     return user