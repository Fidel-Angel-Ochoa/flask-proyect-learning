from wtforms import StringField, PasswordField, SubmitField,Form, validators


class LoginForm(Form):
    username = StringField('Nombre de usuario', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    submit = SubmitField('Enviar')

class TodoForm(Form):
    description = StringField('descripcion', [validators.DataRequired()])
    submit = SubmitField('Crear')
    print(f'descripcion antes de enviar: {description}')

class DeleteTodoForm(Form):
    submit= SubmitField('Borrar')

class UpdateTodoForm(Form):
    submit = SubmitField('Actualizar')