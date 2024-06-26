from flask import Flask, jsonify, request, make_response, session
from flask_restful import Resource,Api
import os
from dotenv import load_dotenv
from flask_cors import CORS
from flask_migrate import Migrate
from model import db
from flask_mail import Mail
from flask_mail import Message


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'dan.careergo@gmail.com'
app.config['MAIL_PASSWORD'] = 'tjyq ofma qvhn iyzq'
app.config['MAIL_DEFAULT_SENDER'] = 'dan.careergo@gmail.com'

migrate = Migrate(app, db)
db.init_app(app)
mail = Mail(app)


api = Api(app)

CORS(app)
    

# Load environment variables from .env file
load_dotenv()


from model import db, User, Jobseeker, Employer, Admin, File, Offer, Payment
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
                <li><strong>/files</strong>:GET - List of all files</li>
                <li><strong>/files</strong>:POST - Add a jobseeker or employer file</li>
                <li><strong>/files/int:id</strong>:GET - Get a jobseeker or employer file</li>
                <li><strong>/files/int:id</strong>:PATCH - Update a jobseeker or employer file</li>
                <li><strong>/files/int:id</strong>:DELETE - Delete a jobseeker or employer file</li>
                <li><strong>/payments</strong>:GET - List of all payments</li>
                <li><strong>/payments</strong>:POST - Add a new payment</li>
                <li><strong>/payments/int:id</strong>:GET - Get a payment's details</li>
                <li><strong>/payments/int:id</strong>:PATCH - Update a payment's details</li>
                <li><strong>/payments/int:id</strong>:DELETE - Delete a payment</li>
                <li><strong>/offers</strong>:GET - List of all offers</li>
                <li><strong>/offers</strong>:POST - Add a new offer</li>
                <li><strong>/offers/employer/<int:employer_id></strong>:GET - Add a new offer</li>
                <li><strong>/offers/int:id</strong>:GET - Get an offer's details</li>
                <li><strong>/offers/int:id</strong>:PATCH - Update an offer's details</li>
                <li><strong>/offers/int:id</strong>:DELETE - Delete an offer</li>
                <li><strong>/admin_login</strong> -:POST - Admin login</li>
                <li><strong>/admin_logout</strong> -:DELETE - Admin logout</li>
            </ul>
        </div>
    </body>
    </html>
    """

# Resource classes



class AdminLogin(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return {'message': 'email and password are required'}, 400

        admin = Admin.query.filter_by(email=email).first()
        if admin and admin.check_password(password):
            session['admin_id'] = admin.id
            return admin.to_dict(), 200  # Return a dictionary directly
        return {'error': 'Unauthorized user'}, 401

class AdminLogout(Resource):
    def delete(self):
        if 'admin_id' in session:
            session.pop('admin_id')
            return '', 204

        

class Login(Resource):    
    def post(self):
        data = request.get_json()
        identifier = data.get('identifier')  # This can be username, email, or phone
        password = data.get('password')
        
        if not identifier or not password:
            return {'message': 'username/email/phone and password are required'}, 400
        
        # Check if the input is an email address
        is_email = '@' in identifier
        
        if is_email:
            user = User.query.filter_by(email=identifier).first()
        else:
            # Check if the input is a phone number
            is_phone = identifier.replace('+', '').isdigit() and len(identifier) > 9
            if is_phone:
                user = User.query.filter_by(phone_number=identifier).first()
            else:
                user = User.query.filter_by(username=identifier).first()
        
        if not user:
            return {'error': 'User not found'}, 404
        
        if user.check_password(password):
            session['user_id'] = user.id
            return user.to_dict(), 200
        
        return {'error': 'Invalid password'}, 401

class Logout(Resource):
    def delete(self):
        if 'user_id' in session:
            session.pop('user_id')
            return '', 204


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
        existing_email = User.query.filter_by(email=data['email']).first()
        if existing_email:
            return make_response(jsonify({'message': 'Email already exists'}), 400)

        # Check if the username already exists
        existing_username = User.query.filter_by(username=data['username']).first()
        if existing_username:
            return make_response(jsonify({'message': 'Username already exists'}), 400)

        # Create a new user
        new_user = User(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            phone_number=data['phone_number'],
            role=data['role']
        )

        # Add the new user to the database
        db.session.add(new_user)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

        return make_response(jsonify({'message': 'User successfully registered', 'user': new_user.to_dict()}), 201)



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

        if user.role == 'jobseeker':
            profile = Jobseeker.query.filter_by(user_id=id).first()
        elif user.role == 'employer':
            profile = Employer.query.filter_by(user_id=id).first()

        if profile:
            db.session.delete(profile)

        db.session.delete(user)
        db.session.commit()

        # Send email notification
        user_email = user.email
        subject = "Account Rejected"
        body = "Your account has been rejected by the admin."
        self.send_email(user_email, subject, body)
       
    @staticmethod
    def send_email(to, subject, body):
        msg = Message(subject, recipients=[to])
        msg.body = body
        mail.send(msg)
    
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
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            availability=data.get('availability'),
            job_category=data.get('job_category'),
            salary_expectation=data.get('salary_expectation'),
            skills=data.get('skills'),
            qualifications=data.get('qualifications'),
            experience=data.get('experience'),
            github_link=data.get('github_link'),
            linkedin_link=data.get('linkedin_link'),
            picture=data.get('picture'),
            profile_verified = False,

        )

        # Add the new jobseeker to the database
        db.session.add(jobseeker)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

        return make_response(jsonify(jobseeker.to_dict()), 201)


class JobseekerByID(Resource):
    def get(self, id):
        jobseeker = Jobseeker.query.filter_by(id=id).first().to_dict()
        return make_response(jsonify(jobseeker), 200)

    def patch(self, id):
            jobseeker = Jobseeker.query.filter_by(id=id).first()
            if not jobseeker:
                return make_response(jsonify({"error": "Jobseeker not found"}), 404)
            data = request.get_json()

            for key, value in data.items():
                setattr(jobseeker, key, value)

            db.session.commit()

            # Send email notification
            if 'profile_verified' in data:
                subject = "Profile Verification Status Changed"
                body = f"Your profile has been {'verified' if data['profile_verified'] else 'unverified'} by the admin."
                self.send_email(jobseeker.user.email, subject, body)

            return make_response(jsonify(jobseeker.to_dict()), 200)


    @staticmethod
    def send_email(to, subject, body):
        msg = Message(subject, recipients=[to])
        msg.body = body
        mail.send(msg)

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
            profile_verified=False,
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

        # Send email notification
        if 'profile_verified' in data:
            subject = "Profile Verification Status Changed"
            body = f"Your profile has been {'verified' if data['profile_verified'] else 'unverified'} by the admin."
            self.send_email(employer.user.email, subject, body)

        return make_response(jsonify(employer.to_dict()), 200)

    @staticmethod
    def send_email(to, subject, body):
        msg = Message(subject, recipients=[to])
        msg.body = body
        mail.send(msg)

    def delete(self, id):
        employer = Employer.query.filter_by(id=id).first()

        db.session.delete(employer)
        db.session.commit()

        return '', 204
    
# Add routes for the File class
class Files(Resource):
    def get(self):
        files = [file.to_dict() for file in File.query.all()]
        return make_response(jsonify(files), 200)

    def post(self):
        data = request.get_json()
        jobseeker_id = data.get('jobseeker_id')
        employer_id = data.get('employer_id')
        
        if not jobseeker_id and not employer_id:
            return {'error': 'Either jobseeker_id or employer_id is required'}, 400

        if jobseeker_id:
            user = Jobseeker.query.get(jobseeker_id)
            if not user:
                return {'error': 'Jobseeker not found'}, 404
        elif employer_id:
            user = Employer.query.get(employer_id)
            if not user:
                return {'error': 'Employer not found'}, 404

        # Create a new file
        file = File(
            jobseeker_id=jobseeker_id,
            employer_id=employer_id,
            file_path=data.get('file_path'),
            file_name=data.get('file_name')
        )

        # Add the new file to the database
        db.session.add(file)
        db.session.commit()

        return make_response(jsonify(file.to_dict()), 201)


class FileByID(Resource):
    def get(self, id):
        file = File.query.filter_by(id=id).first().to_dict()
        return make_response(jsonify(file), 200)

    def patch(self, id):
        file = File.query.filter_by(id=id).first()
        data = request.get_json()

        for key, value in data.items():
            setattr(file, key, value)

        db.session.commit()

        return make_response(jsonify(file.to_dict()), 200)

    def delete(self, id):
        file = File.query.filter_by(id=id).first()

        db.session.delete(file)
        db.session.commit()

        return '', 204
    
class Offers(Resource):
    def get(self):
        offers = [offer.to_dict() for offer in Offer.query.all()]
        return make_response(jsonify(offers), 200)

    def post(self):
        data = request.json
        employer_id = data.get('employer_id')
        job_seeker_id = data.get('job_seeker_id')
        description = data.get('description')
        
        if not employer_id or not job_seeker_id or not description:
            return {'error': 'Missing required data'}, 400

        employer = Employer.query.get(employer_id)
        job_seeker = Jobseeker.query.get(job_seeker_id)

        if not employer or not job_seeker:
            return {'error': 'Employer or Jobseeker not found'}, 404

        new_offer = Offer(
            employer_id=employer_id,
            job_seeker_id=job_seeker_id,
            description=description,
            accept_status=False  
        )

        db.session.add(new_offer)
        db.session.commit()

        # Send email notification to the job seeker
        self.send_offer_email(job_seeker)

        return {'message': 'Offer created successfully', 'offer': str(new_offer)}, 201

    @staticmethod
    def send_offer_email(job_seeker):
        msg = Message("New Job Offer", recipients=[job_seeker.user.email])
        msg.body = f"Hello {job_seeker.first_name},\n\nYou have received a new job offer. Log in to your account to view the details.\n\nRegards,\nThe CareerGo Team"
        
        try:
            mail.send(msg)
            app.logger.info(f"Email sent to {job_seeker.user.email} for new job offer")
        except Exception as e:
            app.logger.error(f"Failed to send email to {job_seeker.user.email}: {str(e)}")
    
class OfferByID(Resource):
    def get(self, id):
        offer = Offer.query.filter_by(id=id).first().to_dict()
        return make_response(jsonify(offer), 200)

    def patch(self, id):
        offer = Offer.query.filter_by(id=id).first()
        if not offer:
            return {'error': 'Offer not found'}, 404
        
        data = request.get_json()

        for key, value in data.items():
            setattr(offer, key, value)

        # Store the original accept_status before updating
        original_status = offer.accept_status

        db.session.commit()

        # If the accept_status has changed to accepted, send an email to the employer
        if offer.accept_status and not original_status:
            employer_id = offer.employer_id
            employer_email = Employer.query.filter_by(id=employer_id).value('email')
            if employer_email:
                subject = "Job Offer Accepted"
                body = f"Congratulations! Your job offer has been accepted by the job seeker."
                self.send_email(employer_email, subject, body)

        return make_response(jsonify(offer.to_dict()), 200)

    @staticmethod
    def send_email(to, subject, body):
        msg = Message(subject, recipients=[to])
        msg.body = body
        mail.send(msg)

    def delete(self, id):
        offer = Offer.query.filter_by(id=id).first()

        db.session.delete(offer)
        db.session.commit()

        return '', 204
    
class Payments(Resource):
    def get(self):
        payments = [payment.to_dict() for payment in Payment.query.all()]
        return make_response(jsonify(payments), 200)

    def post(self):
        data = request.get_json()

        # Create a new payment
        payment = Payment(
            employer_id=data.get('employer_id'),
            amount=data.get('amount'),
            payment_date=data.get('payment_date'),
            payment_status=data.get('payment_status')
        )

        # Add the new payment to the database
        db.session.add(payment)
        db.session.commit()

        return make_response(jsonify(payment.to_dict()), 201)
    
class PaymentByID(Resource):
    def get(self, id):
        payment = Payment.query.filter_by(id=id).first().to_dict()
        return make_response(jsonify(payment), 200)

    def patch(self, id):
        payment = Payment.query.filter_by(id=id).first()
        data = request.get_json()

        for key, value in data.items():
            setattr(payment, key, value)

        db.session.commit()

        return make_response(jsonify(payment.to_dict()), 200)

    def delete(self, id):
        payment = Payment.query.filter_by(id=id).first()

        db.session.delete(payment)
        db.session.commit()

        return '', 204

class OfferByEmployerResource(Resource):
    def get(self, employer_id):
        try:
            # Query the database for offers with the given employer_id
            offers = Offer.query.filter_by(employer_id=employer_id).all()
            if not offers:
                return {'message': 'No offers found for this employer'}, 404
            
            # Serialize the offers to a list of dictionaries
            offers_serialized = [offer.to_dict() for offer in offers]
            return jsonify(offers_serialized)
        
        except NoResultFound:
            return {'message': 'No offers found for this employer'}, 404
        except Exception as e:
            return {'message': str(e)}, 500

# Add routes to the API
api.add_resource(AdminLogin, '/admin_login')
api.add_resource(AdminLogout, '/admin_logout')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(CheckSession, '/check_session')
api.add_resource(Users, '/users')
api.add_resource(UserByID, '/users/<int:id>')
api.add_resource(Jobseekers, '/jobseekers')
api.add_resource(JobseekerByID, '/jobseekers/<int:id>')
api.add_resource(Employers, '/employers')
api.add_resource(EmployerByID, '/employers/<int:id>')
api.add_resource(Files, '/files')
api.add_resource(FileByID, '/files/<int:id>')
api.add_resource(Offers, '/offers')
api.add_resource(OfferByID, '/offers/<int:id>')
api.add_resource(OfferByEmployerResource, '/offers/employer/<int:employer_id>')
api.add_resource(Payments, '/payments')
api.add_resource(PaymentByID, '/payments/<int:id>')

if __name__ == '__main__':
    with app.app_context():
        app.run(port=5050, debug=True)
