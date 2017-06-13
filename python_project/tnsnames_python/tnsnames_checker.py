#!/usr/local/jython/bin/jython

# Import some python stuff
import fileinput
import os
import sys

# Import ANTLR's runtime libraries
from tnsnamesLexer import tnsnamesLexer
from tnsnamesParser import tnsnamesParser
from tnsnamesInterfaceListener import tnsnamesInterfaceListener
import antlr4

def main(argv):
    
    formattingLineBold = "==================================================="
    formattingLineDot = "---------------------------------------------------"
    thisVersion = "1.0"
    
    print(formattingLineBold)
    print("Tnsnames Checker - Version " + thisVersion + ".")
    print(formattingLineBold + "\n")
    os.linesep
    
    # bring in the file
    # noinspection PyUnresolvedReferences
    input = antlr4.FileStream(argv[1])
    
    # The lexer reads from the input CharStream
    lexer = tnsnamesLexer(input)

    # Fetch a list of lexer tokens. For the parser.
    # noinspection PyUnresolvedReferences
    stream = antlr4.CommonTokenStream(lexer)

    # Stuff those tokens into the parser.
    parser = tnsnamesParser(stream)

    print("Using grammar defined in " + parser.grammarFileName + ", downloadable from:" )
    print("\thttps://github.com/NormanDunbar/grammars-v4/tree/master/tnsnames.\n")
    
    # Start parsing the tnsnames.ora file on stdin.
    # Parsing is deemed to be from the 'tnsnames' rule.

    print(formattingLineBold)
    print("Parsing tnsnames file '" + argv[1] + "' ...")
    print(formattingLineBold +"\n")
    print("\n" + formattingLineDot)
    print("Syntax checking ...")
    print(formattingLineDot + "\n")
    tree = parser.tnsnames()
    print(formattingLineDot)
    print("Syntax checking complete.")
    print(formattingLineDot + "\n")
    tnsWalker = antlr4.ParseTreeWalker()
    tnsListener = tnsnamesInterfaceListener(parser)
    print(formattingLineDot)
    print("Semantic checking ...")
    print(formattingLineDot + "\n")
    tnsWalker.walk(tnsListener, tree)
    print(formattingLineDot)
    print("Semantic checking complete.")
    print(formattingLineDot + "\n")
    print(formattingLineBold)
    print("Parsing tnsnames file '" + argv[1] + "' complete.")
    print(formattingLineBold)

if __name__ == '__main__':
    main(sys.argv)
