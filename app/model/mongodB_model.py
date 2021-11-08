from bson.objectid import ObjectId
from requests.sessions import session


class Model(dict):
    __getattr__ = dict.get
    __delattr__ = dict.__delitem__
    __setattr__ = dict.__setitem__

    def save(self, session=None):
        if not self._id:
            self.collection.insert_one(self, session=session)
        else:
            self.collection.replace_one(
                {"_id": ObjectId(self._id)}, self, session=session
            )

    def update(self, update, session=None):
        self.collection.update_one(
            {"_id": ObjectId(self._id)}, {"$set": update}, session=session
        )

    def reload(self):
        if self._id:
            self.update(self.collection.find_one({"_id": ObjectId(self._id)}))

    def remove(self, session=None):
        if self._id:
            self.collection.delete_one({"_id": ObjectId(self._id)}, session=session)
            self.clear()
