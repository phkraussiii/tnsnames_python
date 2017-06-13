#!/usr/bin/env bash
# Assumes that the antlr_shell.sh script has been sourced prior
# to calling this build file:
#
# build.sh now has antlr_shell.sh combined with it
#
 
if [ -z "${JAVA_HOME}" ]
then
        export JAVA_HOME='/Library/Java/JavaVirtualMachines/jdk1.8.0_121.jdk/Contents/Home'
fi
 
# You need to set this to the location of your ANTLR4 jar file.
ANTLR4="/usr/local/lib/antlr-4.7-complete.jar"
if [ ! -f "${ANTLR4}" ]
then
        echo "Cannot locate file \""${ANTLR4}"\""
        exit 1
fi
export CLASSPATH=".:${CLASSPATH}:${ANTLR4}"
 
# Alias to compile an ANTLR4 grammar.
alias antlr4='java org.antlr.v4.Tool'
 
# Alias to test run a parser or parser rule.
alias grun='java org.antlr.v4.runtime.misc.TestRig'
 
# Aliases to jar, run and compile Java files.
alias jar='${JAVA_HOME}/bin/jar'
alias java='${JAVA_HOME}/bin/java'
alias javac='${JAVA_HOME}/bin/javac'
 
 
echo " "
echo "Compiling grammar ..."
/Library/Java/JavaVirtualMachines/jdk1.8.0_121.jdk/Contents/Home/bin/java org.antlr.v4.Tool tnsnamesLexer.g4
/Library/Java/JavaVirtualMachines/jdk1.8.0_121.jdk/Contents/Home/bin/java org.antlr.v4.Tool tnsnamesParser.g4
 
echo "Compiling java ..."
javac *.java
 
echo "Creating jar ..."
jar -cvf tnsnames_checker.jar *.class > /dev/null
 
echo "Cleaning up ..."
rm *.class
 
echo "Done."
echo " "
