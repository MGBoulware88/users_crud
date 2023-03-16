# import the function to create a db instance
from mysqlconnection import connectToMySQL
# import datetime to convert our datetime to Month Day, Year format
from datetime import datetime

class User:
    DB = "user" #alias the db for convenience
    def __init__(self, data):
        #add atts from the db table representing this class
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all_users(cls):
        # I want all rows from users table and probably all the cols of each row
        query = "SELECT * FROM users;"
        # pass the query into the function we are importing from the mysqlconnection and save that to results
        results = connectToMySQL(cls.DB).query_db(query)
        # create an empty list to put each user into
        users = []

        for user in results:
            # use strptime method to change our date to display as Month Day, Year
            created_date = datetime.strptime(str(user["created_at"]), "%Y-%m-%d %H:%M:%S")
            user["created_at"] = created_date.strftime("%B %d, %Y")
            # print("joined on:", user["created_at"])
            users.append(cls(user))
        return users
    
    @classmethod
    def get_one_user(cls,id):
        query = "SELECT * FROM users WHERE id=%(id)s"
        data = {'id' : id}
        return connectToMySQL(cls.DB).query_db(query, data)

    
    @classmethod
    def create(cls, data):
        # fname, lname, email will come from form inputs
        query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES(%(fname)s , %(lname)s , %(email)s , NOW() , NOW())"
        # just commit that to the db
        new_user = connectToMySQL(cls.DB).query_db(query, data)
        print(new_user)
        return new_user
    
    @classmethod
    def update_user(cls, data):
        # fname, lname, email will come from form inputs
        query = "UPDATE users SET first_name=%(fname)s, last_name=%(lname)s, email=%(email)s, updated_at=NOW() WHERE id=%(id)s;"
        # just commit that to the db
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def delete_user(cls,data):
        query = "DELETE FROM users WHERE id=%(id)s;"
        return connectToMySQL(cls.DB).query_db(query, data)
