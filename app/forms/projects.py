from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Optional, Length

class ProjectForm(FlaskForm):
    name = StringField("Nome do Projeto", validators=[DataRequired(), Length(max=180)])
    description = TextAreaField("DescriÃƒÂ§ÃƒÂ£o", validators=[Optional(), Length(max=2000)])
    submit = SubmitField("Salvar")
