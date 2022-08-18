from wtforms import Form, StringField, validators


class LoginForm(Form):
    """name"""
    name = StringField('Nickname', [
            validators.DataRequired(message="Please write your Nickname!!"),
            validators.Length(min=3, max=15, message="You Nickname must be between 3 and 15 characters long. "),
            validators.Regexp(r'^[\w.@+-]+$', message="Your Nickname may have some invalid characters.") 
        ])