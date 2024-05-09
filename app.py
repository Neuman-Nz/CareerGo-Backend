from config import app, api
from flask import Flask, jsonify, request, make_response, session,render_template
from flask_restful import Resource
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


from model import db, User, Jobseeker, Employer, Admin
# Set secret key
app.secret_key = os.environ.get('SECRET_KEY')

# Define home route
@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CareerGo API</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f5f5f5;
            }
            .container {
                max-width: 800px;
                margin: 50px auto;
                background-color: #fff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            h1 {
                text-align: center;
            }
            p {
                margin-bottom: 15px;
            }
            ul {
                list-style-type: none;
                padding-left: 20px;
            }
            li {
                margin-bottom: 5px;
            }
            a {
                color: #007bff;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to CareerGo API</h1>
            <p>This is the API for CareerGo application.</p>
            <p>Endpoints:</p>
            <ul>
                <li><strong>/users</strong> -:GET - List of all users details</li>
                <li><strong>/users</strong> -:POST - Sign up a new user</li>
                <li><strong>/users/int:id</strong> -:GET - Get a user details</li>
                <li><strong>/users/int:id</strong> -:PATCH - Update a user details</li>
                <li><strong>/users/int:id</strong> -:DELETE - Delete a user</li>
                <li><strong>/login</strong> -:POST - User login</li>
                <li><strong>/logout</strong> -:DELETE - User logout</li>
                <li><strong>/check_session</strong>:GET - Check user session</li>
                <li><strong>/jobseekers</strong>:GET - List of all jobseekers profiles</li>
                <li><strong>/jobseekers</strong>:POST - Create a new jobseeker profile</li>
                <li><strong>/jobseekers/int:id</strong>:GET - Get a jobseeker profile</li>
                <li><strong>/jobseekers/int:id</strong>:PATCH - Update a jobseeker profile</li>
                <li><strong>/jobseekers/int:id</strong>:DELETE - Delete a jobseeker profile</li>
                <li><strong>/employers</strong>:GET - List of all employers profiles</li>
                <li><strong>/employers</strong>:POST - Create a new employer profile</li>
                <li><strong>/employers/int:id</strong>:GET - Get a employer profile</li>
                <li><strong>/employers/int:id</strong>:PATCH - Update a employer profile</li>
                <li><strong>/employers/int:id</strong>:DELETE - Delete a employer profile</li>
            </ul>
        </div>
    </body>
    </html>
    """

# Resource classes
class Login(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return {'message': 'Email and password are required'}, 400
        
        user = User.query.filter_by(email=email).first()
        
        if not user:
            return {'error': 'Email not found'}, 404
        
        if user.check_password(password):
            session['user_id'] = user.id
            return user.to_dict(), 200
        
        return {'error': 'Invalid password'}, 401

class Logout(Resource):
    def delete(self):
        if 'user_id' in session:
            session.pop('user_id')
            return '', 204
        else:
            return {'message': 'User is not logged in'}, 404

class CheckSession(Resource):
    def get(self):
        if 'user_id' in session:
            user_id = session['user_id']
            user = User.query.get(user_id)
            if user:
                return user.to_dict(), 200  
            else:
                return {'message': 'User not found'}, 404
        else:
            return {'message': 'Not logged in'}, 401  
        
class Users(Resource):
    def get(self):
        users = [user.to_dict() for user in User.query.all()]
        return make_response(jsonify(users), 200)

    def post(self):
        data = request.get_json()

        # Check if the email already exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return make_response(jsonify({'error': 'Email already exists'}), 400)

        # Create a new user
        new_user = User(
            username=data['username'],
            email=data['email'],
            password=data['password'],  # Use password property
            role=data['role']
        )

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return make_response(jsonify(new_user.to_dict()), 201)



class UserByID(Resource):
    def get(self, id):
        user = User.query.filter_by(id=id).first().to_dict()
        return make_response(jsonify(user), 200)

    def patch(self, id):
        user = User.query.filter_by(id=id).first()
        data = request.get_json()

        for key, value in data.items():
            setattr(user, key, value)

        db.session.commit()

        return make_response(jsonify(user.to_dict()), 200)

    def delete(self, id):
        user = User.query.filter_by(id=id).first()

        db.session.delete(user)
        db.session.commit()

        return '', 204
    
class Jobseekers(Resource):
    def get(self):
        jobseekers = [jobseeker.to_dict() for jobseeker in Jobseeker.query.all()]
        return make_response(jsonify(jobseekers), 200)

    def post(self):
        data = request.get_json()
        user_id = data.get('user_id')
        if not user_id:
            return {'error': 'User ID is required'}, 400

        # Check if the user exists
        user = User.query.get(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        # Create a new jobseeker
        jobseeker = Jobseeker(
            user_id=user_id,
            availability=data.get('availability'),
            job_category=data.get('job_category'),
            salary_expectation=data.get('salary_expectation'),
            skills=data.get('skills'),
            qualifications=data.get('qualifications'),
            experience=data.get('experience'),
            github_link=data.get('github_link'),
            linkedin_link=data.get('linkedin_link'),
            profile_verified=data.get('profile_verified'), #Front end to send json as false
            picture=data.get('picture')
        )

        # Add the new jobseeker to the database
        db.session.add(jobseeker)
        db.session.commit()

        return make_response(jsonify(jobseeker.to_dict()), 201)


class JobseekerByID(Resource):
    def get(self, id):
        jobseeker = Jobseeker.query.filter_by(id=id).first().to_dict()
        return make_response(jsonify(jobseeker), 200)

    def patch(self, id):
        jobseeker = Jobseeker.query.filter_by(id=id).first()
        data = request.get_json()

        for key, value in data.items():
            setattr(jobseeker, key, value)

        db.session.commit()

        return make_response(jsonify(jobseeker.to_dict()), 200)

    def delete(self, id):
        jobseeker = Jobseeker.query.filter_by(id=id).first()

        db.session.delete(jobseeker)
        db.session.commit()

        return '', 204

class Employers(Resource):
    def get(self):
        employers = [employer.to_dict() for employer in Employer.query.all()]
        return make_response(jsonify(employers), 200)

    def post(self):
        data = request.get_json()
        user_id = data.get('user_id')
        if not user_id:
            return {'error': 'User ID is required'}, 400

        # Check if the user exists
        user = User.query.get(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        # Create a new employer
        employer = Employer(
            user_id=user_id,
            company_name=data.get('company_name'),
            profile_verified=data.get('profile_verified'), #False from Frontend..
            picture=data.get('picture')
        )

        # Add the new employer to the database
        db.session.add(employer)
        db.session.commit()

        return make_response(jsonify(employer.to_dict()), 201)


class EmployerByID(Resource):
    def get(self, id):
        employer = Employer.query.filter_by(id=id).first().to_dict()
        return make_response(jsonify(employer), 200)

    def patch(self, id):
        employer = Employer.query.filter_by(id=id).first()
        data = request.get_json()

        for key, value in data.items():
            setattr(employer, key, value)

        db.session.commit()

        return make_response(jsonify(employer.to_dict()), 200)

    def delete(self, id):
        employer = Employer.query.filter_by(id=id).first()

        db.session.delete(employer)
        db.session.commit()

        return '', 204


# Add routes to the API
api.add_resource(Jobseekers, '/jobseekers')
api.add_resource(JobseekerByID, '/jobseekers/<int:id>')
api.add_resource(Employers, '/employers')
api.add_resource(EmployerByID, '/employers/<int:id>')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(CheckSession, '/check_session')
api.add_resource(Users, '/users')
api.add_resource(UserByID, '/users/<int:id>')

if __name__ == '__main__':
    with app.app_context():
        app.run(port=5050, debug=True)