import os
import sys
import cx_Oracle

connection = cx_Oracle.Connection(mode = cx_Oracle.SYSDBA)
cursor = connection.cursor()
cursor.arraysize = 100

try:
    cursor.execute("SELECT UPPER(HOST_NAME), INSTANCE_NAME, NAME, LOG_MODE, OPEN_MODE, DATABASE_ROLE, TO_CHAR(CREATED,'DD-MON-YYYY HH24:MI'), TO_CHAR(STARTUP_TIME,'DD-MON-YYYY HH24:MI'), RTRIM(LTRIM( (CAST(SYSDATE AS TIMESTAMP) - CAST (STARTUP_TIME AS TIMESTAMP)),'+000000000'),'.000000'), TO_CHAR(SYSDATE, 'DD-MON-YYYY HH24:MI') FROM V$DATABASE,V$INSTANCE")

except cx_Oracle.DatabaseError, exc:
    print >> sys.stderr, 'Oracle Error Message : ' + str(exc)
    exit(1)

output = cursor.fetchall()
oracle_sid = os.environ['ORACLE_SID']
value = output[0]

print ('=========================================================')
print ('                      ' + oracle_sid)
print ('=========================================================')
print ('Host Name                  : ' + value[0])
print ('Oracle Database Version    : ' + connection.version)
print ('Instance Name              : ' + value[1])
print ('Database Name              : ' + value[2])
print ('Database Log Mode          : ' + value[3])
print ('Database Mode              : ' + value[4])
print ('Database Role              : ' + value[5])
print ('Database Created Time      : ' + value[6])
print ('Database Last Restart Time : ' + value[7])
print ('Database Uptime Time       : ' + value[8])
print ('Current Time               : ' + value[9])
print ('=========================================================')
print

cursor.close()
connection.close()

exit(0)
