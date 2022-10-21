import firebase_admin 
from firebase_admin import credentials
from firebase_admin import firestore


credential = credentials.Certificate("app/serviceAccountKey.json")
firebase_admin.initialize_app(credential)

db = firebase_admin.firestore.client()

# @login_manger.user_loader # originalmente no va, es para arreglar un problema
def get_users():
    return db.collection('users').get()

def get_user(user_id):
    # print(f'user_id:{user_id}')
    return db.collection('users').document(user_id).get()


def user_put(user_data):
    user_ref=db.collection('users').document(user_data.username)
    user_ref.set({'password': user_data.password})



def get_todos(user_id):
    return db.collection('users')\
            .document(user_id)\
            .collection('todos').get()
            #'\' sirve para saltar parrafo.

def put_todo(user_id, description):
    todos_collection_ref = db.collection('users').document(user_id).collection('todos') # usamos como referencia y para tener disponible en una variable donde guardaremos posteriormente la informacion que queremos agregar al usuario.
    todos_collection_ref.add({'description':description, 'done':False})

def delete_todo(user_id, todo_id):
    todo_ref = _get_todo_ref(user_id, todo_id)
    # todo_ref = db.collection('users').document(user_id).collection('todos').document(todo_id)
    todo_ref.delete()

def update_todo(user_id, todo_id, done):
    todo_done = not bool(done)
    todo_ref = _get_todo_ref(user_id, todo_id)
    todo_ref.update({'done':todo_done})


def _get_todo_ref(user_id, todo_id):
    return db.document('users/{}/todos/{}'.format(user_id,todo_id))
