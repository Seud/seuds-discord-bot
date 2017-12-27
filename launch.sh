<<<<<<< HEAD
=======
CRONFILE='/etc/cron.d/seud-discord'
>>>>>>> d0f8a875591f77f9c18f7067e1a25c1e89c6d249
PROGNAME="Seud's Discord Bot"
PIDFILE='/home/bot/discord/discord.pid'
LOGFILE='/home/bot/discord/log/main.log'

function s_date {
  date +"[%b %d %H:%M:%S]"
}

function s_fatal {
  echo "ERROR - $*" 1>&2
  exit 1
}

function s_debug {
  if [[ $DEBUG ]]
  then
    echo "DEBUG - $*" 1>&2
  fi
}

function s_usage {
  cat  <<EOU
NAME
  $PROGNAME
DESCRIPTION
  This script manages $PROGNAME, which is a Discord bot
SYNOPSIS    
  $I [OPTION] COMMANDS
OPTIONS
  -v                    : Activate verbose mode
  -q                    : Activate quiet mode (Useful for cron)
  --help / -h           : Show this description
COMMANDS
  status
    Show status of the bot
  start
    Start the bot
  stop
    Stop the bot
  restart
    Restart the bot
EOU
    exit $1
}

function s_status {
  local SPID
  
  if [[ -f $PIDFILE ]]
  then
    SPID=$(cat $PIDFILE)
    s_debug "PID : $SPID"
    if [[ $SPID ]]
    then
      ps "$SPID" | grep -E "($I|main.py)" > /dev/null || SPID=
    fi
  else
    SPID=
  fi
  
  [[ $SPID ]]
}

function s_start {
  if ! s_status
  then
    
    echo "Starting $PROGNAME"
    echo "" > $PIDFILE
    l_bot
    
    PID=$!
    s_debug "SUPPOSED PID : $PID"
    echo $PID > $PIDFILE
    
    # Check if daemon started correctly
    if s_status
    then
      echo "$PROGNAME started"
    else
      s_clean &> /dev/null
      s_fatal "$PROGNAME failed to start ! "
    fi
    
  else
    s_debug "$PROGNAME already running !"
    return 1
  fi
}

function s_stop {
  if ! s_status
  then
    s_debug "$PROGNAME not started !"
    return 1
  else
    echo "Stopping $PROGNAME"
  fi

  s_clean &> /dev/null
}

function s_clean {
  if [[ -f $PIDFILE ]]
  then
    PID=$(cat $PIDFILE)
    kill $PID
  fi
}

function l_bot {
  BOT_TOKEN=$(cat token)
  export BOT_TOKEN
  
  # TODO Terrible rotation, improve
  if [[ -f $LOGFILE ]]
  then
    cat "$LOGFILE" >> "$LOGFILE.old"
    echo "" > "$LOGFILE"
  fi
  ./main.py $OPTS &
}

# ---------- Script Start ----------

DEBUG=
OPTS=
I=${0##*/}

if [[ $1 == '-v' ]]
then
  OPTS='-v'
  DEBUG='-v'
  shift
elif [[ $1 == '-q' ]]
then
  OPTS='-q'
  shift
fi

# Checking command
case "$1" in
  '--help')   s_usage 0          ;;
  '-h')       s_usage 0          ;;
  'usage')    s_usage 0          ;;
  'status')   s_status; exit $?  ;;
  'start')    s_start            ;;
  'restart')  s_stop; s_start    ;;
  'stop')     s_stop             ;;
  *)
    echo "Invalid command !"
    s_usage 2
  ;;
esac