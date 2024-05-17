from random import randint
from faker import Faker
import random
import phonenumbers

# Local imports
from config import app  # Import Flask app 
from model import db, User, Jobseeker, Employer, Admin, File

def generate_valid_phone_number():
    kenya_country_code = '+254'
    while True:
        national_number = ''.join([str(random.randint(0, 9)) for _ in range(9)])
        phone_number = f'{kenya_country_code}{national_number}'
        
        # Ensure that the phone number is valid
        try:
            # Parse the phone number
            parsed_number = phonenumbers.parse(phone_number, None)
            
            # Check if the parsed number is valid
            if phonenumbers.is_valid_number(parsed_number):
                return phone_number
        except phonenumbers.phonenumberutil.NumberParseException:
            pass

if __name__ == '__main__':
    fake = Faker()
    
    # Initialize Flask app context
    with app.app_context():
        print("Starting seed...")
        
        # Clear existing data (optional)
        db.drop_all()
        db.create_all()

        dan = User(
            username='dan',
            email='danspmunene@gmail.com',
            password='dan',
            phone_number='+254706318757',
            role='jobseeker' 
        )
        db.session.add(dan)
        db.session.commit()
        
        # Seed data
        for _ in range(10):
            # Create users
            phone_number = generate_valid_phone_number()
            user = User(
                username=fake.user_name(),
                email=fake.email(),
                password=fake.password(),
                phone_number=phone_number,
                role='jobseeker' if randint(0, 1) else 'employer'
            )
            db.session.add(user)
            db.session.commit()
            
            # Create jobseekers
            if user.role == 'jobseeker':
                jobseeker = Jobseeker(
                    user_id=user.id,
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    availability=fake.word(),
                    job_category=fake.word(),
                    salary_expectation=str(randint(20000, 100000)),
                    skills=' '.join(fake.words()),
                    qualifications=' '.join(fake.words()),
                    experience=' '.join(fake.words()),
                    github_link=fake.url(),
                    linkedin_link=fake.url(),
                    profile_verified=bool(random.getrandbits(1)),
                    picture=fake.image_url(),
                    testimonial=fake.text(),
                    app_rating=randint(1, 5)
                )
                db.session.add(jobseeker)
                db.session.commit()
                # Generate fake files for jobseekers
                for _ in range(randint(1, 2)):
                    file = File(
                        jobseeker_id=jobseeker.id,
                        file_path=fake.file_path(),
                        file_name=fake.file_name()
                    )
                    db.session.add(file)
                db.session.commit()
                    
            # Create employers
            if user.role == 'employer':
                employer = Employer(
                    user_id=user.id,
                    company_name=fake.company(),
                    profile_verified=bool(random.getrandbits(1)),
                    picture=fake.image_url(),
                    testimonial=fake.text(),
                    app_rating=randint(1, 5)
                )
                db.session.add(employer)
                db.session.commit()
                # Generate fake files for employers
                for _ in range(randint(1, 2)):
                    file = File(
                        employer_id=employer.id,
                        file_path=fake.file_path(),
                        file_name=fake.file_name()
                    )
                    db.session.add(file)
                db.session.commit()

        
        # Create admin
        admin = Admin(email='admin@gmail.com', password='admin1234')
        db.session.add(admin)
        db.session.commit()

        print("Seed complete!")
