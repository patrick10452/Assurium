# AssuriumChatbotProject/setup.py
from database import init_database, insert_sample_data

def main():
    print("Initializing database...")
    if init_database():
        print("Database initialized successfully!")
        print("Inserting sample data...")
        if insert_sample_data():
            print("Sample data inserted successfully!")
        else:
            print("Failed to insert sample data.")
    else:
        print("Failed to initialize database.")

if __name__ == "__main__":
    main()