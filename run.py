from flask import jsonify
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from app.models import db
from app.errors.questions_errors import QuestionError, QuestionEmptyError, QuestionValueError

from app import create_app

app = create_app()

@app.errorhandler(ValidationError)
def handle_validation_error(e):
    return jsonify({"error": e.errors()})

@app.errorhandler(SQLAlchemyError)
def handle_db_error(e):
    db.session.rollback()
    return jsonify({"error": str(e)})

@app.errorhandler(QuestionError)
def handle_db_error(e):
    return jsonify({"error": str(e.message)}), 400

@app.errorhandler(QuestionEmptyError)
def handle_db_error(e):
    return jsonify({"error": str(e.message)}), 400

@app.errorhandler(QuestionValueError)
def handle_db_error(e):
    return jsonify({"error": str(e.message)}), 400



if __name__ == '__main__':
    app.run(debug=True)

