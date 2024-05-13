from random import randint
from faker import Faker

# Local imports
from config import app  # Import Flask app 
from model import db, User, Jobseeker, Employer, Admin

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
                phone_number='+123-456-7890',
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
                phone_number=fake.phone_number(),
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

        
        # Create admin
        admin = Admin(email='admin@example.com')
        db.session.add(admin)
        db.session.commit()

        print("Seed complete!")