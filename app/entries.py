from datetime import datetime, date
from flask_restful import Resource, reqparse
from flask_jwt_extended import (get_jwt_identity, jwt_required)
from app.models import Entry


class Entries(Resource):
    """
    This resource class will have two methods,a post method that \
    creates a new entry and get method that
    fetches all items from Entry model

    """
    def __init__(self):
        """This method initializes reqparse object """
        self.parser = reqparse.RequestParser()
        self.date = datetime.now().strftime("%d-%m-%Y")
        self.parser.add_argument('title',
                                 type=str, required=True,
                                 help='Title is required!'
                                )
        self.parser.add_argument('content',
                                 type=str, required=True,
                                 help="Content is required"
                                )
    @jwt_required
    def post(self):
        """
        Method: POST
        Creates a new Entry for logged in users
        URL path: mydiary/v1/entries
        """
        data = self.parser.parse_args()
        user_id = get_jwt_identity()[0]
        date = self.date
        title = data['title']
        content = data['content']
        entry = (user_id, date, title, content)
        if Entry().verify_title(title, user_id) == True:
            return{'Server Response':"Title already exist, use a different one."}, 400
        else:
            try:
                return{"This entry was added to your diary":Entry().save(entry)}, 201
            except:
                return{'Server Response':"An error occured try again"}, 500

    @staticmethod
    @jwt_required
    def get():
        """
        Method: GET
        Get all entries of a user
        URL path: mydiary/v1/entries
        """
        user_id = get_jwt_identity()[0]
        entries = Entry().get_all_entries(user_id)
        if len(entries) == 0:
            return {"Server Response":"Your diary is empty"}, 200
        else:
            total_entries = str(len(entries))
            all_user_entries = []
            for user_entries in entries:
                single_entry = {}
                single_entry["id"] = user_entries[0]
                single_entry["date"] = user_entries[1]
                single_entry["title"] = user_entries[2]
                single_entry["content"] = user_entries[3]
                all_user_entries.append(single_entry)
                msg = "You currently have "+total_entries+" diary entries."
                response = {msg:all_user_entries}
            return response, 200

class EntryList(Resource):
    """
    This resource class has three methods,
    a get method that get an entry by id,put method that
    updates an entry by id if it exists and delete method that
    delete an entry by id.All endpoints are protected.
    """

    def __init__(self):
        """This method initializes reqparse object """
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('title',
                                 type=str,
                                 required=True,
                                 help='No enty title provided',
                                )
        self.parser.add_argument('content',
                                 type=str,
                                 required=True,
                                 help='No entry content provided'
                                )

    @staticmethod
    @jwt_required
    def get(entryId):
        """
        Gets an entry using its id
        """
        user_id = get_jwt_identity()[0]
        entry = Entry().get_by_id(entryId, user_id)
        if entry:
            return {"Entry fetched Successuflly":entry[0]}, 200
        return {'Message':"Entry requested does not exist"}, 404

    @staticmethod
    @jwt_required
    def delete(entryId):
        """
        Method: DELETE
        Deletes an entry by it's Id
        URL path: mydiary/v1/entries/<int:entryId>
        """
        try:
            entry_id = Entry().get_entry_id(entryId)
            if entry_id is None:
                return {'message':"Entry does not exist"}, 404
            else:
                Entry().delete_entry(entryId)
            return {'message':'Your entry was successfully deleted'}, 200
        except:
            return{"Server Response":"An internal error occured"}, 500

    @jwt_required
    def put(self, entryId):
        """
        Method: PUT
        Modifies an entry by it's Id
        URL path: mydiary/v1/entries/<int:entryId>
        """
        user_id = get_jwt_identity()[0]
        data = self.parser.parse_args()
        title = data['title']
        content = data['content']
        updated_data = (title, content)
        entry = Entry().get_entry_id(entryId)
        if entry is None:
            return {'message':"Entry does not exist"}, 404
        if entry:
            entry_Date = Entry().entry_date(entryId)[0]
            today_date = date.today().strftime("%d-%m-%Y")
            if today_date == entry_Date:
                if Entry().verify_title(title, user_id) == True:
                    return{'Server Response':"Title already exist, use a different one."}, 400
                else:
                    Entry().update_entry(updated_data, entryId)
                    return{"Server Response":"Entry Updated successfully"}, 200
            else:
                return{'Server Response':'Entry cannot be updated \
                 because it was not created today'}, 400

        return{"Server Response":"An error ocurred while processing your request"}, 500
