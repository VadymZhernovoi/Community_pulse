from . import db
"""
Создание модели Category:
Создайте новую модель Category с использованием SQLAlchemy в модуле models.
Модель должна содержать следующие поля:
    id: первичный ключ, целое число, авто-инкремент.
    name: строка, название категории, не должно быть пустым.
Модель Question должна быть обновлена, чтобы включить ссылку на Category через внешний ключ.
"""

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, default='')
    questions = db.relationship('Question', backref='category', lazy='dynamic')

    def __repr__(self):
        return f'Category: {self.id=},{self.name=}'

    def __str__(self):
        return self.name

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    responses = db.relationship('Response', backref='question', lazy='dynamic')
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    def __repr__(self):
        return f'Question: {self.id=},{self.question=}'

    def __str__(self):
        return self.question


class Statistic(db.Model):
    __tablename__ = 'statistics'

    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), primary_key=True)
    agree_count = db.Column(db.Integer, nullable=False, default=0)
    disagree_count = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f'Statistic: {self.id=},{self.agree_count=},{self.disagree_count=}'

    def __str__(self):
        return f'{self.question_id} {self.agree_count} {self.disagree_count}'


