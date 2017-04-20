#!/bin/bash


#docker restart database
#docker restart backend

xfce4-terminal --tab -T STDOUT-Server --command='docker logs -f backend' --tab -T SrvLogs --command='tail -f /home/jkleinerman/Repos/dobie/server/back_end/logevents.log' --tab -T SrvDB --command='mysql -u dobie_usr -pqwe123qwe -h 172.18.0.2 dobie_db' --tab -T Ctrllr1Execution --command='ssh jkleinerman@10.10.7.75 -t "cd ConPass/controller/py_src; bash --login"' --tab -T Ctrllr1Logs --command='ssh jkleinerman@10.10.7.75 -t "cd ConPass/controller/py_src; tail -f logevents.log; bash --login"' --tab -T Ctrllr1DB --command='ssh jkleinerman@10.10.7.75 -t "cd ConPass/controller/py_src; sqlite3 access.db; bash --login"' --tab -T Ctrllr2Execution --command='ssh jkleinerman@10.10.7.73 -t "cd ConPass/controller/py_src; bash --login"' --tab -T Ctrllr2Logs --command='ssh jkleinerman@10.10.7.73 -t "cd ConPass/controller/py_src; tail -f logevents.log; bash --login"' --tab -T Ctrllr2DB --command='ssh jkleinerman@10.10.7.73 -t "cd ConPass/controller/py_src; sqlite3 access.db; bash --login"' --tab -T Local
