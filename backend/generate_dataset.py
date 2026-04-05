import pandas as pd
import random
import os

# Define extensive templates
good_emails = [
    "Hi {name}, I saw your post about {topic} and loved your insights. I'm building a tool for {role}s that might help your team at {company}. Would love to chat!",
    "Dear {name}, your work at {company} in the {role} space is impressive. I'd love to share how our platform can optimize your workflow. Do you have 10 mins this week?",
    "Hello {name}, I noticed {company} is hiring for {role}s. I have a background in {topic} and would love to discuss how I can contribute. Here is my portfolio.",
    "Hi {name}, congratulations on the recent funding for {company}! I have some ideas on how to scale your {topic} strategy. Are you open to a quick call?",
    "Hey {name}, I'm a huge fan of {company}. I noticed a small bug in your {topic} page and took the liberty of fixing it. Happy to share the code!",
    "Hi {name}, I've been following {company}'s growth for a while. Your approach to {topic} is truly unique. I'd love to learn more about your needs for {role}s.",
    "Dear {name}, I read your profile and your experience with {topic} is remarkable. I think you'd be interested in how we're helping {role}s at {company} achieve better ROI.",
]

bad_emails = [
    "BUY CHEAP PILLS NOW! CLICK HERE FOR 90% DISCOUNT. LIMITED OFFER!!!",
    "URGENT: Your account has been compromised. Log in at http://scam-site.com to verify your identity immediately.",
    "Congratulations! You won $1,000,000. Send your bank details to claim your prize now.",
    "Get rich quick from home! No experience needed. Just pay a small fee of $99 to start making thousands.",
    "Make money fast! Easy work, high pay. Don't miss out on this lifetime opportunity.",
    "Need a loan? We offer low interest rates for everyone. No credit check required. Apply today!",
    "Hi, please check this out: http://link-to-virus.com. It's really cool!",
    "You have a new message! Click here to read it: http://malware.org",
    "Final notice: Pay your bill or your service will be disconnected. Pay now at http://fake-pay.com",
    "Double your money in 24 hours! Guaranteed returns on crypto. Join our Telegram group now.",
]

average_emails = [
    "Hi, I am interested in your services. Can you send me a brochure and pricing details? Thanks.",
    "Hello, we are a marketing agency looking for new clients. Are you interested in growing your business? Let us know.",
    "To whom it may concern, I am applying for the position at your company. My resume is attached. Best regards.",
    "Hello, I have a question about your product. Does it support multi-user access? Please let me know when you can.",
    "Hi team, just following up on our previous email. Have you had a chance to look at our proposal yet?",
    "Hello, I saw your website and wanted to reach out. We offer SEO services that can help you rank higher on Google.",
    "Hi, I'm {name} from {company}. We are a {role} firm specializing in {topic}. Would you like to hear more?",
    "Dear Sir/Madam, I am writing to inquire about the vacant {role} position. I have 5 years of experience in {topic}.",
]

names = ["Alice", "Bob", "Charlie", "David", "Emma", "Frank", "Grace", "Henry", "Ivy", "Jack"]
companies = ["TechCorp", "InnovaSoft", "GlobalSolutions", "FutureAI", "DataSystems", "NextGen", "SmartLogic"]
roles = ["Product Manager", "Software Engineer", "Marketing Lead", "Data Scientist", "Sales Director", "CTO", "HR Manager"]
topics = ["artificial intelligence", "customer retention", "cloud computing", "machine learning", "SEO strategy", "Big Data", "Blockchain"]

def generate():
    dataset = []

    # Generate Good Emails (Label 1) - 400 samples
    for _ in range(400):
        template = random.choice(good_emails)
        email = template.format(
            name=random.choice(names),
            company=random.choice(companies),
            role=random.choice(roles),
            topic=random.choice(topics)
        )
        dataset.append({"email": email, "label": 1})

    # Generate Bad Emails (Label 0) - 300 samples
    for _ in range(300):
        email = random.choice(bad_emails)
        dataset.append({"email": email, "label": 0})

    # Generate Average Emails - 300 samples
    for i in range(300):
        email = random.choice(average_emails)
        if "{name}" in email:
            email = email.format(
                name=random.choice(names),
                company=random.choice(companies),
                role=random.choice(roles),
                topic=random.choice(topics)
            )
        # Randomly assign label based on slight quality variations
        label = 1 if i % 3 == 0 else 0 
        dataset.append({"email": email, "label": label})

    df = pd.DataFrame(dataset)
    df.to_csv("dataset.csv", index=False)
    print(f"Generated v3.14 dataset with {len(df)} samples.")

if __name__ == "__main__":
    generate()
