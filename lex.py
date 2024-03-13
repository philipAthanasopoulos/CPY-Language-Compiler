#FILIPPOS ATHANASOPULOS ANTYRAS 5113
#IOANNIS MPOUZAS 5025

NUMBERS = '0123456789'
NUM = 'number'
ID_KW = 'identifier or keyword'
ADD_OP = 'add operator'
MUL_OP = 'mul operator'
GRP_SMBL = 'group symbol'
DLMTR = 'delimiter'
ASGN = 'assignment'
REL_OP = 'rel operator'
COMMENT = 'comment'
WHITE_SPACE = 'white space'
NL = 'new line'
HSTG = 'hashtag'
ERROR = 'error'
UNASSIGNED = 'unassigned'

class Lex:
    def __init__(self, fileName) -> None:
        self.currentLine = 1
        self.fileName = fileName
        self.token = None
        self.fileToRead = open(fileName, 'r')
        self.tokenList = []
        self.errors = False

    def readFile(self):
        with self.fileToRead as file:
            while True:
                if not self.nextToken():
                    break

    def error(self, token):
        print("\033[91m" + "Error: invalid character" + "\033[0m" + " at line: " , token.lineNumber , " token: " , token.recognizedString)
        self.errors = True
    def error(self, token, message):
        print("\033[91m" + "Error: invalid character" + "\033[0m" + " at line: " , token.lineNumber , ", ", message)
        self.errors = True

    def printTokenList(self):
        for token in self.tokenList:
            print(token)
    
    reserved_words = ['main', 'def' , '#def' , '#int' , 'global' , 'if' , 'elif' 
                , 'else' , 'while' , 'print' , 'return' , 'input' , 'int' , 'and' , 'or' , 'not']
    
    def nextToken(self) :
        token = self.fileToRead.read(1)

        if self.token is not None and self.token.family is UNASSIGNED and token != '=':
            self.error(self.token , "'!' is not a valid character, did you mean '!=' ?")
            self.tokenList[-1] = self.token
        if not token:
            return None
        elif token == '\n':
            self.token = Token(NL, "\\"+"n", self.currentLine)
            self.tokenList.append(self.token)
            self.currentLine += 1
            return self.nextToken()
        elif token == ' ':
            self.token = Token(WHITE_SPACE, '" "', self.currentLine)
            self.tokenList.append(self.token)
        elif token in NUMBERS:
            self.token = Token(NUM, token, self.currentLine)
            self.tokenList.append(self.token)
            return self.token
        elif token == '+' or token == '-':
            self.token = Token(ADD_OP, token, self.currentLine)
            self.tokenList.append(self.token)
            return self.token
        elif token == '*' or token == '%':
            self.token = Token(MUL_OP, token, self.currentLine)
            self.tokenList.append(self.token)
            return self.token
        elif token == '/':
            last_token  = self.token
            if last_token.recognizedString == '/':
                self.token = Token(MUL_OP, '//', self.currentLine)
                self.tokenList.pop()
                self.tokenList.append(self.token)
                return self.nextToken()
            else:
                self.token = Token(MUL_OP, token, self.currentLine)
                self.tokenList.append(self.token)
                return self.nextToken()
        elif token == '(' or token == ')':
            self.token = Token(GRP_SMBL, token, self.currentLine)
            self.tokenList.append(self.token)
            return self.nextToken()
        elif token == '{' or token == '}':
            last_token  = self.token
            if last_token.recognizedString == '#':
                self.token = Token(GRP_SMBL, "#"+token, self.currentLine)
                self.tokenList.pop()
                self.tokenList.append(self.token)
                return self.nextToken()
            else:
                self.token = Token(GRP_SMBL, token, self.currentLine)
                self.error(self.token, "missing '#' before '" + token + "'")
                self.tokenList.append(self.token)
                return self.nextToken()
        elif token == ':' or token == ',':
            self.token = Token(DLMTR, token, self.currentLine)
            self.tokenList.append(self.token)
            return self.token
        elif token == '<' or token == '>':
            self.token = Token(REL_OP, token, self.currentLine)
            self.tokenList.append(self.token)
            return self.nextToken()
        elif token == '!':
            self.token = Token(UNASSIGNED, token, self.currentLine)
            self.tokenList.append(self.token)
            return self.nextToken()
        elif token == '=':
            last_token  = self.token
            if last_token.family in [REL_OP,ASGN,UNASSIGNED]:
                self.token = Token(REL_OP, last_token.recognizedString + token, self.currentLine)
                self.tokenList.pop()
                self.tokenList.append(self.token)
                return self.nextToken()
            else:
                self.token = Token(ASGN, token, self.currentLine)
                self.tokenList.append(self.token)
                return self.nextToken()
        elif token == '#':
            last_token  = self.token
            if last_token.family is HSTG:
                self.token = Token(COMMENT, "##", self.currentLine)
                self.tokenList.pop()
                self.tokenList.append(self.token)
                return self.nextToken()
            elif last_token.recognizedString == '}':
                self.token = Token(GRP_SMBL, '}#', self.currentLine)
                self.tokenList.pop()
                self.tokenList.append(self.token)
                return self.nextToken()
            else:
                self.token = Token(HSTG, token, self.currentLine)
                self.tokenList.append(self.token)
                return self.nextToken()
        elif token.isalpha():
            last_token  = self.token
            if last_token.family is ID_KW:
                word = last_token.recognizedString + token
                self.token = Token(ID_KW, word, self.currentLine)
                self.tokenList.pop()
                self.tokenList.append(self.token)
                return self.nextToken()
            else:
                self.token = Token(ID_KW, token, self.currentLine)
                self.tokenList.append(self.token)
                return self.nextToken()
        else:
            self.token = Token(ERROR, token, self.currentLine)
            self.error(self.token, "invalid character '" + token + "'")
            
        return self.nextToken()

