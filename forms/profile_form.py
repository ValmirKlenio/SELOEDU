from flask_wtf import FlaskForm # type: ignore
from wtforms import StringField, TextAreaField, SubmitField # type: ignore
from wtforms.validators import Optional, Length # type: ignore
from flask_wtf.file import FileField, FileAllowed # type: ignore

class ProfileForm(FlaskForm):
    telefone    = StringField("Telefone", validators=[Optional(), Length(max=11)])
    instituicao = StringField("Instituição", validators=[Optional(), Length(max=100)])
    cargo       = StringField("Cargo", validators=[Optional(), Length(max=50)])
    bio         = TextAreaField("Bio", validators=[Optional(), Length(max=1000)])
    foto        = FileField("Foto de Perfil", validators=[FileAllowed(["jpg","jpeg","png","gif"], "Apenas imagens!")])
    submit      = SubmitField("Salvar")