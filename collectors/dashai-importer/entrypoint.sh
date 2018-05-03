trap "exit" TERM
tail -f /dev/null &
wait
