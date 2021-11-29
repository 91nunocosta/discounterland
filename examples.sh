#!/bin/bash

printf "\n\n Create a promotion\n"
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

printf "\n\n Create a discount\n"
curl --location --request POST 'http://0.0.0.0:5000/consumers/61a2d3be596808c5d69dd11b/discounts' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI5MW51bm9jb3N0YUBnbWFpbC5jb20iLCJpYXQiOjE2MTY2MTY5NjN9.tMQoy_6ROA_sxWR1exWVeRZZZFR4qvMbO2Szos_XIMI' \
--header 'Content-Type: application/json' \
--data-raw '{
  "promotion_id": "61a2d5606ac07b74c824f1a9"
}'
