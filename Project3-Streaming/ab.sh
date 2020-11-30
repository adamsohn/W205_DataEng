#!/bin/sh
docker-compose exec mids ab -n 2 -H "Host: user2.att.com" http://localhost:5000/purchase_a_sword/foam
docker-compose exec mids ab -n 3 -H "Host: user2.att.com" http://localhost:5000/purchase_a_sword/strongium
docker-compose exec mids ab -n 4 -H "Host: user1.comcast.com" http://localhost:5000/join_guild/guildilocks
docker-compose exec mids ab -n 5 -H "Host: user1.comcast.com" http://localhost:5000/join_guild/mids_united
docker-compose exec mids ab -n 6 -H "Host: user1.comcast.com" http://localhost:5000/take_nap/cat
docker-compose exec mids ab -n 7 -H "Host: user1.comcast.com" http://localhost:5000/take_nap/power
docker-compose exec mids ab -n 8 -H "Host: user2.att.com" http://localhost:5000/consume_fermented_beverage/beer
docker-compose exec mids ab -n 9 -H "Host: user2.att.com" http://localhost:5000/consume_fermented_beverage/mead
docker-compose exec mids ab -n 10 -H "Host: user2.att.com" http://localhost:5000/
docker-compose exec mids ab -n 11 -H "Host: user1.comcast.com" http://localhost:5000/funtime