# ----------------------------------------------------------------------
# Run the tnsnames_checker Java code to validate a file passed on stdin
# or as a parameter.
# ----------------------------------------------------------------------
# For example, errors to the screen:
#
# 	tnsnames_checker < standard.tnsnames.ora 
# or
# 	tnsnames_checker standard.tnsnames.ora 
# ----------------------------------------------------------------------
# Informational messages are sent to stdout while errors go to stderr.
# Redirecting error messages to a file:
#
# 	tnsnames_checker standard.tnsnames.ora 2>errors.log
# ----------------------------------------------------------------------
# Redirect all output to the same file:
#
# 	tnsnames_checker standard.tnsnames.ora >errors.log 2>&1
# ----------------------------------------------------------------------
# Have fun. (But  that's not mandatory!)
# Norman Dunbar, August 2014.
# ----------------------------------------------------------------------


/usr/local/jython/bin/jython -Dpython.path=/Users/philipkrauss/Tnsnames_checker/tnsnames_checker-0.4/Tnsnames_checker-master/tnsnames_checker.jar:/usr/local/lib/antlr-4.7-complete.jar  tnsnames_checker.py $*
