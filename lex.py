#FILIPPOS ATHANASOPULOS ANTYRAS 5113
#IOANNIS MPOUZAS 5025

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

        if not token:
            return None
        if token == '\n':
            self.currentLine += 1
            return self.nextToken()
        if token == ' ':
            return self.nextToken()
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
        if token.isalpha():
            self.token = Token(ID_KW, token, self.currentLine)
            self.tokenList.append(self.token)
            return self.token
        else:
            return self.nextToken()
    
NUMBERS = '0123456789'
NUM = 'number'
ID_KW = 'identifier or keyword'
ADD_OP = 'add operator'
MUL_OP = 'mul operator'
GRP_SMBL = 'group symbol'
DLMTR = 'delimiter'
ASGN = 'assignment'
REL_OP = 'rel operator'

class Token:
    def __init__(self, family, recognizedString, lineNumber) -> None:
        self.family = family
        self.recognizedString = recognizedString
        self.lineNumber = lineNumber

    def __str__(self) -> str:
        return self.recognizedString + "   "+ "family: " + '"' + self.family + '"' + " line: " + str(self.lineNumber)
lex = Lex(r'C:\Users\Philip\Desktop\UOI\Metafrastes\Metafrastes\test.cpy')
lex.readFile()
lex.printTokenList()
