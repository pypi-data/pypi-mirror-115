from pymongo import MongoClient
from fire import Fire
from bson import ObjectId


class Const:
    class State:
        TODO = "todo"
        INPROGRESS = "inprogress"
        DONE = "done"
        FAIL = "fail"

    STATE = "state"
    DATA = "data"
    COUNT = "count"
    RESULT = "result"
    ID = "_id"


class RSQ:
    def __init__(
        self,
        mongo_url: str = "localhost",
        db_name: str = "rsq",
        collection_name: str = "rsq",
    ):
        client = MongoClient(mongo_url)
        database = client[db_name]
        self.collection = database[collection_name]

    def list_task(self, _id: str = None, state=None):
        query = {} if state is None else {Const.STATE: state}
        if _id is not None:
            query[Const.ID]: ObjectId(_id)
        return list(self.collection.find(query))

    def results(self, _id=None, query=None):
        query = {Const.STATE: Const.State.DONE} if query is None else query
        if _id is not None:
            query.update({Const.ID: ObjectId(_id)})
        return list(self.collection.find(query))

    def push(self, **kwargs):
        result = self.collection.insert_one(
            {Const.STATE: Const.State.TODO, Const.DATA: kwargs}
        )
        return str(result.inserted_id)

    def pull(self, additional_query=None):

        query = {Const.STATE: Const.State.TODO}
        if additional_query is not None:
            query.update(additional_query)

        doc = self.collection.find_one_and_update(
            query,
            {"$set": {Const.STATE: Const.State.INPROGRESS}},
        )
        if doc is None:
            return None
        return {
            Const.ID: str(doc[Const.ID]),
            Const.DATA: doc[Const.DATA],
        }

    def done(self, _id: str, result=None):
        return self.collection.find_one_and_update(
            {Const.ID: ObjectId(_id)},
            {"$set": {Const.STATE: Const.State.DONE, Const.RESULT: result}},
        )

    def reset(self, _id: str = None, state: str = Const.State.TODO):
        if _id is None:
            self.collection.update_many({}, {"$set": {Const.STATE: state}})
        else:
            update_result = self.collection.update_one(
                {Const.ID: ObjectId(_id)}, {"$set": {Const.STATE: state}}
            )

        return (update_result.matched_count, update_result.modified_count)

    def count(self, state=None):
        query = {} if state is None else {Const.STATE: state}
        return self.collection.count_documents(query)

    def remove(self, _id: str = None):
        query = {}
        if _id is not None:
            query = {Const.ID: ObjectId(_id)}
        return self.collection.remove(query)


if __name__ == "__main__":
    Fire(RSQ)
