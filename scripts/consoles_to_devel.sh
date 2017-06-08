#!/bin/bash





function consoles_to_devel_home {

xfce4-terminal --tab -T STDOUT-Server --tab -T SrvLogs --command='tail -f /home/jkleinerman/Repos/dobie/server/back_end/logevents.log' --tab -T SrvDB --command='mysql -u dobie_usr -pqwe123qwe -h 172.18.0.2 dobie_db' --tab -T Ctrllr1Execution --command='ssh jkleinerman@192.168.1.75 -t "cd dobie/controller/py_src; bash --login"' --tab -T Ctrllr1Logs --command='ssh jkleinerman@192.168.1.75 -t "cd dobie/controller/py_src; tail -f logevents.log; bash --login"' --tab -T Ctrllr1DB --command='ssh jkleinerman@192.168.1.75 -t "cd dobie/controller/py_src; sqlite3 access.db; bash --login"' --tab -T Ctrllr2Execution --command='ssh jkleinerman@192.168.1.73 -t "cd dobie/controller/py_src; bash --login"' --tab -T Ctrllr2Logs --command='ssh jkleinerman@192.168.1.73 -t "cd dobie/controller/py_src; tail -f logevents.log; bash --login"' --tab -T Ctrllr2DB --command='ssh jkleinerman@192.168.1.73 -t "cd dobie/controller/py_src; sqlite3 access.db; bash --login"'


}


function consoles_to_devel_work {

xfce4-terminal --tab -T STDOUT-Server --tab -T SrvLogs --command='tail -f /home/jkleinerman/Repos/dobie/server/back_end/logevents.log' --tab -T SrvDB --command='mysql -u dobie_usr -pqwe123qwe -h 172.18.0.2 dobie_db' --tab -T Ctrllr1Execution --command='ssh jkleinerman@10.10.7.75 -t "cd dobie/controller/py_src; bash --login"' --tab -T Ctrllr1Logs --command='ssh jkleinerman@10.10.7.75 -t "cd dobie/controller/py_src; tail -f logevents.log; bash --login"' --tab -T Ctrllr1DB --command='ssh jkleinerman@10.10.7.75 -t "cd dobie/controller/py_src; sqlite3 access.db; bash --login"' --tab -T Ctrllr2Execution --command='ssh jkleinerman@10.10.7.73 -t "cd dobie/controller/py_src; bash --login"' --tab -T Ctrllr2Logs --command='ssh jkleinerman@10.10.7.73 -t "cd dobie/controller/py_src; tail -f logevents.log; bash --login"' --tab -T Ctrllr2DB --command='ssh jkleinerman@10.10.7.73 -t "cd dobie/controller/py_src; sqlite3 access.db; bash --login"' 


}




case "$1" in
    -h)
    consoles_to_devel_home
    ;;
    -w)
    consoles_to_devel_work
    ;;
  *)
    echo "consoles_to_devel: $0 {-h|-w}"
    exit 1
    ;;
esac

exit 0

