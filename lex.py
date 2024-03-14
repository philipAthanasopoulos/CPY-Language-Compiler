# FILIPPOS ATHANASOPULOS ANTYRAS 5113
# IOANNIS MPOUZAS 5025

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
DCLR = 'declaration'
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
        print("\033[91m" + "Error: invalid character" + "\033[0m" + " at line: ", token.lineNumber, " token: ",
              token.recognizedString)
        self.errors = True

    def error(self, token, message):
        print("\033[91m" + "Error: invalid character" + "\033[0m" + " at line: ", token.lineNumber, ", ", message)
        self.errors = True

    def printTokenList(self):
        for token in self.tokenList:
            print(token)

    reserved_words = ['main', 'def', '#def', '#int', 'global', 'if', 'elif'
        , 'else', 'while', 'print', 'return', 'input', 'int', 'and', 'or', 'not']

    def nextToken(self):
        token = self.fileToRead.read(1)

        if self.token is not None and self.token.family is UNASSIGNED and token != '=':
            self.error(self.token, "'!' is not a valid character, did you mean '!=' ?")
            self.tokenList[-1] = self.token
        if not token:
            return None
        elif token == '\n':
            self.token = Token(NL, "\\" + "n", self.currentLine)
            self.tokenList.append(self.token)
            self.currentLine += 1
            return self.nextToken()
        elif token == ' ':
            self.token = Token(WHITE_SPACE, '" "', self.currentLine)
            self.tokenList.append(self.token)
        elif token in NUMBERS:
            last_token = self.token
            if last_token.family is ID_KW:
                self.token = Token(ID_KW, last_token.recognizedString + token, self.currentLine)
                self.tokenList.pop()
                self.tokenList.append(self.token)
            elif last_token.family is NUM:
                self.token = Token(NUM, last_token.recognizedString + token, self.currentLine)
                self.tokenList.pop()
                self.tokenList.append(self.token)
            else:
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
            last_token = self.token
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
            last_token = self.token
            if last_token.recognizedString == '#':
                self.token = Token(GRP_SMBL, "#" + token, self.currentLine)
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
            last_token = self.token
            if last_token.family in [REL_OP, ASGN, UNASSIGNED]:
                self.token = Token(REL_OP, last_token.recognizedString + token, self.currentLine)
                self.tokenList.pop()
                self.tokenList.append(self.token)
                return self.nextToken()
            else:
                self.token = Token(ASGN, token, self.currentLine)
                self.tokenList.append(self.token)
                return self.nextToken()
        elif token == '#':
            last_token = self.token
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
            last_token = self.token
            if last_token.family is ID_KW:
                word = last_token.recognizedString + token
                self.token = Token(ID_KW, word, self.currentLine)
                self.tokenList.pop()
                self.tokenList.append(self.token)
                # handle keywords
                if self.tokenList[-2].recognizedString == '#':
                    if self.token.recognizedString == 'int':
                        self.tokenList.pop()
                        self.tokenList.pop()
                        self.token = Token(DCLR, '#int', self.currentLine)
                        self.tokenList.append(self.token)
                    elif self.token.recognizedString == 'def':
                        self.tokenList.pop()
                        self.tokenList.pop()
                        self.token = Token(DCLR, '#def', self.currentLine)
                        self.tokenList.append(self.token)
                elif self.token.recognizedString == 'def':
                    self.token.family = DCLR
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
        return '\033[92m' + self.recognizedString + '\033[0m' + "   " + "family: " + '"' + self.family + '"' + " line: " + str(
            self.lineNumber)


class Parser:
    def __init__(self, tokenList) -> None:
        self.tokenList = tokenList
        self.currentToken = tokenList[0]
        self.tokenIndex = 0
        print("Started syntax analysis")

    def error(self, error_message, token):
        print(error_message, " at line " + str(token.lineNumber))

    def nextToken(self):
        self.tokenIndex += 1
        self.currentToken = self.tokenList[self.tokenIndex]
        # print("Reading token ", self.currentToken)

    def declaration(self):
        if self.currentToken.recognizedString == '#int':
            self.nextToken()
            if self.currentToken.family is WHITE_SPACE:
                self.nextToken()
                if self.currentToken.family is ID_KW:
                    self.nextToken()
                    ##TODO do rest
                else:
                    self.error("Missing variable name", self.currentToken)
            else:
                self.error("Syntax error near #int declaration", self.currentToken)
        elif self.currentToken.recognizedString == 'def':
            self.nextToken()
            if self.currentToken.family is WHITE_SPACE:
                self.nextToken()
                if self.currentToken.family is ID_KW:
                    self.nextToken()
                    if self.currentToken.recognizedString == '(':
                        self.nextToken()
                        ##TODO handle parameters
                        while self.currentToken.recognizedString != ')':
                            self.nextToken()
                        self.nextToken()
                        if self.currentToken.recognizedString == ':':
                            self.nextToken()
                        else:
                            self.error("missing ':' after function declaration", self.currentToken)
                    else:
                        self.error("Missing variable parameters", self.currentToken)
                else:
                    self.error("Missing variable name", self.currentToken)
            else:
                self.error("Syntax error near 'def' declaration", self.currentToken)
        elif self.currentToken.recognizedString == '#def':
            self.nextToken()

            if self.currentToken.family is WHITE_SPACE:
                self.nextToken()
                if self.currentToken.recognizedString == 'main':
                    ##TODO handle main part
                    self.nextToken()
                else:
                    self.error("Missing 'main' after function declaration", self.currentToken)
            else:
                self.error("Syntax error near main function declaration", self.currentToken)
        else:
            self.error("Syntax error near declaration", self.currentToken)

    def analyze(self):
        while self.tokenIndex < len(self.tokenList):
            if self.currentToken.family is DCLR:
                self.declaration()
            self.nextToken()
        print("Finished syntax analysis")


# TODO change sos that the user enters the path of the file
lex = Lex(r'C:\Users\Philip\Desktop\UOI\Metafrastes\Metafrastes\test.cpy')
# lex = Lex(r'/workspaces/Metafrastes/test.cpy')
lex.readFile()

if not lex.errors:
    lex.printTokenList()
    parser = Parser(lex.tokenList)
    parser.analyze()
