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
NONE = 'none'


class Lex:
    def __init__(self, fileName) -> None:
        self.currentLine = 1
        self.fileName = fileName
        self.token = Token(NONE, "none", 0)
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
                if len(self.tokenList) > 1 and self.tokenList[-2].recognizedString == '#':
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
        self.analyze()

    def error(self, error_message, token):
        print(error_message, " at line " + str(token.lineNumber))

    def nextToken(self):
        self.tokenIndex += 1
        self.currentToken = self.tokenList[self.tokenIndex]
        # print("Reading token ", self.currentToken)

    def program(self):
        self.block()

    def block(self):
        return self.declarations() or self.subprograms() or self.blockstatemets()

    def declarations(self):
        if self.currentToken.recognizedString in ['#int', 'global']:
            print("Checking declarations")
            if self.varlist():
                pass
            else:
                self.error("Missing variable name near declaration", self.currentToken)

    def varlist(self):
        print("In varlist")
        self.nextToken()  # consume #decl
        if self.currentToken.family is not WHITE_SPACE:
            self.error("Syntax error near variable declaration, missing white space", self.currentToken)
        self.nextToken()  # consume white space
        if self.currentToken.family is not ID_KW:
            print("NO variables found")
            return False
        while self.currentToken.family is ID_KW:
            print("Reading variable", self.currentToken.recognizedString)
            self.nextToken()
            if self.currentToken.recognizedString != ',':
                return True
            if self.currentToken.recognizedString == ',':
                self.nextToken()
            else:
                return True

            # global a,b,c

    def subprograms(self):
        self.subprogram()

    def subprogram(self):
        if self.currentToken.recognizedString == 'def':
            self.nextToken()
            if self.currentToken.family is WHITE_SPACE:
                self.nextToken()
                if self.currentToken.family is ID_KW:
                    self.nextToken()
                    if self.formalparlist():
                        if self.currentToken.recognizedString == ':':
                            self.nextToken()
                            if self.currentToken.family is NL:
                                self.nextToken()
                                if self.block():
                                    pass #FIXME
                                else:
                                    self.error("Syntax error, missing code block", self.currentToken)
                            else:
                                self.error("Syntax error, missing new line after function declaration",
                                           self.currentToken)
                        else:
                            self.error("Syntax error near function parameters, missing ':'", self.currentToken)
                    else:
                        self.error("Syntax error, missing parameters", self.currentToken)
                else:
                    self.error("Syntax error near function name", self.currentToken)
            else:
                self.error("Syntax error near 'def' declaration", self.currentToken)

    def formalparlist(self):
        print("Reading char:", self.currentToken.recognizedString)
        self.nextToken()  # consume (
        while self.currentToken.family is WHITE_SPACE:
            self.nextToken()
        self.formalparitem()
        while self.currentToken.family is WHITE_SPACE:
            self.nextToken()
        print("Checking par list")
        while self.currentToken.recognizedString == ',':
            self.nextToken()  # consume comma
            while self.currentToken.family is WHITE_SPACE:
                self.nextToken()
            self.formalparitem()
            while self.currentToken.family is WHITE_SPACE:
                self.nextToken()
        print("Reading char:", self.currentToken.recognizedString)
        self.nextToken()  # consume )
        print("Finished par list")
        return True

    def formalparitem(self):
        if self.currentToken.family is ID_KW:
            # print("Read param", self.currentToken.recognizedString)
            self.nextToken()  # consume ID

    def statements(self):
        if self.currentToken.recognizedString == '#{':
            while self.currentToken.recognizedString != '#}':
                self.nextToken()
                self.statement()
        else:
            self.statement()

    def blockstatemets(self):
        return self.statement()  # FIXME

    def statement(self):
        # return self.assignStat() or self.ifStat() or self.whileStat() or self.returnStat() or self.inputStat() or self.printStat()
        return self.returnStat()

    def assignStat(self):
        pass

    def ifStat(self):
        self.nextToken()  # consume if
        if self.currentToken.family is WHITE_SPACE:
            self.nextToken()
            self.condition()
            if self.currentToken.family is NL:
                self.nextToken()
                self.statements()
                self.elsePart()
            else:
                self.error("Missing new line after condition", self.currentToken)
        else:
            self.error("Syntax error near 'if' statement", self.currentToken)

    def elsePart(self):
        if self.currentToken.recognizedString == 'else':
            self.nextToken()
            if self.currentToken.family is NL:
                self.nextToken()
                self.statements()
            else:
                self.error("Missing new line after else", self.currentToken)
        else:
            return  # else part is not mandatory

    def whileStat(self):
        if self.currentToken.recognizedString == 'while':
            self.nextToken()
            if self.currentToken.family is WHITE_SPACE:
                self.nextToken()
                self.conditions()
                if self.currentToken.family is NL:
                    self.nextToken()
                    self.statements()
                else:
                    self.error("Missing new line after condition", self.currentToken)
            else:
                self.error("Syntax error near 'while' statement", self.currentToken)

    def returnStat(self):
        print("in returnStat")
        if self.currentToken.recognizedString == 'return':
            self.nextToken()  # consume return
            # if self.expression():
            #     pass
            # else:
            #     self.error("Missing value after return statement", self.currentToken)
        return True

    def printStat(self):
        print(" in printStat")
        if self.currentToken.recognizedString == "print":
            self.nextToken()
            if self.currentToken.recognizedString == '(':
                self.nextToken()
                self.expression()  # read expression to print
                if self.currentToken.recognizedString == ')':
                    self.nextToken()
                    return True
                else:
                    self.error("missing ')' after expression", self.currentToken)
            else:
                self.error("missing '(' before expression", self.currentToken)
        else:
            self.error("missing 'print' keyword", self.currentToken)
        return False

    def inputStat(self):
        print("in inputStat")
        if self.currentToken.recognizedString == 'int':
            self.nextToken()
            if self.currentToken.recognizedString == '(':
                self.nextToken()
                if self.currentToken.recognizedString == 'input':
                    self.nextToken()
                    if self.currentToken.recognizedString == '(':
                        self.nextToken()
                        if self.currentToken.recognizedString == ')':
                            self.nextToken()
                            if self.currentToken.recognizedString == ')':
                                self.nextToken()
                                return True
                            else:
                                self.error("missing ')' after 'input'", self.currentToken)
                        else:
                            self.error("missing ')' after 'input'", self.currentToken)
                    else:
                        self.error("missing '(' before 'input'", self.currentToken)
                else:
                    self.error("missing 'input' keyword", self.currentToken)
            else:
                self.error("missing '(' before 'input'", self.currentToken)

        return False

    def actualparlist(self):
        self.actualParItem()
        while self.currentToken.recognizedString == ',':
            self.nextToken()
            self.actualParItem()

    def actualparitem(self):
        self.expression()

    def condition(self):
        self.boolTerm()
        while self.currentToken.recognizedString == 'or':
            self.nextToken()
            self.boolTerm()

    def boolTerm(self):
        self.nextToken()
        self.boolFactor()
        while self.currentToken.recognizedString == 'and':
            self.nextToken()
            self.boolFactor()

    def boolFactor(self):
        if self.currentToken.recognizedString == 'not':
            self.nextToken()
            self.condition()

        self.condition()

        self.expression()
        if self.currentToken.family is REL_OP:
            self.nextToken()
            self.expression()

    def expression(self):
        self.optionalSign()
        self.term()
        while self.currentToken.family is ADD_OP:
            self.nextToken()
            self.term()

    def term(self):
        self.factor()
        while self.currentToken.family is MUL_OP:
            self.nextToken()
            self.factor()

    def factor(self):
        if self.currentToken.family is NUM:
            self.nextToken()

        self.expression()

        if self.currentToken.family is ID_KW:
            self.idtail()

    def idtail(self):
        self.actualParList()

    def optionalSign(self):
        if self.currentToken.recognizedString in ['+', '-']:
            self.nextToken()

    def actualParList(self):
        self.actualparitem()
        while self.currentToken.recognizedString == ',':
            self.nextToken()
            self.actualparitem()

    def actualParItem(self):
        self.expression()

    def analyze(self):
        self.program()
        print("Finished syntax analysis")


# lex = Lex(r'C:\Users\Philip\Desktop\UOI\Metafrastes\Metafrastes\test.cpy')
lex = Lex(r'C:\Users\Philip\Desktop\UOI\Metafrastes\Metafrastes\tests\declaration.cpy')
lex.readFile()

if not lex.errors:
    parser = Parser(lex.tokenList)
