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
EMPTY = 'empty'
NL = 'new line'
HSTG = 'hashtag'


class Lex:
    def __init__(self, fileName) -> None:
        self.currentLine = 1
        self.fileName = fileName
        self.token = None
        self.fileToRead = open(fileName, 'r')
        self.tokenList = []

    def error():
        print("Error: invalid character")

    def readFile(self):
        with self.fileToRead as file:
            while True:
                if not self.nextToken():
                    break

    def printTokenList(self):
        for token in self.tokenList:
            print(token)
    
    def nextToken(self) :
        token = self.fileToRead.read(1)
        words = ['main', 'def' , '#def' , '#int' , 'global' , 'if' , 'elif' 
                 , 'else' , 'while' , 'print' , 'return' , 'input' , 'int' , 'and' , 'or' , 'not']

        if not token:
            return None
        if token == '\n':
            self.token = Token(NL, "\\"+"n", self.currentLine)
            self.tokenList.append(self.token)
            self.currentLine += 1
            return self.nextToken()
        if token == ' ':
            self.token = Token(EMPTY, token, self.currentLine)
        if token in NUMBERS:
            self.token = Token(NUM, token, self.currentLine)
            self.tokenList.append(self.token)
            return self.token
        if token == '+' or token == '-':
            self.token = Token(ADD_OP, token, self.currentLine)
            self.tokenList.append(self.token)
            return self.token
        if token == '*' or token == '/':
            self.token = Token(MUL_OP, token, self.currentLine)
            self.tokenList.append(self.token)
            return self.token
        if token == '(' or token == ')':
            self.token = Token(GRP_SMBL, token, self.currentLine)
            self.tokenList.append(self.token)
            return self.token
        if token == ';' or token == ',':
            self.token = Token(DLMTR, token, self.currentLine)
            self.tokenList.append(self.token)
            return self.token
        if token == '=':
            self.token = Token(ASGN, token, self.currentLine)
            self.tokenList.append(self.token)
            return self.token
        if token == '<' or token == '>' or token == '!' or token == '=':
            self.token = Token(REL_OP, token, self.currentLine)
            self.tokenList.append(self.token)
            return self.token
        if token == ':':
            self.token = Token(DLMTR, token, self.currentLine)
            self.tokenList.append(self.token)
            return self.token
        if token == '#':
            last_token  = self.token
            if last_token.family is HSTG:
                word = last_token.recognizedString + token
                self.token = Token(COMMENT, word, self.currentLine)
                self.tokenList.pop()
                self.tokenList.append(self.token)
                return self.nextToken()
            else:
                self.token = Token(HSTG, token, self.currentLine)
                self.tokenList.append(self.token)
                return self.token
        if token.isalpha():
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
                return self.token
        else:
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
        while True:
            
            self.defMainFunction()
            self.nextToken()

            

lex = Lex(r'C:\Users\Philip\Desktop\UOI\Metafrastes\Metafrastes\test.cpy')
lex.readFile()
lex.printTokenList()


parser = Parser(lex.tokenList)
parser.parse()
