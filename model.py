from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.hybrid import hybrid_property
from flask_bcrypt import Bcrypt
import re
import phonenumbers


# Define metadata, instantiate db
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)
bcrypt = Bcrypt()


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ('-jobseeker.user', '-employer.user',)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone_number = db.Column(db.String(100), nullable=True)
    _password_hash = db.Column(db.String, nullable=False)
    role = db.Column(db.String(20), nullable=False)

    # Define relationship
    jobseeker = db.relationship("Jobseeker", back_populates="user", cascade="all, delete")
    employer = db.relationship("Employer", back_populates="user", cascade="all, delete")

    def __repr__(self):
        return f'<User {self.username} | Email: {self.email}>'
    
    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise ValueError('Username is required')
        if len(username) > 50:
            raise ValueError('Username must be less than 50 characters')
        return username
    
    @validates('email')
    def validate_email(self, key, email):
        if not email:
            raise ValueError('Email is required')
        
        # Check email format using regular expression
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, email):
            raise ValueError('Invalid email format')

        return email
    

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if not phone_number:
            raise ValueError('Phone number is required')

        try:
            # Parse the phone number
            parsed_number = phonenumbers.parse(phone_number, None)

            # Get the country code from the parsed number
            country_code = phonenumbers.region_code_for_country_code(parsed_number.country_code)
            
            # Re-parse the phone number with the detected country code
            parsed_number = phonenumbers.parse(phone_number, country_code)

            if not phonenumbers.is_valid_number(parsed_number):
                raise ValueError('Invalid phone number')
        except phonenumbers.phonenumberutil.NumberParseException:
            raise ValueError('Invalid phone number format. Should be:"+254123456789"')

        return phone_number
    
    @hybrid_property
    def password(self):
        return self._password_hash

    @password.setter
    def password(self, plaintext_password):
        self._password_hash = bcrypt.generate_password_hash(plaintext_password).decode('utf-8')

    def check_password(self, plaintext_password):
        return bcrypt.check_password_hash(self._password_hash, plaintext_password)


class Jobseeker(db.Model, SerializerMixin):
    __tablename__ = 'jobseekers'

    serialize_rules = ('-user.jobseeker',)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    availability = db.Column(db.String(50))
    job_category = db.Column(db.String(50))
    salary_expectation = db.Column(db.String(50))
    skills = db.Column(db.Text)
    qualifications = db.Column(db.Text)
    experience = db.Column(db.Text)
    github_link = db.Column(db.String(255))
    linkedin_link = db.Column(db.String(255))
    profile_verified = db.Column(db.Boolean, default=False)
    picture = db.Column(db.String)
    testimonial = db.Column(db.Text)
    app_rating = db.Column(db.Integer)

    # Relationships
    user = db.relationship("User", back_populates="jobseeker", cascade="all, delete")
    files = db.relationship("File", back_populates="jobseeker", cascade="all, delete")
    payments = db.relationship("Payment", back_populates="jobseeker", cascade="all, delete")
    offers = db.relationship("Offer", back_populates="jobseeker", cascade="all, delete")





    def __repr__(self):
        return f'<Jobseeker {self.first_name} >'
    
    @validates('app_rating')
    def validate_app_rating(self, key, app_rating):
        if app_rating is not None and (app_rating < 1 or app_rating > 5):
            raise ValueError('App rating must be between 1 and 5')
        return app_rating


class Employer(db.Model, SerializerMixin):
    __tablename__ = 'employers'

    serialize_rules = ('-user.employer',)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    company_name = db.Column(db.String(100))
    profile_verified = db.Column(db.Boolean, default=False)
    picture = db.Column(db.String)
    testimonial = db.Column(db.Text)
    app_rating = db.Column(db.Integer)

    # Relationships
    user = db.relationship("User", back_populates="employer", cascade="all, delete")
    files = db.relationship("File", back_populates="employer", cascade="all, delete")
    payments = db.relationship("Payment", back_populates="employer", cascade="all, delete")
    offers = db.relationship("Offer", back_populates="employer", cascade="all, delete")

    def __repr__(self):
        return f'<Employer {self.company_name}>'
    
    @validates('app_rating')
    def validate_app_rating(self, key, app_rating):
        if app_rating is not None and (app_rating < 1 or app_rating > 5):
            raise ValueError('App rating must be between 1 and 5')
        return app_rating
    
class Admin(db.Model, SerializerMixin):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    _password_hash = db.Column(db.String, nullable=False)


    @hybrid_property
    def password(self):
        return self._password_hash

    @password.setter
    def password(self, plaintext_password):
        self._password_hash = bcrypt.generate_password_hash(plaintext_password).decode('utf-8')

    def check_password(self, plaintext_password):
        return bcrypt.check_password_hash(self._password_hash, plaintext_password)


    def __repr__(self):
        return f'<Admin email: {self.email}>'
    

class File(db.Model, SerializerMixin):
    __tablename__ = 'files'

    serialize_rules = ('-jobseeker', '-employer',)

    id = db.Column(db.Integer, primary_key=True)
    jobseeker_id = db.Column(db.Integer, db.ForeignKey('jobseekers.id'))
    employer_id = db.Column(db.Integer, db.ForeignKey('employers.id'))
    file_path = db.Column(db.String(255))
    file_name = db.Column(db.String(50))

    jobseeker = db.relationship("Jobseeker", back_populates="files")
    employer = db.relationship("Employer", back_populates="files")

    def __repr__(self):
        return f'<File name: {self.file_name}>'
    

class Payment(db.Model, SerializerMixin):
    __tablename__ = 'payments'

    serialize_rules = ('-jobseeker', '-employer',)

    id = db.Column(db.Integer, primary_key=True)
    jobseeker_id = db.Column(db.Integer, db.ForeignKey('jobseekers.id'))
    employer_id = db.Column(db.Integer, db.ForeignKey('employers.id'))
    amount = db.Column(db.Integer, nullable=False)
    payment_date = db.Column(db.Date, nullable=False)
    payment_status = db.Column(db.Boolean, default=False)
    
    jobseeker = db.relationship("Jobseeker", back_populates="payments")
    employer = db.relationship("Employer", back_populates="payments")

    def __repr__(self):
        return f'<Payment status: {self.payment_status}>'
    
class Offer(db.Model, SerializerMixin): 
    __tablename__ = 'offers'

    serialize_rules = ('-jobseeker', '-employer',)

    id = db.Column(db.Integer, primary_key=True)
    employer_id = db.Column(db.Integer, db.ForeignKey('employers.id'), nullable=False)
    job_seeker_id = db.Column(db.Integer, db.ForeignKey('jobseekers.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    accept_status = db.Column(db.Boolean, default=False)

    jobseeker = db.relationship("Jobseeker", back_populates="offers")
    employer = db.relationship("Employer", back_populates="offers")

    def __repr__(self):
        return f'<Offer status: {self.accept_status}>'


    

