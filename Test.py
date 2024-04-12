from mongoengine import connect
def test_connection():
    # Replace <your_connection_string> with your actual MongoDB Atlas connection string
    connection_string = "mongodb+srv://camping:SqP6B8wLx62DsUf6@cluster0.l5yaw7u.mongodb.net/TestCamping"
    
    try:
        # Connect to MongoDB Atlas using mongoengine
        connect(db='TestCamping',
                    host='cluster0.l5yaw7u.mongodb.net',
                    port=27017,
                    username='camping',
                    password='SqP6B8wLx62DsUf6',
                    authentication_source='admin')
        
        print("Connection to MongoDB Atlas using mongoengine successful!")
    except Exception as e:
        print(f"Failed to connect to MongoDB Atlas using mongoengine: {e}")
if __name__ == "__main__":
    test_connection()