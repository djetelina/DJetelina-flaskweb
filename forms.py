from flask_wtf import Form
from wtforms import TextAreaField, StringField, validators

class ProjectForm(Form):
    name = StringField('Name', [validators.InputRequired()], render_kw={"placeholder": "My Project"})
    slug = StringField('Slug', [validators.InputRequired()], render_kw={"placeholder": "my-project"})
    category = StringField('Category', [validators.InputRequired()], render_kw={"placeholder": "Python"})
    status = StringField('Status', [validators.InputRequired()], render_kw={"placeholder": "56"})
    github = StringField('GitHub', [validators.Optional()], render_kw={"placeholder": "https://github.com/iScrE4m/DJetelina"})
    url = StringField('URL', [validators.Optional()], render_kw={"placeholder": "https://www.djetelina.cz/"})
    info = TextAreaField('About', [validators.InputRequired()], default="Write something about the project")
