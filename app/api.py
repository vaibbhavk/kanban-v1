from flask_restful import Resource
from flask_restful import fields, marshal_with, reqparse
from app.validation import ListValidationError, CardValidationError, UserValidationError
from app.database import db
from app.models import User, List, Card
from datetime import datetime

other_response = {
    "message": fields.String
}

list_output_fields = {
    "list_id": fields.Integer,
    "name": fields.String,
    "user": fields.Integer,
    "created_at": fields.DateTime,
    "updated_at": fields.DateTime
}

create_list_parser = reqparse.RequestParser()
create_list_parser.add_argument('name')
create_list_parser.add_argument('user_id')

update_list_parser = reqparse.RequestParser()
update_list_parser.add_argument('name')


card_output_fields = {
    "card_id": fields.Integer,
    "title": fields.String,
    "content": fields.String,
    "deadline": fields.String,
    "completed": fields.Integer,
    "list": fields.Integer,
    "created_at": fields.DateTime,
    "updated_at": fields.DateTime,
    "completed_datetime": fields.DateTime,
}


create_card_parser = reqparse.RequestParser()
create_card_parser.add_argument('title')
create_card_parser.add_argument('content')
create_card_parser.add_argument('deadline')
create_card_parser.add_argument('completed')
create_card_parser.add_argument('list')

update_card_parser = reqparse.RequestParser()
update_card_parser.add_argument('title')
update_card_parser.add_argument('content')
update_card_parser.add_argument('deadline')
update_card_parser.add_argument('completed')



# CRUD on Lists
class ListAPI(Resource):
    @marshal_with(list_output_fields)
    def get(self, id): # get a list by id
        list = List.query.get(id)

        if list:
            return list, 200
        else:
            raise ListValidationError(status_code = 404, error_code = "L104", error_message =  "List does not exist")


    @marshal_with(list_output_fields)
    def post(self): # create a list for a user
        args = create_list_parser.parse_args()
        name = args.get("name", None)
        user_id = args.get("user_id", None)

        if name is None:
            raise ListValidationError(status_code = 400, error_code = "L101", error_message =  "name is required")
        
        if user_id is None:
            raise ListValidationError(status_code = 400, error_code = "L102", error_message =  "user id is required")

        user = User.query.get(user_id)

        if user is None:
            raise UserValidationError(error_code = "U101", error_message = "User does not exist")
        
        lists = db.session.query(List).filter((List.user == user_id)).all()

        if len(lists)>4:
            raise ListValidationError(status_code = 400, error_code = "L103", error_message =  "Cannot create more than 5 lists for a user")
        
        new_list = List(name=name, user=user_id)
        db.session.add(new_list)
        db.session.commit()
        db.session.refresh(new_list)

        return new_list, 201


    
    @marshal_with(list_output_fields)
    def put(self, id): # update a list by id
        args  = update_list_parser.parse_args()
        name = args.get('name', None)

        if name is None:
            raise ListValidationError(status_code = 400, error_code = "L101", error_message =  "name is required")

        list = List.query.get(id)

        if list is None:
            raise ListValidationError(status_code = 404, error_code = "L104", error_message =  "List does not exist")

        list.name = name
        db.session.add(list)
        db.session.commit()

        return list, 200


    def delete(self, id): # delete a list by id
        list = List.query.get(id)

        if list is None:
            raise ListValidationError(status_code = 404, error_code = "L104", error_message =  "List does not exist")

        db.session.delete(list)
        db.session.commit()

        response = {
            "message": "List has been deleted successfully"
        }

        return response, 200


    


# CRUD on Cards
class CardAPI(Resource):
    @marshal_with(card_output_fields)
    def get(self, id): # get a card by id
        card = Card.query.get(id)

        if card:
            return card, 200
        else:
            raise CardValidationError(status_code = 404, error_code = "C106", error_message =  "Card does not exist")



    @marshal_with(card_output_fields)
    def post(self): # create a card for a list
        args = create_card_parser.parse_args()
        title = args.get("title", None)
        content = args.get("content", None)
        deadline = args.get("deadline", None)
        completed = args.get("completed", None)
        list = args.get("list", None)

        if title is None:
            raise CardValidationError(status_code = 400, error_code = "C101", error_message =  "title is required")
        
        if content is None:
            raise CardValidationError(status_code = 400, error_code = "C102", error_message =  "content is required")
        
        if deadline is None:
            raise CardValidationError(status_code = 400, error_code = "C103", error_message =  "deadline is required")
        
        if completed is None:
            raise CardValidationError(status_code = 400, error_code = "C104", error_message =  "completed flag is required")
        
        if list is None:
            raise CardValidationError(status_code = 400, error_code = "C105", error_message =  "list id is required")

        list_q = List.query.get(list)

        if list_q is None:
            raise ListValidationError(status_code = 404, error_code = "L104", error_message =  "List does not exist")

        deadline = datetime.strptime(deadline, '%Y-%m-%d').date()

        completed_datetime = None

        if completed == '1':
            completed_datetime = datetime.now()
        
        new_card = Card(title=title, content=content, deadline=deadline, completed=completed, list=list, completed_datetime=completed_datetime)
        db.session.add(new_card)
        db.session.commit()
        db.session.refresh(new_card)

        return new_card, 201


    
    @marshal_with(card_output_fields)
    def put(self, id): # update a card by id
        args = update_card_parser.parse_args()
        title = args.get("title", None)
        content = args.get("content", None)
        deadline = args.get("deadline", None)
        completed = args.get("completed", None)

        if title is None:
            raise CardValidationError(status_code = 400, error_code = "C101", error_message =  "title is required")
        
        if content is None:
            raise CardValidationError(status_code = 400, error_code = "C102", error_message =  "content is required")
        
        if deadline is None:
            raise CardValidationError(status_code = 400, error_code = "C103", error_message =  "deadline is required")
        
        if completed is None:
            raise CardValidationError(status_code = 400, error_code = "C104", error_message =  "completed flag is required")

        card = Card.query.get(id)

        if card is None:
            raise CardValidationError(status_code = 404, error_code = "C106", error_message =  "Card does not exist")

        deadline = datetime.strptime(deadline, '%Y-%m-%d').date()

        completed_datetime = None
        
        if completed == '1':
            completed_datetime = datetime.now()


        card.title = title
        card.content = content
        card.deadline = deadline
        card.completed = completed
        card.completed_datetime = completed_datetime


        db.session.add(card)
        db.session.commit()

        return card, 200


    def delete(self, id): # delete a card by id
        card = Card.query.get(id)

        if card is None:
            raise CardValidationError(status_code = 404, error_code = "C106", error_message =  "Card does not exist")

        db.session.delete(card)
        db.session.commit()

        response = {
            "message": "Card has been deleted successfully"
        }

        return response, 200