from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from app import db, login
from datetime import datetime

from app.utils import generate_qr_base64

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'  # Явно задаем имя таблицы
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), unique=True)
    l_name = db.Column(db.String(32))
    f_name = db.Column(db.String(32))
    m_name = db.Column(db.String(32))
    password = db.Column(db.String(256))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))  # Изменено на groups.id
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username} {self.l_name} {self.f_name}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    

class Group(db.Model):
    __tablename__ = 'groups'  # Явно задаем имя таблицы во множественном числе
    
    id = db.Column(db.Integer, primary_key=True)
    g_name = db.Column(db.String(32), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    users = db.relationship('User', backref='user_group', lazy='dynamic')

    def __repr__(self):
        return f'<Group {self.g_name}>'
    

class TechGroup(db.Model):
    __tablename__ = 'tech_groups'  # Явно задаем имя таблицы
    
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(64), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    techs = db.relationship('Tech', backref='tech_group', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<TechGroup {self.group_name}>'


class Tech(db.Model):
    __tablename__ = 'tech'  # Явно задаем имя таблицы
    
    id = db.Column(db.Integer, primary_key=True)
    tech_group_id = db.Column(db.Integer, db.ForeignKey('tech_groups.id', ondelete='CASCADE'))  # Исправлено на tech_groups.id
    tech_name = db.Column(db.String(256))
    description = db.Column(db.Text, nullable=True)
    serial_number = db.Column(db.String(128), nullable=True, unique=True)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Отношение к QR-кодам
    qr_codes = db.relationship('QR_codes', backref='tech', lazy='dynamic', cascade='all, delete-orphan')
    # Отношение к комментариям
    comments = db.relationship('Comment', backref='tech', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Tech {self.id}: {self.tech_name}>'


class QR_codes(db.Model):
    __tablename__ = 'qr_codes'  # Явно задаем имя таблицы
    
    id = db.Column(db.Integer, primary_key=True)
    tech_id = db.Column(db.Integer, db.ForeignKey('tech.id', ondelete='CASCADE'))
    qr_data = db.Column(db.Text)
    qr_type = db.Column(db.String(32), default='tech')
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Исправлено на users.id
    is_active = db.Column(db.Boolean, default=True)

    # Уникальный constraint для предотвращения дублирования QR-кодов для одной техники
    __table_args__ = (
        db.UniqueConstraint('tech_id', 'qr_type', name='_tech_qrtype_uc'),
    )

    def __repr__(self):
        return f'<QR_code {self.id} for Tech:{self.tech_id} ({self.qr_type})>'
    
    def generate_and_store(self, payload: str = None) -> str:
        payload = payload or self.qr_data or f"tech:{self.tech_id}"
        img_b64 = generate_qr_base64(payload)
        self.qr_data = img_b64
    
class Status(db.Model):
    __tablename__ = 'status'

    id = db.Column(db.Integer, primary_key=True)
    status_name = db.Column(db.String(64))

    techs = db.relationship('Tech', backref='status', lazy='dynamic')

    def __repr__(self):
        return f'<Status {self.status_name}>'
    
class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    tech_id = db.Column(db.Integer, db.ForeignKey('tech.id', ondelete='CASCADE'), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='comments')

    def __repr__(self):
        return f'<Comment {self.id} for Tech:{self.tech_id}>'