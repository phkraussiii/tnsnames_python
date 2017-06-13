Working on writing tnsnames checker in python.

added to pycharm

TNSNAMES CHECKER 0.4
====================

Please note, since version 0.3 was originally created, I no longer have access to Java version 1.6 aka Java 6. As far as I am aware, the code will still compile and run under Java 6 but the download now requires Java 7 aka Java verion 1.7 (Does Java have to be so damned difficult?). If you see any mention of Java 6/1.6 in the text below, it means I've missed a bit in removing it!

If you only have Java 6/1.6 then I'm afraid you'll have to download the source and build it yourself. Sorry. :-(


Changes
=======

You may skip to the "Steps to Install" section below, if you wish.


Version 0.4
-----------

* Downloadable binaries now compiled with Java 7 aka Java version 1.7 instead of Java 6/1.6. The code will still compile with Java 6/1.6, it's just that I no longer have that version to build the download with.
* Allows IFILE entries to contain filenames delimited by single, double or no quotes at all.
* The list of IFILEs at the end is in a better format. (Other opinions are available!)
* Allows host, service, instance etc names to contain reserved words. For example, a service of "someservice.service.domain.co.uk" is now acceptable. Version 0.3 produced errors. This was issue 232 on GitHub - see https://github.com/antlr/grammars-v4/issues/232
* the tnsnames_checker.sh file was, in version 0.3, pretty much useless as it was simply a copy of the Windows file, tnsnames_checker.cmd. Major oops! This has been corrected and tested.


Version 0.3
-----------

* First version released into the wild.



Steps to Install:
=================

1. Tnsnames_checker requires Java 6/1.6 at a minimum - if you build it from source yourself, otherwise, it has been built for you with Java 7/1.7 and runs happily under that, or higher versions.

2. Save the zip file. Assume in c:\tnsnames on a Windows box or $HOME/tnsnames on a Linux box.

3. cd c:\tnsnames (Windows) or $HOME/tnsnames (Linux).

4. unzip tnsnames_checker.zip. You will now see the following files:

    antlr-4.4-complete.jar - Support routines.
    tnsnames_checker.jar - The parser itself. Compiled for Java 7/1.7.
    tnsnames_checker.cmd - Windows "run it" command file.
    tnsnames_checker.sh - Unix "run it" script.
    tnsnames.test.ora - the world's worst tnsnames.ora file.
    ReadMe.txt - this file.

5. Optional - add the two jar files to the CLASSPATH environment variable. This means that you can run the utility without having to be in its home folder:

    Windows: set CLASSPATH="c:\tnsnames\antlr-4.4-complete.jar:c:\tnsnames\tnsnames_checker.jar:%CLASSPATH%"
    Linux: export CLASSPATH="${HOME}/tnsnames/antlr-4.4-complete.jar;${HOME}/tnsnames/tnsnames_checker.jar;${CLASSPATH}"

6. It is assumed that JAVA_HOME points at your favoured Java JRE (or JDK) installation and that your PATH is correctly set.

    java -version

Should return something like:

    java version "1.7.0_51"
    Java(TM) SE Runtime Environment (build 1.7.0_51-b13)
    Java HotSpot(TM) 64-Bit Server VM (build 24.51-b03, mixed mode)


Running the Utility:
====================

You only need one parameter, the name of a tnsnames.ora file to be parsed. By default, all output is to the screen although output messages are split between the normal output and the error channel, so can be redirected to separate files, if necessary.

All INFO, WARNING or ERROR messages are sent to the error channel. All other messages, statistics etc, are sent to the normal output channel.


1. Output to screen:

Windows: tnsnames_checker.cmd tnsnames.test.ora
Linux: ./tnsnames_checker.cmd tnsnames.test.ora


2. Output to two files, messages and errors/warnings separately:

Windows: tnsnames_checker.cmd tnsnames.test.ora >details.txt 2>errors.txt
Linux: ./tnsnames_checker.cmd tnsnames.test.ora >details.txt 2>errors.txt


3. Everything to one file:

Windows: tnsnames_checker.cmd tnsnames.test.ora >all_out.txt 2>&1
Linux: ./tnsnames_checker.cmd tnsnames.test.ora >all_out.txt 2>&1


Sample Output:
==============

The following is the sample output from running the utility against the "tnsnames.ora from Hell" file, as supplied. There are numerous errors encoded in that file and I think it tests everything built in to the checker.

It has lever errors, parser errors and semantic errors built in.


================================================================================
Tnsnames Checker - Version 0.4.
================================================================================

Using TNSNAMES specification version for Oracle 11gR2, as defined at:
	http://docs.oracle.com/cd/E11882_01/network.112/e10835/tnsnames.htm.

Using grammar defined in tnsnamesParser.g4, downloadable from:
	https://github.com/NormanDunbar/grammars-v4/tree/master/tnsnames.

The official ANTLR version is downloadable from:
	https://github.com/antlr/grammars-v4/tree/master/tnsnames.
(This may not be as up to date if there are any pull requests outstanding.)

================================================================================
Parsing tnsnames file '/home/norman/tnsnames/tnsnames.test.ora' ...
================================================================================

--------------------------------------------------------------------------------
Syntax checking ...
--------------------------------------------------------------------------------
line 210:7 extraneous input ')' expecting '('
line 310:15 no viable alternative at input 'rmancatalog=()'
Syntax checking complete.

--------------------------------------------------------------------------------
Semantic checking ...
--------------------------------------------------------------------------------

Line 12:1  Listener alias found: LSNR_FRED
*** INFO: 0, WARNING: 0, ERRORS: 0

Line 21:1  Listener alias found: LSNR_HEXFRED
*** INFO: 0, WARNING: 0, ERRORS: 0

Line 30:1  Listener alias found: LSNR_OCTFRED
*** INFO: 0, WARNING: 0, ERRORS: 0

Line 39:1  Listener alias found: LSNR_MIXFRED
*** INFO: 0, WARNING: 0, ERRORS: 0

Line 48:1  Listener alias found: LSNR_MESSFRED
	Line 50:40 ERROR: dotQuad '0xFe0' in '10.0xFe0.029.0X27' out of range 0 - 254.
*** INFO: 0, WARNING: 0, ERRORS: 1

Line 57:1  Listener alias found: LSNR_MESSFRED
	Line 57:1 ERROR: Duplicate alias - LSNR_MESSFRED
	Line 59:40 ERROR: dotQuad '0xFe0' in '10.0xFe0.029.0X27' out of range 0 - 254.
*** INFO: 0, WARNING: 0, ERRORS: 2

Line 66:1  Listener alias found: LSNR_WILMA
	Line 67:46 WARNING: PROTOCOL parameter redefines PROTOCOL parameter at line 67.
	Line 67:62 WARNING: KEY parameter redefines KEY parameter at line 67.
*** INFO: 0, WARNING: 2, ERRORS: 0

Line 74:1  Listener alias found: lsnr_barney
*** INFO: 0, WARNING: 0, ERRORS: 0

Line 86:1  Listener alias found: lsnr_betty
	Line 87:3 WARNING: Missing ADDRESS_LIST, 2 ADDRESS entries found.
*** INFO: 0, WARNING: 1, ERRORS: 0

Line 107:1  Database alias found: alias_1,alias_2.world,alias3.dunbar-it.co.uk
	Line 110:8 WARNING: LOAD_BALANCE parameter redefines LOAD_BALANCE parameter at line 109.
	Line 119:84 WARNING: Port number, 80 < 1024. May be invalid.
	Line 120:52 ERROR: dotQuad '0' in '0.2.3.400' out of range 1 - 254.
	Line 120:52 ERROR: dotQuad '400' in '0.2.3.400' out of range 0 - 254.
	Line 125:21 WARNING: PROTOCOL parameter redefines PROTOCOL parameter at line 123.
	Line 127:21 WARNING: PORT parameter redefines PORT parameter at line 126.
	Line 128:21 WARNING: HOST parameter redefines HOST parameter at line 124.
	Line 130:85 ERROR: Port number 65536. Out of range 1024 - 65535.
	Line 135:21 WARNING: PROTOCOL parameter redefines PROTOCOL parameter at line 133.
	Line 136:21 WARNING: KEY parameter redefines KEY parameter at line 134.
	Line 143:28 WARNING: SEND_BUF_SIZE parameter redefines SEND_BUF_SIZE parameter at line 141.
	Line 144:28 WARNING: RECV_BUF_SIZE parameter redefines RECV_BUF_SIZE parameter at line 142.
	Line 149:21 WARNING: PROTOCOL parameter redefines PROTOCOL parameter at line 146.
	Line 156:21 WARNING: ARGV0 parameter redefines ARGV0 parameter at line 154.
	Line 157:21 WARNING: PROGRAM parameter redefines PROGRAM parameter at line 153.
	Line 158:21 WARNING: ARGS parameter redefines ARGS parameter at line 155.
	Line 163:21 WARNING: ARGV0 parameter redefines ARGV0 parameter at line 162.
	Line 164:84 WARNING: LOCAL parameter redefines LOCAL parameter at line 164.
	Line 164:96 WARNING: ADDRESS parameter redefines ADDRESS parameter at line 164.
	Line 164:107 WARNING: PROTOCOL parameter redefines PROTOCOL parameter at line 164.
	Line 169:28 WARNING: PIPE parameter redefines PIPE parameter at line 168.
	Line 170:28 WARNING: SERVER parameter redefines SERVER parameter at line 167.
	Line 171:28 WARNING: PROTOCOL parameter redefines PROTOCOL parameter at line 166.
	Line 175:13 ERROR: SDU value 256. Out of range 512 - 65535.
	Line 176:13 WARNING: SDU parameter redefines SDU parameter at line 175.
	Line 177:13 WARNING: SDU parameter redefines SDU parameter at line 175.
	Line 178:13 WARNING: SDU parameter redefines SDU parameter at line 175.
	Line 178:13 INFO: SDU value 8192. This is the default setting.
	Line 179:13 WARNING: SDU parameter redefines SDU parameter at line 175.
	Line 180:13 WARNING: SDU parameter redefines SDU parameter at line 175.
	Line 180:13 ERROR: SDU value 65536. Out of range 512 - 65535.
	Line 183:28 WARNING: SID parameter redefines SID parameter at line 183.
	Line 183:41 WARNING: SID parameter redefines SID parameter at line 183.
	Line 186:15 WARNING: SERVER parameter redefines SERVER parameter at line 184.
	Line 191:15 WARNING: HS parameter redefines HS parameter at line 188.
	Line 192:15 WARNING: UR parameter redefines UR parameter at line 190.
	Line 193:15 WARNING: SERVICE_NAME parameter redefines SERVICE_NAME parameter at line 185.
	Line 194:15 WARNING: SERVICE_NAME parameter redefines SERVICE_NAME parameter at line 185.
	Line 196:13 WARNING: RETRY_COUNT parameter redefines RETRY_COUNT parameter at line 181.
	Line 199:13 WARNING: SDU parameter redefines SDU parameter at line 175.
	Line 199:13 ERROR: SDU value 65536. Out of range 512 - 65535.
	Line 200:13 WARNING: SEND_BUF_SIZE parameter redefines SEND_BUF_SIZE parameter at line 112.
	Line 201:13 WARNING: RECV_BUF_SIZE parameter redefines RECV_BUF_SIZE parameter at line 115.
	Line 203:8 WARNING: Missing ADDRESS_LIST, 4 ADDRESS entries found.
	Line 205:48 ERROR: dotQuad '255' in '10.0.254.255' out of range 0 - 254.
*** INFO: 1, WARNING: 37, ERRORS: 7

Line 217:1  Database alias found: barney
*** INFO: 0, WARNING: 0, ERRORS: 0

Line 230:1  Database alias found: alias3.dunbar-it.co.uk
	Line 230:1 ERROR: Duplicate alias - alias3.dunbar-it.co.uk
*** INFO: 0, WARNING: 0, ERRORS: 1

Line 243:1  Database alias found: pebbles
*** INFO: 0, WARNING: 0, ERRORS: 0

Line 263:1  Database alias found: pebbles_two
	Line 276:11 WARNING: FAILOVER_MODE parameter redefines FAILOVER_MODE parameter at line 267.
	Line 281:17 WARNING: TYPE parameter redefines TYPE parameter at line 280.
	Line 282:17 WARNING: METHOD parameter redefines METHOD parameter at line 277.
	Line 284:17 WARNING: BACKUP parameter redefines BACKUP parameter at line 278.
	Line 285:17 WARNING: DELAY parameter redefines DELAY parameter at line 279.
	Line 286:17 WARNING: RETRIES parameter redefines RETRIES parameter at line 283.
	Line 287:17 WARNING: TYPE parameter redefines TYPE parameter at line 280.
*** INFO: 0, WARNING: 7, ERRORS: 0

Line 299:1  Database alias found: alias.foo.bar
*** INFO: 0, WARNING: 0, ERRORS: 0

================================================================================
Parsing Information:
===================
INFORMATION      : 1
PARSER WARNINGS  : 47
PARSER ERRORS    : 11
DUPLICATE ENTRIES: 2
	Duplicate[0] = 'LSNR_MESSFRED'
	Duplicate[1] = 'alias3.dunbar-it.co.uk'
================================================================================

--------------------------------------------------------------------------------
IFILE List:
--------------------------------------------------------------------------------
Please run the tnsnames_checker script on the following 3 files:
	IFILE[0] = '/this/is/a/double_quoted/ifile/entry/tnsnames.ora' (not found on this computer.)
	IFILE[1] = '/this/is/a/single_quoted/ifile/entry/tnsnames.ora' (not found on this computer.)
	IFILE[2] = '/this/is/an/unquoted/ifile/entry/tnsnames.ora' (not found on this computer.)
End of IFILE List.

Semantic checking complete.

================================================================================
Parsing tnsnames file '/home/norman/tnsnames/tnsnames.test.ora' complete.
================================================================================


