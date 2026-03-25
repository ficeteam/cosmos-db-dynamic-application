from azure.cosmos import CosmosClient
from flask import Flask, render_template, redirect, request

COSMOS_URI = " "
COSMOS_KEY = " "

DATABASE_NAME = "gtudb"
CONTAINER_NAME = "container"

PARTITION_KEY_FIELD = "/state"


client = CosmosClient(COSMOS_URI, credential=COSMOS_KEY)
database = client.get_database_client(DATABASE_NAME)
container = database.get_container_client(CONTAINER_NAME)

print("Connected to Cosmos DB successfully!")

app = Flask(__name__)

@app.route('/')
def Index():
    # lst = []
    query = "SELECT * FROM c"
    items = container.query_items(
        query=query,
        enable_cross_partition_query=True
    )
    
    # print(items)
    # for item in items:
    #     lst.append(items)
    return render_template('index.html',data=items)

@app.route('/create',methods=["POST"])
def Create():
    id = request.form.get('id')
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    state = request.form.get('state')
   
    item = {
        "id": id,
        "state": state,
        "firstname": fname,
        "lastname": lname,
    }

    container.upsert_item(item)

    return redirect('/')


# item = {
#     "id": "103",
#     "state":"Gujarat",
#     "firstname": "Rahul",
#     "lastname": "Roy",
#     "city": "surat",
# }

# container.upsert_item(item)
# print("Item Inserted Successfully....!")

# query = "SELECT * FROM c"
# items = container.query_items(
#     query=query,
#     enable_cross_partition_query=True
# )

# # print(items)
# for item in items:
#     print(item)

# updated_item = {
#     "id": "102",
#     "state":"Gujarat",
#     "firstname": "Rohit",
#     "lastname": "Singh",
#     "city": "Vadodara"
# }

# container.upsert_item(updated_item)
# print("Item updated!")


# container.delete_item(
#     item="100",
#     partition_key="Gujarat"
# )
# print("Deleted Successfully....")

if __name__ == "__main__":
    app.run()
