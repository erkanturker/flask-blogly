from models import User,Post,db,connect_db 
from app import create_app

app = create_app("blogly_db", testing=True)
    
    # Establish app context
app_context = app.app_context()
app_context.push()

# Connect to the database
connect_db(app)

# Drop all tables (if any)
db.drop_all()

# Create all tables
db.create_all()


u1 = User(first_name='Josh', last_name='Allen',image_url='https://randomuser.me/api/portraits/men/51.jpg')
u2 = User(first_name='Christy', last_name='Sutton',image_url='https://randomuser.me/api/portraits/women/25.jpg')


db.session.add_all([u1,u2])
db.session.commit()

# Manually generate titles and content for posts
title1 = "Introduction to Machine Learning"
content1 = """
Machine learning (ML) is the scientific study of algorithms and statistical models that computer systems use to perform a specific task without using explicit instructions, relying on patterns and inference instead. 
It is seen as a subset of artificial intelligence. Machine learning algorithms build a mathematical model based on sample data, known as "training data", in order to make predictions or decisions without being explicitly programmed to perform the task.
"""

title2 = "The Importance of Data Visualization"
content2 = """
Data visualization is the graphical representation of information and data. By using visual elements like charts, graphs, and maps, data visualization tools provide an accessible way to see and understand trends, outliers, and patterns in data.
Effective data visualization is important because it helps users analyze and interpret complex data more easily, enabling them to make better-informed decisions.
"""

title3 = "Exploring Natural Language Processing"
content3 = """
Natural language processing (NLP) is a subfield of linguistics, computer science, and artificial intelligence concerned with the interactions between computers and human language, in particular how to program computers to process and analyze large amounts of natural language data.
NLP is used to apply algorithms to identify and extract information from text and speech data, enabling computers to understand, interpret, and generate human language in a meaningful way.
"""

title4 = "Deep Dive into Neural Networks"
content4 = """
A neural network is a series of algorithms that endeavors to recognize underlying relationships in a set of data through a process that mimics the way the human brain operates. 
In artificial intelligence (AI), a neural network is a system of hardware and/or software patterned after the operation of neurons in the human brain.
Neural networks are used in a variety of applications, such as image and speech recognition, medical diagnosis, and financial forecasting.
"""


post1 = Post(title=title1,content=content1,user_id='1')
post2 = Post(title=title2,content=content2,user_id='1')

post3 = Post(title=title3,content=content3,user_id='2')
post4 = Post(title=title4,content=content4,user_id='2')

db.session.add_all([post1,post2,post3,post4])
db.session.commit()








