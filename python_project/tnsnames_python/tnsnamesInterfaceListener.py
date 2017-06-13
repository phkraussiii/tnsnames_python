#!/usr/local/jython/bin/jython

# Import some python stuff
import fileinput
import pprint
import sys

# Import ANTLR's runtime libraries
from tnsnamesParserListener import tnsnamesParserListener
import antlr4
from LineNumber import LineNumber

class tnsnamesInterfaceListener(tnsnamesParserListener):

    global aliasNames
    aliasNames = []
    global aliasCount
    aliasCount = 0
    global duplicateNames
    duplicateNames = []
    global duplicateCount
    duplicateCount = 0

    global thisInfo
    thisInfo = 0
    global thisWarnings
    thisWarnings = 0
    global thisErrors
    thisErrors = 0
    global totalInfo
    totalInfo = 0
    global totalWarnings
    totalWarnings = 0
    global totalErrors
    totalErrors = 0
    global totalDuplicates
    totalDuplicates = 0

    # The following are all to be found in the DESCRIPTION.
    global firstSduLine
    firstSduLine = LineNumber(0)                # SDU.
    global firstLoadBalanceLine
    firstLoadBalanceLine = LineNumber(0)        # LOAD_BALANCE.
    global firstEnableLine
    firstEnableLine = LineNumber(0)             # ENABLE.
    global firstFailOverLine
    firstFailOverLine = LineNumber(0)           # FAILOVER.
    global firstRecvBufLine
    firstRecvBufLine = LineNumber(0)            # RECV_BUF_SIZE
    global firstSendBufLine
    firstSendBufLine = LineNumber(0)            # SEND_BUF_SIZE
    global firstSourceRouteLine
    firstSourceRouteLine = LineNumber(0)        # SOURCE_ROUTE
    global firstServiceTypeLine
    firstServiceTypeLine = LineNumber(0)        # SERVICE_TYPE
    global firstSecurityLine
    firstSecurityLine = LineNumber(0)           # SECURITY
    global firstConnTimeoutLine
    firstConnTimeoutLine = LineNumber(0)        # CONN_TIMEOUT
    global firstRetryCountLine
    firstRetryCountLine = LineNumber(0)         # RETRY_COUNT
    global firstTctLine
    firstTctLine = LineNumber(0)                # TCT

    # The following are all DESCRIPTION_LIST parameters.
    global firstDL_LoadBalanceLine
    firstDL_LoadBalanceLine = LineNumber(0)     # LOAD_BALANCE.
    global firstDL_FailOverLine
    firstDL_FailOverLine = LineNumber(0)        # FAILOVER.
    global firstDL_SourceRouteLine
    firstDL_SourceRouteLine = LineNumber(0)     # SOURCE_ROUTE.

    # The following are all ADDRESS_LIST parameters.
    global firstAL_LoadBalanceLine
    firstAL_LoadBalanceLine = LineNumber(0)	# LOAD_BALANCE.
    global firstAL_FailOverLine
    firstAL_FailOverLine = LineNumber(0)	# FAILOVER.
    global firstAL_SourceRouteLine
    firstAL_SourceRouteLine = LineNumber(0)	# SOURCE_ROUTE.

    # The following are all ADDRESS parameters.
    global firstA_RecvBufLine
    firstA_RecvBufLine = LineNumber(0)          # RECV_BUF_SIZE.
    global firstA_SendBufLine
    firstA_SendBufLine = LineNumber(0)          # SEND_BUF_SIZE.

    # The following are all CONNECT_DATA parameters.
    global firstCD_ServiceNameLine 
    firstCD_ServiceNameLine = LineNumber(0)     # SERVICE_NAME.
    global firstCD_SidLine
    firstCD_SidLine = LineNumber(0)             # SID.
    global firstCD_InstanceNameLine
    firstCD_InstanceNameLine = LineNumber(0)    # INSTANCE_NAME.
    global firstCD_FailoverModeLine
    firstCD_FailoverModeLine = LineNumber(0)    # FAILOVER_MODE.
    global firstCD_GlobalNameLine
    firstCD_GlobalNameLine = LineNumber(0)      # GLOBAL_NAME.
    global firstCD_HsLine
    firstCD_HsLine = LineNumber(0)              # HS.
    global firstCD_RdbDatabaseLine
    firstCD_RdbDatabaseLine = LineNumber(0)     # RDB_DATABASE.
    global firstCD_ServerLine
    firstCD_ServerLine = LineNumber(0)          # SERVER.
    global firstCD_UrLine
    firstCD_UrLine = LineNumber(0)              # UR.

    # These are for TCP Protocol.
    global firstTCP_HostLine
    firstTCP_HostLine = LineNumber(0)           # HOST
    global firstTCP_PortLine
    firstTCP_PortLine = LineNumber(0)           # PORT
    global firstTCP_ProtocolLine
    firstTCP_ProtocolLine = LineNumber(0)       # PROTOCOL

    # These are for IPC Protocol.
    global firstIPC_KeyLine
    firstIPC_KeyLine = LineNumber(0)            # KEY
    global firstIPC_ProtocolLine
    firstIPC_ProtocolLine = LineNumber(0)       # PROTOCOL

    # These are for SPX Protocol.
    global firstSPX_ServiceLine
    firstSPX_ServiceLine = LineNumber(0)        # SERVICE
    global firstSPX_ProtocolLine
    firstSPX_ProtocolLine = LineNumber(0)       # PROTOCOL

    # These are for NMP Protocol
    global firstNMP_PipeLine
    firstNMP_PipeLine = LineNumber(0)           # PIPE
    global firstNMP_ServerLine
    firstNMP_ServerLine = LineNumber(0)         # SERVER
    global firstNMP_ProtocolLine
    firstNMP_ProtocolLine = LineNumber(0)       # PROTOCOL

    # These are for BEQ Protocol
    global firstBEQ_ProgramLine
    firstBEQ_ProgramLine = LineNumber(0)        # PROGRAM
    global firstBEQ_ProtocolLine
    firstBEQ_ProtocolLine = LineNumber(0)       # PROTOCOL
    global firstBEQ_Argv0Line
    firstBEQ_Argv0Line = LineNumber(0)          # ARGV0 (ARGV<zero>)
    global firstBEQ_ArgsLine
    firstBEQ_ArgsLine = LineNumber(0)           # ARGS

    # These are from BEQ Args.
    global firstBAD_AddressLine
    firstBAD_AddressLine = LineNumber(0)        # ADDRESS
    global firstBAD_LocalLine
    firstBAD_LocalLine = LineNumber(0)          # LOCAL
    global firstBAD_ProtocolLine
    firstBAD_ProtocolLine = LineNumber(0)       # PROTOCOL

    # These are for the FAILOVER_MODE in CONNECT_DATA.
    global firstFOM_BackupLine
    firstFOM_BackupLine = LineNumber(0)         # BACKUP
    global firstFOM_TypeLine
    firstFOM_TypeLine = LineNumber(0)           # TYPE
    global firstFOM_MethodLine
    firstFOM_MethodLine = LineNumber(0)         # METHOD
    global firstFOM_RetriesLine
    firstFOM_RetriesLine = LineNumber(0)        # RETRIES
    global firstFOM_DelayLine
    firstFOM_DelayLine = LineNumber(0)          # DELAY

    #----------------------------------------------------------------
    # CONSTRUCTOR
    #----------------------------------------------------------------
    # We use the parser, because we need the rule names later when we
    # are checking for parameter redefinition of the parameters that
    # apply to DESCRIPTION_LIST, DESCRIPTION and ADDRESS_LIST.
    #----------------------------------------------------------------
    def __init__(self,parser):
        self.parser = parser
        #print(parser.__dict__)
        self.ruleNames = parser.ruleNames

    #----------------------------------------------------------------
    # Write an INFO to stderr and increment the information counters.
    #----------------------------------------------------------------
    def doInfo(self, message, ctx):
	global totalInfo
	global thisInfo
        print(self.whereAmI + str(self.whereAmIlin) + ':' + str(self.whereAmIcol) + " INFO: " + message)
	totalInfo += 1
	thisInfo += 1

    #----------------------------------------------------------------
    # Write an WARNING to stderr and increment the warning counters.
    #----------------------------------------------------------------
    def doWarning(self, message, ctx):
        global totalWarnings
	global thisWarnings
	print(self.whereAmI + str(self.whereAmIlin) + ':' + str(self.whereAmIcol) + " WARNING: " + message)
        totalWarnings += 1
        thisWarnings += 1

    #----------------------------------------------------------------
    # Write an ERROR to stderr and increment the total error counters.
    #----------------------------------------------------------------
    def doError(self, message, ctx):
	global totalErrors
	global thisErrors
        print(self.whereAmI + str(self.whereAmIlin) + ':' + str(self.whereAmIcol) + " ERROR: " + message)
        totalErrors += 1
        thisErrors += 1

    #----------------------------------------------------------------
    # Error Logger for parameter redefinitions
    #----------------------------------------------------------------
    # This function simply prints a warning message to stderr when
    # we find a parameter has been redefined at some point.
    #----------------------------------------------------------------
    def tnsRedefined(self, tnsSectionName, firstLineNumber):
	# print(ctx.__dict__)
	# print(tnsSectionName)
	# print(firstLineNumber)
        self.doWarning(tnsSectionName + " parameter redefines " + tnsSectionName + " parameter at line " + str(firstLineNumber) + ".", self)

    #------------------------------------------------------------------
    # Check for parameter redefinitions
    #------------------------------------------------------------------
    # This function checks to see if the passed LineNumber has been
    # redefined by the current lineNumber. If so, prints a warning
    # message and saves the current lineNumber.
    #------------------------------------------------------------------
    # First time we hit a specific parameter, previous will be zero
    # so we save the current line number as the previous one. All
    # other passes through will be redefinitions and result in warnings.
    #------------------------------------------------------------------
    # And don;t talk to me about Java's inability to properly pass by
    # reference. Having to wrap an int in a class, with a getter and
    # setter just to be able to swap two ints in a function, is a joke.
    #------------------------------------------------------------------
    def checkForRedefinition(self, message, previous, current, ctx):
        #print(current)
	#print(previous)
	#print(self.whereAmI)
	if previous.value != 0:
	
            # Not the first time we've seen this parameter, so
            # warn the user about a redefinition.
            self.tnsRedefined(message, previous.value)
	    # print('tnsRedefined')
        else:
            # First time we've seen this parameter, so save the
            # current line number.
            previous.value = current
	    # print('previous = current')

    #----------------------------------------------------------------
    # EVERY RULE
    #----------------------------------------------------------------
    # As we enter every rule, extract the line and column positions.
    # Use them to build a location string for the start of this rule.
    #----------------------------------------------------------------
    def enterEveryRule(self, ctx):
	startToken = ctx.start
	# test print
	# print(startToken.__dict__)
        if startToken != None:
            # Lines number from 1.
	    # old self.lineNumber = startToken.getLine()
            self.lineNumber = startToken.line

            # Characters from zero. Adjust.
            self.charPosition = 1 + startToken.column
        else:
            # Just in case Token can ever be null.
            self.lineNumber = 0
            self.charPosition = 0

        # Build a location string for error messages etc.
	# old self.whereAmI = 'Line:'  + str(self.lineNumber) + ':' + str(self.charPosition)
        self.whereAmI = 'Line: '
	self.whereAmIlin = self.lineNumber
	self.whereAmIcol = self.charPosition
	# test print
	# print(self.whereAmI + str(self.whereAmIlin) + ':' + str(self.whereAmIcol))

    #----------------------------------------------------------------
    # LISTENER ENTRY
    #----------------------------------------------------------------
    # We have found a listener style tns_entry.
    #----------------------------------------------------------------
    def enterLsnr_entry(self, ctx):
	
	global duplicateCount
        global duplicateNames
        global aliasNames
        global aliasCount
	global thisInfo
	global thisWarnings
	global thisErrors

	# old thisAlias = ctx.alias().getText()
	thisAlias = ctx.alias().getText()
	
	# old System.err.println("\n" + whereAmI.substring(1) + " Listener alias found: " + thisAlias);
	print(self.whereAmI + str(self.whereAmIlin) + ':' + str(self.whereAmIcol) + " Listener alias found: " + thisAlias)
        thisInfo = 0
        thisWarnings = 0
        thisErrors = 0
        # Has this alias been seen before in this file
	for p in range (0, aliasCount):
		if (aliasNames[p] == thisAlias):
			self.doError("Duplicate alias - " + thisAlias, ctx)
                        duplicateNames.append(thisAlias)
                        duplicateCount += 1
			break
		else:
			pass

	# New alias, add it to the list of found aliases.
	# old aliasNames.add(ctx.alias().getText())
	aliasNames.append(thisAlias)
	aliasCount += 1

    #----------------------------------------------------------------
    # LISTENER EXIT
    #----------------------------------------------------------------
    def exitLsnr_entry(self, ctx):
	
	global thisInfo
        global thisWarnings
        global thisErrors
	print("*** INFO: " + str(thisInfo) + ", WARNING: " + str(thisWarnings) + ", ERRORS: " + str(thisErrors))

    #----------------------------------------------------------------
    # TNS ENTRY
    #----------------------------------------------------------------
    # We have found a proper database style tns_entry.
    #----------------------------------------------------------------
    def enterTns_entry(self, ctx):

	global duplicateCount
        global duplicateNames
	global aliasNames
        global aliasCount
	global thisInfo
	global thisWarnings
	global thisErrors

        thisAlias = ctx.alias_list().getText()
        # old print("\n" + whereAmI.substring(1) + " Database alias found: " + thisAlias)
        print(self.whereAmI + str(self.whereAmIlin) + ':' + str(self.whereAmIcol) + " Database alias found: " + thisAlias)

        # Initialise the counters for this tns alias.
        thisInfo = 0
        thisWarnings = 0
        thisErrors = 0
        # Add each alias to the found aliases list, if it hasn't already been added.	
	# old for i, val in enumerate(ctx.alias_list().alias()):	
	for i in range(0, len(ctx.alias_list().alias())):
	    thisAlias1 = ctx.alias_list().alias(i).getText()
            # Has this alias been seen before in this file
	    for e, ele in enumerate(aliasNames):
	    	if (aliasNames[e] == thisAlias1):
                	self.doError("Duplicate alias - " + thisAlias1, ctx)
                	duplicateNames.append(thisAlias1)
                	duplicateCount += 1
			break
           	else:
			pass
            aliasNames.append(thisAlias1)
            aliasCount += 1
	
    #----------------------------------------------------------------
    # TNS EXIT
    #----------------------------------------------------------------
    def exitTns_entry(self, ctx):
	
	global thisInfo
        global thisWarnings
        global thisErrors
        print("*** INFO: " + str(thisInfo) + ", WARNING: " + str(thisWarnings) + ", ERRORS: " + str(thisErrors))

    #----------------------------------------------------------------
    # DESCRIPTION_LIST ENTRY
    #----------------------------------------------------------------
    def enterDescription_list(self, ctx):
        # Zeroise the first line counters for the parameters applicable
        # to a DESCRIPTION_LIST entry.
        firstDL_LoadBalanceLine.setValue(0)        # LOAD_BALANCE
        firstDL_FailOverLine.setValue(0)           # FAILOVER
        firstDL_SourceRouteLine.setValue(0)        # SOURCE_ROUTE

    #----------------------------------------------------------------
    # DESCRIPTION ENTRY
    #----------------------------------------------------------------
    def enterDescription(self, ctx):
        # Zeroise the first line counters for the parameters applicable
        # to a DESCRIPTION entry.
        firstSduLine.setValue(0)                   # SDU
        firstLoadBalanceLine.setValue(0)           # LOAD_BALANCE
        firstEnableLine.setValue(0)                # ENABLE
        firstFailOverLine.setValue(0)              # FAILOVER
        firstRecvBufLine.setValue(0)               # RECV_BUF_SIZE
        firstSendBufLine.setValue(0)               # SEND_BUF_SIZE
        firstSourceRouteLine.setValue(0)           # ROUTE
        firstServiceTypeLine.setValue(0)           # SERVICE_TYPE
        firstSecurityLine.setValue(0)              # SECURITY
        firstConnTimeoutLine.setValue(0)           # CONN_TIMEOUT
        firstRetryCountLine.setValue(0)            # RETRY_COUNT
        firstTctLine.setValue(0)                   # TCT

        # Multiple ADDRESSes without an ADDRESS_LIST?
        # test print
	# print(ctx.__dict__)
	addressCount = len(ctx.address())

        if (ctx.address_list() == None and addressCount > 1):
            # We might have a problem, but Oracle allows this form anyway.
            self.doWarning("Missing ADDRESS_LIST, " + str(addressCount) + " ADDRESS entries found.", ctx)

        # Missing CONNECT_DATA?
        if (ctx.connect_data() == None):
            self.doError("Missing CONNECT_DATA.", ctx)

    #----------------------------------------------------------------
    # ADDRESS_LIST ENTRY
    #----------------------------------------------------------------
    def enterAddress_list(self, ctx):
        # Zeroise the first line counters for the parameters applicable
        # to a ADDRESS_LIST entry.
        firstA_RecvBufLine.setValue(0)             # RECV_BUF_SIZE
        firstA_SendBufLine.setValue(0)             # SEND_BUF_SIZE

    #----------------------------------------------------------------
    # ADDRESS ENTRY
    #----------------------------------------------------------------
    def enterAddress(self, ctx):

        # Zeroise the first line counters for the parameters applicable
        # to a ADDRESS entry.
        firstAL_LoadBalanceLine.setValue(0)        # Address List
        firstAL_FailOverLine.setValue(0)
        firstAL_SourceRouteLine.setValue(0)
        firstTCP_HostLine.setValue(0)              # TCP
        firstTCP_PortLine.setValue(0)
        firstTCP_ProtocolLine.setValue(0)
        firstIPC_KeyLine.setValue(0)               # IPC
        firstIPC_ProtocolLine.setValue(0)
        firstSPX_ServiceLine.setValue(0)           # SPX
        firstSPX_ProtocolLine.setValue(0)
        firstNMP_ServerLine.setValue(0)            # NMP
        firstNMP_PipeLine.setValue(0)
        firstNMP_ProtocolLine.setValue(0)
        firstBEQ_ProgramLine.setValue(0)           # BEQ
        firstBEQ_ProtocolLine.setValue(0)
        firstBEQ_Argv0Line.setValue(0)
        firstBEQ_ArgsLine.setValue(0)
    
    #----------------------------------------------------------------
    # CONNECT_DATA ENTRY
    #----------------------------------------------------------------
    def enterConnect_data(self, ctx):
    
        # Zeroise the first line counters for the parameters applicable
        # to a CONNECT_DATA entry.
        firstCD_ServiceNameLine.setValue(0)        # SERVICE_NAME
        firstCD_SidLine.setValue(0)                # SID
        firstCD_InstanceNameLine.setValue(0)       # INSTANCE_NAME
        firstCD_FailoverModeLine.setValue(0)       # FAILOVER_MODE
        firstCD_GlobalNameLine.setValue(0)         # GLOBAL_NAME
        firstCD_HsLine.setValue(0)                 # HS
        firstCD_RdbDatabaseLine.setValue(0)        # RDB_DATABASE
        firstCD_ServerLine.setValue(0)             # SERVER
        firstCD_UrLine.setValue(0)                 # UR
    
    #----------------------------------------------------------------
    # BA_DESCRIPTION ENTRY
    #----------------------------------------------------------------
    def enterBa_description(self, ctx):
    
        # Zeroise the first line counters for the parameters applicable
        # to a BEQ ARGS DESCRIPTION entry.
        firstBAD_AddressLine.setValue(0)           # ADDRESS
        firstBAD_LocalLine.setValue(0)             # LOCAL
        firstBAD_ProtocolLine.setValue(0)          # PROTOCOL
    
    #----------------------------------------------------------------
    # SERVICE_NAME ENTRY
    #----------------------------------------------------------------
    # Check only for parameter redefinition.
    #----------------------------------------------------------------
    def enterCd_service_name(self, ctx):
    
        self.checkForRedefinition("SERVICE_NAME", firstCD_ServiceNameLine, self.lineNumber, ctx)

    #----------------------------------------------------------------
    # SID ENTRY
    #----------------------------------------------------------------
    # Check only for parameter redefinition.
    #----------------------------------------------------------------
    def enterCd_sid(self, ctx):
	# print(firstCD_SidLine.value)
	# print(self.lineNumber)
	# print('enterCd_sid called')
        self.checkForRedefinition("SID", firstCD_SidLine, self.lineNumber, ctx)
    

    #----------------------------------------------------------------
    # INSTANCE_NAME ENTRY
    #----------------------------------------------------------------
    # Check only for parameter redefinition.
    #----------------------------------------------------------------
    def enterCd_instance_name(self, ctx):
    
        self.checkForRedefinition("INSTANCE_NAME", firstCD_InstanceNameLine, self.lineNumber, ctx)
    
    #----------------------------------------------------------------
    # FAILOVER_MODE ENTRY
    #----------------------------------------------------------------
    # Check only for parameter redefinition. There will be checks
    # later on for the individual parts of a FAILOVER_MODE.
    #----------------------------------------------------------------
    def enterCd_failover_mode(self, ctx):
    
        self.checkForRedefinition("FAILOVER_MODE", firstCD_FailoverModeLine, self.lineNumber, ctx)

        # Reset the line numbers for the various FAILOVER_MODE parameters.
        firstFOM_BackupLine.setValue(0)
        firstFOM_TypeLine.setValue(0)
        firstFOM_MethodLine.setValue(0)
        firstFOM_RetriesLine.setValue(0)
        firstFOM_DelayLine.setValue(0)

    #----------------------------------------------------------------
    # FOM BACKUP ENTRY
    #----------------------------------------------------------------
    # Check only for parameter redefinition.
    #----------------------------------------------------------------
    def enterFo_backup(self, ctx):
    
        self.checkForRedefinition("BACKUP", firstFOM_BackupLine, self.lineNumber, ctx)
    
    #----------------------------------------------------------------
    # FOM TYPE ENTRY
    #----------------------------------------------------------------
    # Check only for parameter redefinition.
    #----------------------------------------------------------------
    def enterFo_type(self, ctx):
    
        self.checkForRedefinition("TYPE", firstFOM_TypeLine, self.lineNumber, ctx)

    #----------------------------------------------------------------
    # FOM METHOD ENTRY
    #----------------------------------------------------------------
    # Check only for parameter redefinition.
    #----------------------------------------------------------------
    def enterFo_method(self, ctx):
    
        self.checkForRedefinition("METHOD", firstFOM_MethodLine, self.lineNumber, ctx)
    
    #----------------------------------------------------------------
    # FOM RETRIES ENTRY
    #----------------------------------------------------------------
    # Check only for parameter redefinition.
    #----------------------------------------------------------------
    def enterFo_retries(self, ctx):
    
        self.checkForRedefinition("RETRIES", firstFOM_RetriesLine, self.lineNumber, ctx)

    #----------------------------------------------------------------
    # FOM DELAY ENTRY
    #----------------------------------------------------------------
    # Check only for parameter redefinition.
    #----------------------------------------------------------------
    def enterFo_delay(self, ctx):
    
        self.checkForRedefinition("DELAY", firstFOM_DelayLine, self.lineNumber, ctx)
    
    #----------------------------------------------------------------
    # GLOBAL_NAME ENTRY
    #----------------------------------------------------------------
    # Check only for parameter redefinition.
    #----------------------------------------------------------------
    def enterCd_global_name(self, ctx):
    
        self.checkForRedefinition("GLOBAL_NAME", firstCD_GlobalNameLine, self.lineNumber, ctx)

    #----------------------------------------------------------------
    # HS ENTRY
    #----------------------------------------------------------------
    # Check only for parameter redefinition.
    #----------------------------------------------------------------
    def enterCd_hs(self, ctx):
    
        self.checkForRedefinition("HS", firstCD_HsLine, self.lineNumber, ctx)
    
    # THIS IS NOT THE NEXT FUNCTION THERE IS MORE ENTRY FUNCTIONS NEEDSED BEFORE THIS
    #----------------------------------------------------------------
    # PORT (number)
    #----------------------------------------------------------------
    # Check the port numbers are 1024 <= n <= 65535
    #----------------------------------------------------------------
    def enterPort(self, ctx):
        
        # old portNumber = Integer.parseInt(ctx.INT().getText())
        portNumber = int(ctx.INT().getText())
	# test print
	#print(portNumber)

        # Below 1024 is suspicious. Requires root privileges to open.
        if (portNumber < 1024):
            self.doWarning("Port number, " + str(portNumber) + " < 1024. May be invalid.", ctx)

        # Above 65535 is out of range.
        if (portNumber > 65535):
            self.doError("Port number " + str(portNumber) + ". Out of range 1024 - 65535.", ctx)

    #----------------------------------------------------------------
    # TNSNAMES EXIT
    #----------------------------------------------------------------
    # On exit from the complete tnsnames file, list the run stats and
    # IFILE filenames for further processing. They are not checked by
    # this script automatically (yet!) so need to be done manually.
    #----------------------------------------------------------------
    def exitTnsnames(self, ctx):
        # Advise the user of the state of the tnsnames.ora file.
	global totalInfo
	global totalWarnings
	global totalErrors
	global duplicateCount
        print("\nParsing Information:");
        print("===================");
        print("INFORMATION      : " + str(totalInfo))
        print("PARSER WARNINGS  : " + str(totalWarnings))
        print("PARSER ERRORS    : " + str(totalErrors))
        print("DUPLICATE ENTRIES: " + str(duplicateCount))
	for i in range(0, duplicateCount):
		print('Duplicate[' + str(i + 1)  + ']' + ' = ' + duplicateNames[i])

if __name__ == '__main__':
    main(sys.argv)
