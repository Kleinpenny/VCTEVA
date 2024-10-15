from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://kleinpenny:vcteva_2024@vcteva-cluster.poyls.mongodb.net/?retryWrites=true&w=majority&appName=VCTEVA-Cluster"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)