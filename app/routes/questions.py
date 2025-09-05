from flask import Blueprint, jsonify, request
from ..models.questions import Question, Category
from ..models import db
from ..schemas.questions import QuestionCreate, CategoryCreate, QuestionResponse, CategoryResponse
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from app.errors.questions_errors import QuestionError, QuestionEmptyError, QuestionValueError

# Создайте новые эндпоинты для создания, чтения, обновления и удаления категорий

categories_bp = Blueprint('categories', __name__, url_prefix='/categories')

@categories_bp.route('/', methods=['POST'])
def create_category():
    data = request.get_json()
    try:
        data = CategoryCreate(**data)
    except ValidationError as e:
        return jsonify({'error': e.errors()}), 422

    category = Category(name=data.name.strip())
    db.session.add(category)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Category with this name already exists'}), 409

    return jsonify(CategoryResponse(id=category.id, name=category.name).model_dump()), 201

@categories_bp.route('/', methods=['GET'])
def get_categories():
    """
    Returns a list of all categories.
    """
    categories = Category.query.all()
    data = []
    for item in categories:
        try:
            res = CategoryResponse.model_validate(item)
            res = res.model_dump()
            data.append(res)
        except ValidationError:
            continue

    return jsonify({'categories': data})


@categories_bp.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """
    Returns a category by id.
    """
    category = Category.query.get(category_id)
    if not category:
        return jsonify({'error': 'Question with that id not found.'}), 404

    return jsonify({'id': category.id, 'name': category.name}), 200


@categories_bp.route('/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    """
    Updates a category by id.
    """
    category = Category.query.get(category_id)
    if not category:
        return jsonify({'error': 'Name with that id not found.'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No name provided.'}), 400

    name = data['name'].strip()
    if not name:
        return jsonify({'error': 'No name category provided.'}), 400

    category.name = name

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': f"Category with this name already exists"}), 409

    return jsonify({'message': f"Категория {category.id} ({category.name}) обновлена"}), 200


@categories_bp.route('/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    """
    Deletes a category by id.
    """
    category = Category.query.get(category_id)
    if not category:
        return jsonify({'error': f"Category with ID {id} not found."}), 404

    # Проверим, чтобы не было вопросов с этой категорией
    if category.questions.count() > 0: # удалять нельзя
        return jsonify({'detail': 'Category has related questions'}), 409

    db.session.delete(category)
    db.session.commit()

    return  jsonify({'message': f"Категория с ID {category_id} удалена"}), 200


questions_bp = Blueprint('questions', __name__, url_prefix='/questions')

@questions_bp.route('/', methods=['GET'])
def get_questions():
    """
    Returns a list of all questions.
    """
    questions = Question.query.all()
    data = []
    for item in questions:
        try:
            res = QuestionResponse.model_validate(item)
            res = res.model_dump()
            data.append(res)
        except ValidationError:
            continue

    return jsonify({'questions': data})


@questions_bp.route('/', methods=['POST'])
def create_question():
    """
    Creates a new question.
    """
    data = request.get_json()
    if not data:
        raise QuestionError('No input data provided')
    text = data.get('question')
    if not text:
        raise QuestionEmptyError('No text provided')
    text = text.strip()
    if not text:
        raise QuestionEmptyError('No text provided')
    if len(text) < 10:
        raise QuestionValueError('Text must be at least 10 characters long')

    data = QuestionCreate(**data)

    # проверим категорию
    category_obj = None
    if data.category_id is not None:  # если указан ID категории (category_id), то будем считать, что категория существует
        category_obj = Category.query.get(data.category_id)  # ищем в базе категорию по ID

        if not category_obj:
            return jsonify({'error': f'Category {data.category_id} not found'}), 404
    # иначе будем пробовать искать по имени категории ("category": {"name": "New category 333"}})
    elif data.category is not None:
        name = data.category.name.strip()
        category_obj = Category.query.filter_by(name=name).first()  # ищем в базе категорию по name

        if not category_obj: # если категории с таким именем нет
            category_obj = Category(name=name) # создадим новую категорию
            db.session.add(category_obj)
            db.session.flush()

    # запишем вопрос уже с категорией
    question = Question(question=data.question, category=category_obj)
    db.session.add(question)
    db.session.commit()

    return  jsonify(QuestionResponse(id=question.id, question=question.question, category=question.category).model_dump()), 201


@questions_bp.route('/<int:question_id>', methods=['GET'])
def get_question(question_id):
    """
    Returns a question by id.
    """
    question = Question.query.get(question_id)
    if not question:
        return jsonify({'error': 'Question with that id not found.'}), 404

    return jsonify(QuestionResponse(id=question.id, question=question.question, category=question.category).model_dump()), 201


@questions_bp.route('/<int:question_id>', methods=['PUT'])
def update_question(question_id):
    """
    Updates a question by id.
    """
    question = Question.query.get(question_id)
    if not question:
        return jsonify({'error': 'Question with that id not found.'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No question provided.'}), 400

    text = data['question'].strip()
    if not text:
        return jsonify({'error': 'No question provided.'}), 400

    question.question = text
    db.session.commit()

    return  jsonify({'message': f"Вопрос обновлен: {question.question}"}), 200


@questions_bp.route('/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    """
    Deletes a question by id.
    """
    question = Question.query.get(question_id)
    if not question:
        return jsonify({'error': 'Question with that id not found.'}), 404

    db.session.delete(question)
    db.session.commit()

    return  jsonify({'message': f"Вопрос с ID {question_id} удален"}), 200