from flask_wtf import Form, RecaptchaField
from wtforms import TextAreaField, StringField, PasswordField, validators
from wtforms.fields.html5 import EmailField


class ProjectForm(Form):
    name = StringField('Name',
                       [validators.InputRequired()],
                       render_kw={"placeholder": "My Project",
                                  "data-minlength": "1",
                                  "required": True})
    slug = StringField('Slug',
                       [validators.InputRequired()],
                       render_kw={"placeholder": "my-project",
                                  "data-minlength": "1",
                                  "pattern": "^[a-z0-9-]+$",
                                  "required": True})
    category = StringField('Category',
                           [validators.InputRequired()],
                           render_kw={"placeholder": "Python",
                                      "data-minlength": "1",
                                      "required": True})
    status = StringField('Status',
                         [validators.InputRequired()],
                         render_kw={"placeholder": "56",
                                    "data-minlength": "1",
                                    "required": True})
    github = StringField('GitHub',
                         [validators.Optional()],
                         render_kw={"placeholder": "e.g. DJetelina"})
    url = StringField('URL',
                      [validators.Optional()],
                      render_kw={"placeholder": "https://www.djetelina.cz/"})
    info = TextAreaField('About',
                         [validators.InputRequired()],
                         default="Write something about the project",
                         render_kw={"data-minlength": "50",
                                    "required": True})
    tags = StringField('Tags',
                       [validators.Optional()],
                       render_kw={"placeholder": "flask,discord.py,sqlalchemy"})


class LoginForm(Form):
    email = EmailField('Email',
                       [validators.InputRequired(), validators.Email()],
                       render_kw={"placeholder": "email@email.email",
                                  "data-minlength": "5",
                                  "required": True})
    password = PasswordField('Password',
                             [validators.InputRequired()],
                             render_kw={"required": True,
                                        "data-minlength": "2",
                                        "placeholder": "Password"})
    recaptcha = RecaptchaField()
