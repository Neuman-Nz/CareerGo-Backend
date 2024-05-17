from random import randint
from faker import Faker
import random
import phonenumbers
from datetime import datetime, timedelta



# Local imports
from app import app  # Import Flask app 
from model import db, User, Jobseeker, Employer, Admin, File, Offer, Payment

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
    
    # List of picture URLs
    picture_urls = [
        "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "https://images.unsplash.com/photo-1577975882846-431adc8c2009?q=80&w=1480&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "https://images.unsplash.com/photo-1538330627166-33d1908c210d?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "https://images.unsplash.com/photo-1491233670471-398d873b5406?q=80&w=1473&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "https://images.unsplash.com/photo-1588376483402-acc965d4ac21?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "https://images.unsplash.com/photo-1500517484800-e4676bd66290?q=80&w=1469&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?q=80&w=1471&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "https://images.unsplash.com/photo-1568602471122-7832951cc4c5?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?q=80&w=1448&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "https://images.unsplash.com/photo-1523673671576-35ff54e94bae?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
    ]

    jobseeker_file_names = ["Curriculum Vitae",
                  "Resume",
                  "Personal Website",
                  "PortFolio"
    ]

    employer_file_names = ["Business License",
                  "Tax Documents",
                  "Business Proposal",
                  "Contracts"
    ]

    availabilities = [
        "Available",
        "Not Available",
        "Needs notice period"
    ]
    
    job_categories = [
        "Software Engineer",
        "Doctor",
        "Teacher",
        "Designer",
        "Manager",
        "Nurse",
        "Accountant",
        "Architect",
        "Consultant",
        "Electrician",
        "Mechanic",
        "Plumber",
        "Pharmacist",
        "Project Manager",
        "Sales Executive",
        "Marketing Specialist",
        "Business Analyst",
        "HR Manager",
        "Data Scientist",
        "Cyber Security Specialist"
    ]
    
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
                    availability=random.choice(availabilities),
                    job_category=random.choice(job_categories),
                    salary_expectation=str(randint(20000, 100000)),
                    skills=fake.text(),
                    qualifications=fake.text(),
                    experience=fake.text(),
                    github_link=fake.url(),
                    linkedin_link=fake.url(),
                    profile_verified=bool(random.getrandbits(1)),
                    picture=random.choice(picture_urls),
                    testimonial=fake.text(),
                    app_rating=randint(1, 5)
                )
                db.session.add(jobseeker)
                db.session.commit()
                # Generate fake files for jobseekers
                for _ in range(randint(1, 2)):
                    file = File(
                        jobseeker_id=jobseeker.id,
                        file_path="https://www.canva.com/design/DAF1oaO_juM/AJbTRI-L0jjnDeZYzFqmig/view?utm_content=DAF1oaO_juM&utm_campaign=designshare&utm_medium=link&utm_source=viewer",
                        file_name=random.choice(jobseeker_file_names)
                    )
                    db.session.add(file)
                db.session.commit()
                    
            # Create employers
            if user.role == 'employer':
                employer = Employer(
                    user_id=user.id,
                    company_name=fake.company(),
                    profile_verified=bool(random.getrandbits(1)),
                    picture=random.choice(picture_urls),
                    testimonial=fake.text(),
                    app_rating=randint(1, 5)
                )
                db.session.add(employer)
                db.session.commit()
                # Generate fake files for employers
                for _ in range(randint(1, 2)):
                    file = File(
                        employer_id=employer.id,
                        file_path="https://www.canva.com/design/DAF1oaO_juM/AJbTRI-L0jjnDeZYzFqmig/view?utm_content=DAF1oaO_juM&utm_campaign=designshare&utm_medium=link&utm_source=viewer",
                        file_name=random.choice(employer_file_names)
                    )
                    db.session.add(file)
                db.session.commit()

       # Seed Offer data
        for _ in range(5):
            employer = random.choice(Employer.query.all())
            jobseeker = random.choice(Jobseeker.query.all())
            offer = Offer(
                employer_id=employer.id,
                job_seeker_id=jobseeker.id,
                description=fake.text(),
                accept_status=bool(random.getrandbits(1))
            )
            db.session.add(offer)
            db.session.commit()

        # Seed Payments
        employers = Employer.query.all()  # Fetch all employers outside the loop
        for employer in employers:  # Iterate over each employer
                if employer.profile_verified:
                    payment = Payment(
                        employer_id=employer.id,
                        amount=1000,
                        payment_date=datetime.now() - timedelta(days=randint(1, 365)),
                        payment_status= True
                    )
                    db.session.add(payment)
                    db.session.commit()

        unverified_employer = Employer.query.filter_by(profile_verified=False).first()
        if unverified_employer:
                payment = Payment(
                    employer_id=unverified_employer.id,
                    amount=1000,
                    payment_date=datetime.now() - timedelta(days=randint(1, 365)),
                    payment_status= True
                )
                db.session.add(payment)
                db.session.commit()

            
        # Create admin
        admin = Admin(email='admin@gmail.com', password='@ADMIN1')
        db.session.add(admin)
        db.session.commit()

        print("Seed complete!")
