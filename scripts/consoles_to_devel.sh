#!/bin/bash

DB_DOCKER_IP=$(tr -d '", ' <<< $(docker inspect database | grep '"IPAddress": "1' | gawk '{print $2}'))

CTRLLR_H_1=192.168.1.97
CTRLLR_H_2=192.168.1.98
CTRLLR_H_3=192.168.1.99

CTRLLR_W_1=10.10.7.97
CTRLLR_W_2=10.10.7.98
CTRLLR_W_3=10.10.7.99

PATH_SRVR=/home/jkleinerman/Repos/dobie
PATH_CTRLLR=/opt/dobie
USER_CTRLLER=root


function consoles_to_devel_home {

xfce4-terminal --tab -T S_Stdout --command="docker logs -f backend" --tab -T S_Logs --command="tail -f $PATH_SRVR/server/back_end/logevents.log" --tab -T S_DB --command="mysql -u dobie_usr -pqwe123qwe -h $DB_DOCKER_IP dobie_db" --tab -T 1_C_Exec --command="ssh $USER_CTRLLER@$CTRLLR_H_1 -t 'cd $PATH_CTRLLR/controller/py_src; bash --login'" --tab -T 1_C_Logs --command="ssh $USER_CTRLLER@$CTRLLR_H_1 -t 'cd $PATH_CTRLLR/controller/py_src; tail -f logevents.log; bash --login'" --tab -T 1_C_DB --command="ssh $USER_CTRLLER@$CTRLLR_H_1 -t 'cd $PATH_CTRLLR/controller/py_src; sqlite3 access.db; bash --login'" --tab -T 2_C_Exec --command="ssh $USER_CTRLLER@$CTRLLR_H_2 -t 'cd $PATH_CTRLLR/controller/py_src; bash --login'" --tab -T 2_C_Logs --command="ssh $USER_CTRLLER@$CTRLLR_H_2 -t 'cd $PATH_CTRLLR/controller/py_src; tail -f logevents.log; bash --login'" --tab -T 2_C_DB --command="ssh $USER_CTRLLER@$CTRLLR_H_2 -t 'cd $PATH_CTRLLR/controller/py_src; sqlite3 access.db; bash --login'" --tab -T 3_C_Exec --command="ssh $USER_CTRLLER@$CTRLLR_H_3 -t 'cd $PATH_CTRLLR/controller/py_src; bash --login'" --tab -T 3_C_Logs --command="ssh $USER_CTRLLER@$CTRLLR_H_3 -t 'cd $PATH_CTRLLR/controller/py_src; tail -f logevents.log; bash --login'" --tab -T 3_C_DB --command="ssh $USER_CTRLLER@$CTRLLR_H_3 -t 'cd $PATH_CTRLLR/controller/py_src; sqlite3 access.db; bash --login'"


}


function consoles_to_devel_work {

xfce4-terminal --tab -T S_Stdout --command="docker logs -f backend" --tab -T S_Logs --command="tail -f $PATH_SRVR/server/back_end/logevents.log" --tab -T S_DB --command="mysql -u dobie_usr -pqwe123qwe -h $DB_DOCKER_IP dobie_db" --tab -T 1_C_Exec --command="ssh $USER_CTRLLER@$CTRLLR_W_1 -t 'cd $PATH_CTRLLR/controller/py_src; bash --login'" --tab -T 1_C_Logs --command="ssh $USER_CTRLLER@$CTRLLR_W_1 -t 'cd $PATH_CTRLLR/controller/py_src; tail -f logevents.log; bash --login'" --tab -T 1_C_DB --command="ssh $USER_CTRLLER@$CTRLLR_W_1 -t 'cd $PATH_CTRLLR/controller/py_src; sqlite3 access.db; bash --login'" --tab -T 2_C_Exec --command="ssh $USER_CTRLLER@$CTRLLR_W_2 -t 'cd $PATH_CTRLLR/controller/py_src; bash --login'" --tab -T 2_C_Logs --command="ssh $USER_CTRLLER@$CTRLLR_W_2 -t 'cd $PATH_CTRLLR/controller/py_src; tail -f logevents.log; bash --login'" --tab -T 2_C_DB --command="ssh $USER_CTRLLER@$CTRLLR_W_2 -t 'cd $PATH_CTRLLR/controller/py_src; sqlite3 access.db; bash --login'" --tab -T 3_C_Exec --command="ssh $USER_CTRLLER@$CTRLLR_W_3 -t 'cd $PATH_CTRLLR/controller/py_src; bash --login'" --tab -T 3_C_Logs --command="ssh $USER_CTRLLER@$CTRLLR_W_3 -t 'cd $PATH_CTRLLR/controller/py_src; tail -f logevents.log; bash --login'" --tab -T 3_C_DB --command="ssh $USER_CTRLLER@$CTRLLR_W_3 -t 'cd $PATH_CTRLLR/controller/py_src; sqlite3 access.db; bash --login'"

}




case "$1" in
    -h)
    consoles_to_devel_home
    ;;
    -w)
    consoles_to_devel_work
    ;;
  *)
    echo "Usage: $0 {-h|-w}"
    exit 1
    ;;
esac

exit 0

