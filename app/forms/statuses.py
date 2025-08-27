from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Optional, Length

class EquipmentStatusForm(FlaskForm):
    name = StringField("Status", validators=[DataRequired(), Length(max=120)])
    color = StringField("Cor (hex opcional)", validators=[Optional(), Length(max=20)])
    submit = SubmitField("Salvar")
