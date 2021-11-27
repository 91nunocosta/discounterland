#!/bin/bash

printf "\n\n Create discount\n"
curl --location --request POST 'http://0.0.0.0:5000/brands/61a22c8f43cf71b9933afdd7/promotions' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI5MW51bm9jb3N0YUBnbWFpbC5jb20iLCJpYXQiOjE2MTY2MTY5NjN9.tMQoy_6ROA_sxWR1exWVeRZZZFR4qvMbO2Szos_XIMI' \
--header 'Content-Type: application/json' \
--data-raw '{
  "expiration_date": "2022-11-25T16:51:02.003Z",
  "product": {
    "name": "Nutella",
    "images": [
      "https://images.jumpseller.com/store/hercules-it-llc/10188702/Nutella.jpg?1623999446"
    ]
  },
  "discounts_quantity": 10
}'

printf "\n\n Create a promotion \n"
curl --location --request POST 'http://0.0.0.0:5000/consumers/61a22cb797321cee10c8df49/discounts' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0MTI5ODM0OTg5IiwibmFtZSI6IlBhdHJpY2siLCJpYXQiOjE1MTYyMzkwMjJ9.UNxtO1rOKdkMawosiKiaQ3yupcKZWAvev1N0Lb49m28' \
--header 'Content-Type: application/json' \
--data-raw '{
  "promotion_id": "/promotions/9e169116-e3de-41cc-952a-149ed1cc4b40"
}'

