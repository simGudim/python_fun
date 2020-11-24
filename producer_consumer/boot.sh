#!/bin/sh
source venv/bin/activate
# flask db init
# flask db migrate -m "msg"
# while true; do
#     flask db upgrade
#     if [[ "$?" == "0" ]]; then
#         break
#     fi
#     echo Upgrade command failed, retrying in 5 secs...
#     sleep 5
# done
# rm -rf migrations
# flask db init
# flask db migrate -m "msg"
# flask db upgrade
flask run --host=0.0.0.0
