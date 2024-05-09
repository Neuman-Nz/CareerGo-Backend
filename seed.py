from random import randint
from faker import Faker

# Local imports
from config import app  # Import Flask app 
from model import db, User, Jobseeker, Employer, File, Admin, Offer, Payment

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
                role='jobseeker' 
            )
        db.session.add(dan)
        db.session.commit()
        
        # Seed data
        for _ in range(10):
            # Create users
            user = User(
                username=fake.user_name(),
                email=fake.email(),
                password=fake.password(),
                role='jobseeker' if randint(0, 1) else 'employer'
            )
            db.session.add(user)
            db.session.commit()
            
            # Create jobseekers
            if user.role == 'jobseeker':

                jobseeker = Jobseeker(
                    user_id=user.id,
                    availability=fake.word(),
                    job_category=fake.word(),
                    salary_expectation = str(randint(20000, 100000)),
                    skills=' '.join(fake.words()),  # Convert list to string
                    qualifications=' '.join(fake.words()),  # Convert list to string
                    experience=' '.join(fake.words()),  # Convert list to string
                    github_link=fake.url(),
                    linkedin_link=fake.url(),
                    profile_verified=True if randint(0, 1) else False,
                    picture=fake.image_url()
                )
                db.session.add(jobseeker)
                db.session.commit()
                    
            # Create employers
            if user.role == 'employer':
                employer = Employer(
                    user_id=user.id,
                    company_name=fake.company(),
                    profile_verified=True if randint(0, 1) else False,
                    picture=fake.image_url()
                )
                db.session.add(employer)
                db.session.commit()

            # Create payments
            if user.role == 'employer':
                for _ in range(randint(0, 3)):
                    payment = Payment(
                    user_id=user.id,
                    amount=randint(100, 1000),
                    payment_date=fake.date_this_year(),
                    payment_status =True if randint(0, 1) else False
                    )
                    db.session.add(payment)
                    db.session.commit()
                
            
            # Create files for jobseekers
            if user.role == 'jobseeker':
                for _ in range(randint(0, 3)):
                    file = File(
                        jobseeker_id=jobseeker.id,
                        file_path=fake.file_path(),
                        file_type=fake.file_extension()
                    )
                    db.session.add(file)
                    db.session.commit()
        
        # Create offers
        for _ in range(3):
            offer = Offer(
                employer_id=(randint(1, 5)),
                job_seeker_id=(randint(1, 5)),
                description=fake.text()
            )
            db.session.add(offer)
            db.session.commit()
        
        
        
        # Create admin
        admin = Admin(email='admin@example.com')
        db.session.add(admin)
        db.session.commit()

        print("Seed complete!")