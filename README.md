# news_database

to start:
1) install requirements
2) cd app
3) sh uvic.sh
This script will deploy db and api to the provided in the config files ports at localhost.

There are only four functions:
add_channel --- adds channel
```
curl -X POST "http://0.0.0.0:1488/add_channel" \
     -H "Content-Type: application/json" \
     -d '{"channel_name": "TechNews"}'
```

add_news --- adds news
```
curl -X POST "http://0.0.0.0:1488/add_news" -H "Content-Type: application/json" -d '{                                             
           "message": "TechNews: news",
           "date": "2025-01-15T10:00:00",
           "channel": "TechNews",
           "topic": "RandomTopic"
         }'
```
select_news --- select news within the interval of start_time and end_time
```
curl -X GET "http://0.0.0.0:1488/select_news" \
     -H "Content-Type: application/json" \
     -d '{
           "start_date": "2025-01-15T00:00:00",
           "end_date": "2025-01-16T23:59:59"
         }'
```

flush --- delete news remaining n last days
note: if you want to delete all the news, set remain_n_days=0
```
curl -X 'POST' \
  'http://127.0.0.1:1488/flush' \
  -H 'Content-Type: application/json' \
  -d '{
    "remain_n_days": 1
  }'
```

