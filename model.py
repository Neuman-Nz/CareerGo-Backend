from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.hybrid import hybrid_property
from flask_bcrypt import Bcrypt
import re


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
    jobseeker = db.relationship("Jobseeker", back_populates="user")
    employer = db.relationship("Employer", back_populates="user")

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
            raise ValueError('Phone is required')
        
        # Check phone number format using regular expression
        # phone_pattern =  r'^\+?\d{1,3}-?\d{3,}-?\d{3,}-?\d{4,}$'  # Assuming phone numbers start with 254 and are followed by 9 digits
        # if not re.match(phone_pattern, phone_number):
        #     raise ValueError('Invalid phone number format')

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
    availability = db.Column(db.String(50))
    job_category = db.Column(db.String(50))
    salary_expectation = db.Column(db.String(50))
    skills = db.Column(db.Text, nullable=False)
    qualifications = db.Column(db.Text, nullable=False)
    experience = db.Column(db.Text, nullable=False)
    github_link = db.Column(db.String(255))
    profile_verified = db.Column(db.Boolean, default=False)
    picture = db.Column(db.String)

    # Relationships
    user = db.relationship("User", back_populates="jobseeker")
    #files = db.relationship("File", back_populates="jobseeker")


    def __repr__(self):
        return f'<Jobseeker {self.job_category} >'


class Employer(db.Model, SerializerMixin):
    __tablename__ = 'employers'

    serialize_rules = ('-user.employer',)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    company_name = db.Column(db.String(100))
    profile_verified = db.Column(db.Boolean, default=False)
    picture = db.Column(db.String)

    # Relationships
    user = db.relationship("User", back_populates="employer")

    def __repr__(self):
        return f'<Employer {self.company_name}>'
    
class Admin(db.Model, SerializerMixin):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f'<Admin email: {self.email}>'
    

# class File(db.Model):
#     __tablename__ = 'files'

#     serialize_rules = ('-jobseeker.files',)

#     id = db.Column(db.Integer, primary_key=True)
#     jobseeker_id = db.Column(db.Integer, db.ForeignKey('jobseekers.id'))
#     file_path = db.Column(db.String(255))
#     file_type = db.Column(db.String(50))

#     # Relationships
#     jobseeker = db.relationship("Jobseeker", back_populates="files")

#     def __repr__(self):
#         return f'<File >'
    
# class Offer(db.Model):
#     __tablename__ = 'offers'
#     id = db.Column(db.Integer, primary_key=True)
#     employer_id = db.Column(db.Integer, db.ForeignKey('employers.id'), nullable=False)
#     job_seeker_id = db.Column(db.Integer, db.ForeignKey('jobseekers.id'), nullable=False)
#     description = db.Column(db.Text, nullable=False)
#     accepted = db.Column(db.Boolean, default=False)
    
#     employer = db.relationship('Employer', backref=db.backref('offers', lazy=True))
#     job_seeker = db.relationship('Jobseeker', backref=db.backref('offers', lazy=True))

#     def __repr__(self):
#         return f'<Offer>'


    
# class Payment(db.Model):
#     __tablename__ = 'payments'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     amount = db.Column(db.Integer, nullable=False)
#     payment_date = db.Column(db.Date, nullable=False)
#     payment_status = db.Column(db.Boolean, default=False)
#     user = db.relationship('User', backref=db.backref('payments', lazy=True))

#     def __repr__(self):
#         return f'<Payment>'
# class Testimonials(db.Model):
#     __tablename__ = 'testimonials'

#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     description = db.Column(db.Text, nullable=False)
#     rating = db.Column(db.Integer, nullable=False)
    
#     user = db.relationship('User', backref=db.backref('testimonials', lazy=True))
#     @validates('rating')
#     def validate_rating(self, key, value):
#         """Validate that the rating is an integer between 1 and 5."""
#         if not (1 <= value <= 5):
#             raise exc.InvalidRequestError(f"Invalid rating: {value}. Rating must be an integer between 1 and 5.")
#         return value
#     def __repr__(self):
#         return f'<Testimonials>'