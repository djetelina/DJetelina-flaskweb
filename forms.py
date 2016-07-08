from flask_wtf import Form
from wtforms import TextAreaField, StringField, validators


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
                         render_kw={"placeholder": "https://github.com/iScrE4m/DJetelina"})
    url = StringField('URL',
                      [validators.Optional()],
                      render_kw={"placeholder": "https://www.djetelina.cz/"})
    info = TextAreaField('About',
                         [validators.InputRequired()],
                         default="Write something about the project",
                         render_kw={"data-minlength": "50",
                                    "required": True})