class Token:
    def __init__(self, family, recognizedString, lineNumber) -> None:
        self.family = family
        self.recognizedString = recognizedString
        self.lineNumber = lineNumber

    def __str__(self) -> str:
        return '\033[92m' + self.recognizedString + '\033[0m' + "   "+ "family: " + '"' + self.family + '"' + " line: " + str(self.lineNumber)

class Parser:
    def __init__(self, tokenList) -> None:
        self.tokenList = tokenList
        self.currentToken = tokenList[0]
        self.tokenIndex = 0
        print("Initialized Parser")
        print(self.currentToken)

    def error(self,error_mesage):
        print(error_mesage)

    def nextToken(self):
        self.tokenIndex += 1
        self.currentToken = self.tokenList[self.tokenIndex]
        print("Reading token " , self.currentToken)

    def defMainFunction(self):
        if self.currentToken.recognizedString == '#':
            self.nextToken()
            if self.currentToken.recognizedString == 'def':
                self.nextToken()
                if self.currentToken.recognizedString == 'main':
                    print("Found main function")
                    self.nextToken()
                
    def structuredStatement(self):
        if self.currentToken.recognizedString == 'if':
            self.ifStatement()
        elif self.currentToken.recognizedString == 'while':
            self.whileStatement()

    def ifStatement(self):
        print("Found if statement")

    def whileStatement(self):
        print("Found while statement")
        
    def parse(self):
        while self.tokenIndex < len(self.tokenList) - 1:
            self.defMainFunction()
            self.nextToken()

            

##TODO change sos that the user enters the path of the file
# lex = Lex(r'C:\Users\Philip\Desktop\UOI\Metafrastes\Metafrastes\test.cpy')
lex = Lex(r'/workspaces/Metafrastes/test.cpy')
lex.readFile()

if not lex.errors:
    parser = Parser(lex.tokenList)
    parser.parse()


