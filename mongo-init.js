db = new Mongo().getDB("eve");
db.accounts.insert(
  {
      "_id": ObjectId("61a2d3be596808c5d69dd11b"),
      "username": "91nunocosta@gmail.com",
      "password": "unsercurepassword"
  },
);

db.brands.insert(
    {
        "_id": ObjectId("61a22c8f43cf71b9933afdd7"),
    }
);

db.brand_managers.insert(
  {
    "account_id": ObjectId("61a2d3be596808c5d69dd11b"),
    "brand_id": ObjectId("61a22c8f43cf71b9933afdd7"),
  }
);

db.promotions.insert( {
  "_id": ObjectId("61a2d5606ac07b74c824f1a9"),
  "brand_id": "61a22c8f43cf71b9933afdd7",
  "expiration_date": new Date("2100-1-1"),
  "product": {
      "name": "Nutella",
      "images": [
          "https://images.jumpseller.com/store/hercules-it-llc/10188702/Nutella.jpg"
      ]
  },
  "discounts_quantity": 10,
});

