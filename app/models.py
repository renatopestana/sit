from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db

class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class User(UserMixin, TimestampMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(140), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    cpf = db.Column(db.String(14), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    role = db.Column(db.String(50), default="user")

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

class Client(TimestampMixin, db.Model):
    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(2), nullable=False)  # PF ou PJ

    # Comuns
    nome_razao = db.Column(db.String(180), nullable=False)
    endereco = db.Column(db.String(300), nullable=False)

    # PF
    nacionalidade = db.Column(db.String(80))
    estado_civil = db.Column(db.String(60))
    profissao = db.Column(db.String(120))
    rg = db.Column(db.String(30))
    orgao_emissor_rg = db.Column(db.String(50))
    cpf = db.Column(db.String(14))
    email = db.Column(db.String(255))
    telefone = db.Column(db.String(30))

    # PJ
    cnpj = db.Column(db.String(18))
    representante_nome = db.Column(db.String(180))
    representante_email = db.Column(db.String(255))
    representante_telefone = db.Column(db.String(30))
    representante_funcao = db.Column(db.String(120))

class Dealer(TimestampMixin, db.Model):
    __tablename__ = "dealers"

    id = db.Column(db.Integer, primary_key=True)
    razao_social = db.Column(db.String(180), nullable=False)
    endereco = db.Column(db.String(300), nullable=False)
    cnpj = db.Column(db.String(18), nullable=False, unique=True)

    representante_nome = db.Column(db.String(180), nullable=False)
    representante_email = db.Column(db.String(255), nullable=False)
    representante_telefone = db.Column(db.String(30), nullable=False)
    representante_funcao = db.Column(db.String(120), nullable=False)

class Project(TimestampMixin, db.Model):
    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(180), unique=True, nullable=False)
    description = db.Column(db.Text)

class EquipmentStatus(TimestampMixin, db.Model):
    __tablename__ = "equipment_statuses"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    color = db.Column(db.String(20))  # hex opcional

class Equipment(TimestampMixin, db.Model):
    __tablename__ = "equipment"
    id = db.Column(db.Integer, primary_key=True)

    # Colunas mapeadas da planilha
    name = db.Column(db.String(180), nullable=False)           # Item
    pn = db.Column(db.String(80))                              # PN
    model_number = db.Column(db.String(120))                   # Model Number / Model
    serial_number = db.Column(db.String(120))                  # SN / Serial Number
    machine_installed = db.Column(db.String(180))              # Machine Installed
    image_ref = db.Column(db.String(255))                      # Imagem de Referência

    # Extras úteis
    asset_tag = db.Column(db.String(80))                       # espelha PN se desejar
    category = db.Column(db.String(120))                       # opcional
    brand = db.Column(db.String(120))                          # opcional
    notes = db.Column(db.Text)                                 # Obs

    # Associações
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    current_responsible_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    location_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    status_id = db.Column(db.Integer, db.ForeignKey('equipment_statuses.id'))

    owner = db.relationship('User', foreign_keys=[owner_id], lazy='joined')
    current_responsible = db.relationship('User', foreign_keys=[current_responsible_id], lazy='joined')
    location = db.relationship('Client', lazy='joined')
    project = db.relationship('Project', lazy='joined')
    status = db.relationship('EquipmentStatus', lazy='joined')
