
import unittest
from flask import request, make_response, redirect, render_template, session, url_for, flash
from flask_login import login_required, current_user

from app import create_app
from app.forms import LoginForm, TodoForm, DeleteTodoForm, UpdateTodoForm
from app.firestore_service import delete_todo, get_users, get_todos, put_todo, delete_todo, update_todo


app= create_app()


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)

#aqui manejamos el error 404 archivo o ruta no encontrada, con el decorador propio de flask .errorhandler, le damos en los parentesis el tipo de error a manejar, luego en la funcion que recibe el error retornamos el html que queremos renderizar, en el contexto le pasamos el error.
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html', error=error)

@app.route('/task_admin_about')
def task_admin_about():
    
    return render_template('task_admin_about.html')

@app.route('/')
def index():
    user_ip= request.remote_addr
    
    users = get_users()
    for user in users:
        print(user.id)
        print(user.to_dict()['password'])

    response = make_response(redirect('/hello')) 
    session['user_ip'] = user_ip

    return response
        
@app.route('/hello', methods=['GET', 'POST'])
@login_required
def hello():
    user_ip= session.get('user_ip')
    username = current_user.id
    todo_form = TodoForm()
    delete_form = DeleteTodoForm()
    update_form= UpdateTodoForm()

    context = {
        'user_ip': user_ip,
        'todos':get_todos(user_id=username),
        'username': username,
        'todo_form': todo_form,
        'delete_form': delete_form,
        'update_form': update_form,
        } # creamos una lista con las variables a user dentro del template html, asi solo pasamos un parametro dentro.

    form = TodoForm(request.form) # esta linea funciona cuando se manda un request, es decir, que cuando damos submit a la forma que se renderiza, entonces en esta variable se guarda la informacion que se ingresa en la forma. Esta informacion la podemos llamar despues por ejemplo mediante 'form.description.data' siendo 'description' la variable que queremos obtener.
    if request.method== 'POST':
        put_todo(user_id=username, description=form.description.data)

        flash('Tu tarea se creo con exito!')

        return redirect(url_for('hello'))
        

    return render_template('hello.html', **context) # aqui decimos que template de html queremos renderizar, le agregamos la variable 'context' que contiene todas las demas variables que podemos usar dentro del archivo html 'hello'. el doble asterisco(**) expande todas las variables dentro del template, asi podremos llamar estas variables solo con el nombre y no por ejemplo mediante context.user_ip.


@app.route('/todos/delete/<todo_id>', methods=['POST'])
def delete(todo_id):
    user_id = current_user.id
    delete_todo(user_id=user_id, todo_id=todo_id)
    
    return redirect(url_for('hello'))

@app.route('/todos/update/<todo_id>/<int:done>', methods=['POST'])
def update(todo_id, done):
    user_id = current_user.id

    update_todo(user_id=user_id, todo_id=todo_id, done=done)
    
    return redirect(url_for('hello'))