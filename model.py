from flask_wtf import FlaskForm
from wtforms import FileField, RadioField, SubmitField
from wtforms.validators import InputRequired, DataRequired

class InputForm(FlaskForm):
    filename = FileField([InputRequired()])

    project = RadioField('Project', [DataRequired()],
        choices=[('Golden Toad', 'goldenToad'), ('Not Golden Toad', 'notGoldenToad')]
    )

    submit = SubmitField('Submit')
