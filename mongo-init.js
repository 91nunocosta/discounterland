db = new Mongo().getDB("eve");
db.accounts.insert(
  {
      "_id": ObjectId(""),
      "username": "91nunocosta@gmail.com",
      "password": "unsercurepassword"
  });

db.brands.insert(
    {
        "_id": ObjectId("61a22c8f43cf71b9933afdd7"),
    });
db.consumers.insert(
    {
        "_id": ObjectId("61a22cb797321cee10c8df49"),
    });
