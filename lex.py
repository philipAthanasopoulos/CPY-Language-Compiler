# FILIPPOS ATHANASOPULOS ANTYRAS 5113
# IOANNIS MPOUZAS 5025
import sys

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
reserved_words = ['main', 'def', '#def', '#int', 'global', 'if', 'elif'
    , 'else', 'while', 'print', 'return', 'input', 'int', 'and', 'or', 'not']


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
        print("\033[91m Error: \033[0m", error_message, " at line " + str(token.lineNumber))

    def nextToken(self):
        if self.tokenIndex >= len(self.tokenList) - 1:
            print("Run out of Tokens!")
            return False
            sys.exit()
        self.tokenIndex += 1
        self.currentToken = self.tokenList[self.tokenIndex]
        return True

    def program(self):
        self.block()

    def block(self):
        res = False
        while self.currentToken.recognizedString !='#}' and self.hasTokens():
            self.skip_spaces_and_nl()

            if self.declarations():
                res = True

            if self.subprograms():
                res = True

            if self.blockstatements():
                res = True

            if self.mainPart():
                res = True

            if res: print("Found block")

        return res

    def declarations(self):
        print("Looking for declarations")
        self.consume_white_spaces()
        self.consume_new_line()
        while self.declaration():
            self.consume_white_spaces()
            self.consume_new_line()
        return True

    def declaration(self):
        print("Looking for declarations")
        self.consume_white_spaces()
        self.consume_new_line()
        if self.currentToken.recognizedString in ['#int', 'global']:
            print("Checking declaration", self.currentToken.recognizedString)
            if self.varlist():
                return True
            else:
                self.error("Missing variable name near declaration", self.currentToken)
        return False

    def varlist(self):
        print("In varlist")
        self.nextToken()  # consume #decl
        if self.currentToken.family is not WHITE_SPACE:
            self.error("Syntax error near variable declaration, missing white space", self.currentToken)
        self.consume_white_spaces()
        if self.currentToken.family is not ID_KW:
            print("NO variables found")
            return False
        while self.currentToken.family is ID_KW:
            print("Reading variable", self.currentToken.recognizedString)
            self.nextToken()  # consume ID
            self.consume_white_spaces()
            if self.currentToken.recognizedString != ',':
                return True
            if self.currentToken.recognizedString == ',':
                self.nextToken()  # consume comma
                self.consume_white_spaces()
            else:
                return True

    def consume_white_spaces(self):
        while self.currentToken.family is WHITE_SPACE:
            self.nextToken()  # consume white space

    def subprograms(self):
        print("Looking for subprograms")
        if self.subprogram():
            while self.subprogram():
                pass
            return True
        return False

    def subprogram(self):
        print("Looking for subprogram")
        self.skip_spaces_and_nl()
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
                                self.nextToken()  # consume new line
                                self.skip_spaces_and_nl()
                                if self.currentToken.recognizedString == '#{':
                                    self.nextToken()  # consume {
                                    if self.block():
                                        self.skip_spaces_and_nl()
                                        if self.currentToken.recognizedString == '#}':
                                            self.nextToken()  # consume }
                                            return True
                                        else:
                                            self.error("Syntax error, missing closing block", self.currentToken)
                                    else:
                                        self.error("Syntax error, missing code block", self.currentToken)
                                else:
                                    self.error("Syntax error, missing opening block", self.currentToken)
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
        return False

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
        print("Looking for statements")
        if self.statement():
            while self.statement():
                pass
            print('Found statements')
            return True
        return False

    def blockstatements(self):
        print("Looking for blockstatements")
        if self.statement():
            while self.statement():
                pass
            return True
        return False

    def statement(self):
        print("Looking for statement")
        self.skip_spaces_and_nl()
        if self.tokenIndex >= len(self.tokenList):
            return False
        if self.currentToken.recognizedString == 'return':
            return self.returnStat()
        elif self.currentToken.recognizedString == 'if':
            return self.ifStat()
        elif self.currentToken.recognizedString == 'while':
            return self.whileStat()
        elif self.currentToken.family is COMMENT:
            return self.commentStat()
        elif self.currentToken.family is ID_KW and self.currentToken.recognizedString not in reserved_words:
            return self.assignStat()

        return False

    def assignStat(self):
        print("Checking for assignment")
        first_token = self.currentToken
        self.nextToken()  # consume ID
        self.consume_white_spaces()
        if self.currentToken.recognizedString == '=':
            self.nextToken()  # consume =
            self.consume_white_spaces()
            if self.expression():
                print("Found assignment", first_token.recognizedString, "=", self.currentToken.recognizedString)
                return True
        return False

    def ifStat(self):
        print("Found if statement")
        self.nextToken()  # consume if
        if self.currentToken.family is WHITE_SPACE:  # there should be at least one space after if statement
            self.consume_white_spaces()  # consume the rest if any
            if self.condition():
                self.consume_white_spaces()
                if self.currentToken.recognizedString == ':':
                    self.nextToken()  # consume :
                    self.consume_white_spaces()
                    if self.currentToken.family is NL:
                        self.nextToken()  # consume new line
                        self.skip_spaces_and_nl()
                        if self.statements():
                            self.skip_spaces_and_nl()
                            while self.elifStat():  # check for elif statements
                                self.skip_spaces_and_nl()
                                pass
                            self.skip_spaces_and_nl()
                            self.elseStat()
                            return True
                        else:
                            self.error("Missing statements after if", self.currentToken)
                    else:
                        self.error("Missing new line after if", self.currentToken)
                else:
                    self.error("Missing ':' after if", self.currentToken)
        else:
            self.error("Syntax error near 'if' statement", self.currentToken)

    def elifStat(self):
        print("Checking for elif statement")
        print(self.currentToken)
        if self.currentToken.recognizedString == 'elif':
            print("Found elif statement")
            self.nextToken()  # consume elif
            self.consume_white_spaces()
            if self.condition():
                self.consume_white_spaces()
                if self.currentToken.recognizedString == ':':
                    self.nextToken()
                    self.consume_white_spaces()
                    if self.currentToken.family is NL:
                        self.nextToken()  # consume new line
                        self.skip_spaces_and_nl()
                        if self.statements():
                            return True
                        else:
                            self.error("Missing statements after elif", self.currentToken)
                    else:
                        self.error("Missing new line after condition", self.currentToken)
                else:
                    self.error("Missing ':' after condition", self.currentToken)
            else:
                self.error("Missing condition after elif", self.currentToken)

        return False

    def elseStat(self):
        print("Checking for else statement")
        if self.currentToken.recognizedString == 'else':
            print("Found else statement")
            self.nextToken()  # consume else
            self.consume_white_spaces()
            if self.currentToken.recognizedString == ':':
                self.nextToken()  # consume :
                self.skip_spaces_and_nl()
                if self.statements():
                    return True
                else:
                    self.error("Missing statement after else", self.currentToken)
            else:
                self.error("Missing ':' after else", self.currentToken)
        return False

    def skip_spaces_and_nl(self):
        while self.currentToken.family is WHITE_SPACE or self.currentToken.family is NL:
            self.nextToken()

    def whileStat(self):
        print("Found while")
        print(self.currentToken)
        self.nextToken()  # consume while
        if self.currentToken.family is WHITE_SPACE:
            self.consume_white_spaces()
            if self.condition():
                print("Found while condition")
                self.consume_white_spaces()
                if self.currentToken.recognizedString == ':':
                    self.nextToken()  # consume :
                    if self.currentToken.family is NL:
                        self.nextToken()  # consume new line
                        self.skip_spaces_and_nl()
                        if self.currentToken.recognizedString == '#{':
                            self.nextToken()  # consume {
                            self.skip_spaces_and_nl()
                            if self.statements():
                                self.skip_spaces_and_nl()
                                if self.currentToken.recognizedString == '#}':
                                    self.nextToken()
                                    return True
                                else:
                                    self.error("Missing closing block", self.currentToken)
                            else:
                                self.error("Missing statements after while", self.currentToken)
                                print(self.currentToken)
                        else:
                            self.error("Missing opening block", self.currentToken)
                    else:
                        self.error("Missing new line after condition", self.currentToken)
                else:
                    self.error("Missing ':' after condition", self.currentToken)
            else:
                self.error("Missing condition after while", self.currentToken)
        else:
            self.error("Syntax error near 'while' statement", self.currentToken)

        return False

    def returnStat(self):
        print("Found return statement")
        self.nextToken()  # consume return
        while self.currentToken.family is WHITE_SPACE:
            self.nextToken()  # consume white spaces
        if self.expression():
            return True
        else:
            self.error("Missing value after return statement", self.currentToken)
            return False

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
        if self.expression() or self.currentToken.family is ID_KW:
            return True
        return False

    def condition(self):
        print("Checking for condition")
        self.consume_white_spaces()
        if self.boolTerm():
            print("Found condition")
            while self.currentToken.recognizedString == 'or':
                self.nextToken()  # consume or
                if not self.boolTerm(): return False
            print("Returned condition")
            return True
        return False

    def boolTerm(self):
        print("Checking for bool term")
        self.consume_white_spaces()
        if self.boolFactor():
            print("Found bool term")
            while self.currentToken.recognizedString == 'and':
                self.nextToken()  # consume and
                self.consume_white_spaces()
                if not self.boolFactor(): return False
            print("Returned boolTerm")
            return True
        return False

    def boolFactor(self):
        print("Checking for bool factor")
        self.consume_white_spaces()
        if self.expression():
            print("boolfactor found expr")
            self.consume_white_spaces()
            if self.currentToken.family is REL_OP:
                print("Found rel op", self.currentToken.recognizedString)
                self.nextToken()  # consume rel op
                self.consume_white_spaces()
                if self.expression(): return True
        if self.currentToken.recognizedString == 'not':
            self.nextToken()  # consume not
            if self.condition():
                print("boolfactor found condition")
                return True

        if self.condition():
            print("boolfactor found condition")
            return True
        print("Didnt find bool factor")
        return False

    def expression(self):
        print("Checking for expression")
        print(self.currentToken.recognizedString)
        if self.optionalSign():
            if self.term():
                self.consume_white_spaces()
                print(self.currentToken.recognizedString)
                while self.currentToken.family is ADD_OP:
                    print("Found add op", self.currentToken.recognizedString)
                    self.nextToken()  # consume add op
                    if not self.term(): return False
                print("Found expression")
                return True
        else:
            if self.term():
                self.consume_white_spaces()
                print(self.currentToken.recognizedString)
                while self.currentToken.family is ADD_OP:
                    print("Found add op", self.currentToken.recognizedString)
                    self.nextToken()  # consume add op
                    if not self.term(): return False
                print("Found expression")
                return True
        return False
        # 1+1

    def term(self):
        print("Checking for term")
        self.consume_white_spaces()
        if self.factor():
            self.consume_white_spaces()
            while self.currentToken.family is MUL_OP:
                print("Found mul op", self.currentToken.recognizedString)
                self.nextToken()  # consume mul op
                if not self.factor(): return False
            print("Found term")
            return True
        else:
            return False

    def factor(self):
        print("Checking for factor")
        if self.currentToken.family is NUM:
            print("Read factor ", self.currentToken.recognizedString)
            self.nextToken()  # consume number
            return True
        elif self.currentToken.family is ID_KW:
            self.nextToken()  # consume ID
            if self.currentToken.recognizedString == '(':
                self.nextToken()  # consume (
                print("Found function factor")
                if self.expression():
                    if self.currentToken.recognizedString == ')':
                        self.nextToken()
                        return True
                    else:
                        self.error("Missing closing parenthesis", self.currentToken)
                        return False
            else:
                print("Read factor ", self.tokenList[self.tokenIndex - 1].recognizedString)
                print("Current token ", self.currentToken.family)
                return True
        elif self.currentToken.family is GRP_SMBL:
            self.nextToken()  # consume (
            
        return False

    def idtail(self):
        print("Checking for idtail")
        self.actualParList()

    def optionalSign(self):
        print("Checking for sign")
        self.consume_white_spaces()
        if self.currentToken.recognizedString in ['+',
                                                  '-'] or self.currentToken.family is NUM or self.currentToken.family is ID_KW:
            print("Found sign")
            if self.currentToken.recognizedString in ['+', '-']: self.nextToken()
            return True
        print("No sign found")
        return False

    def actualParList(self):
        print("Checking for par list")
        self.actualparitem()
        while self.currentToken.recognizedString == ',':
            self.nextToken()
            self.actualparitem()

    def actualParItem(self):
        print("Checking for act par list")
        self.expression()

    def analyze(self):
        self.program()
        print("Finished syntax analysis")

    def consume_new_line(self):
        while self.currentToken.family is NL:
            self.nextToken()

    def commentStat(self):
        print("Checking for comment")
        self.nextToken()  # consume ##
        while self.nextToken():
            if self.currentToken.family is COMMENT:
                print("Found comment")
                self.nextToken()  # consume ending ##
                return True
            elif self.currentToken.family is NL:
                self.error("Missing closing comment", self.currentToken)
                return False

    def mainPart(self):
        self.skip_spaces_and_nl()
        if self.currentToken.recognizedString == '#def':
            self.nextToken() # consume def
            if self.currentToken.family is WHITE_SPACE:
                self.nextToken()
                if self.currentToken.recognizedString == 'main':
                    self.nextToken()
                    self.consume_white_spaces()
                    if self.currentToken.family is NL:
                        self.skip_spaces_and_nl()
                        self.declarations()
                        self.blockstatements()
                        print("Found main function")
                        return True
                    else:
                        self.error("Missing new line after main", self.currentToken)
                else:
                    self.error("Missing main function", self.currentToken)
            else:
                self.error("Missing white space after def", self.currentToken)
        return False

    def hasTokens(self):
        return self.tokenIndex < len(self.tokenList)


# lex = Lex(r'C:\Users\GiannisB\Desktop\Metafrastes\test.cpy')
lex = Lex(r'C:\Users\GiannisB\Desktop\Metafrastes\tests\declaration.cpy')
lex.readFile()

if not lex.errors:
    parser = Parser(lex.tokenList)
