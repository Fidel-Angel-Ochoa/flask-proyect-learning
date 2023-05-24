from wtforms import StringField, PasswordField, SubmitField,Form, validators


class LoginForm(Form):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    submit = SubmitField('Send')

class TodoForm(Form):
    description = StringField('Description', [validators.DataRequired()])
    submit = SubmitField('Create')
    print(f'description before send: {description}')

class DeleteTodoForm(Form):
    submit= SubmitField('Delete')

class UpdateTodoForm(Form):
    submit = SubmitField('Update')