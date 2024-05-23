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
RESERVED = 'reserved'
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
            for index, token in enumerate(self.tokenList):
                if token.recognizedString in reserved_words:
                    self.tokenList[index] = Token(RESERVED, token.recognizedString, token.lineNumber)

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

        if self.token.recognizedString == '/' and token != '/':
            self.error(self.token, "missing '/' before '" + token + "'")

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
        self.last_temp = "T_0"
        self.looking_for_param = None
        self.tokenList = tokenList
        self.currentToken = tokenList[0]
        self.tokenIndex = 0
        self.numberOfPrograms = 0
        self.generated_program = QuadList()
        print("Started syntax analysis")
        self.temp_counter = 0
        self.symbolTable = Table()
        self.analyze()

    def newTemp(self):
        self.temp_counter += 1
        self.last_temp = "T_" + str(self.temp_counter)
        return self.last_temp

    def error(self, error_message, token):
        print("\033[91m Error: \033[0m", error_message, " at line " + str(token.lineNumber))
        sys.exit()

    def nextToken(self):
        if self.tokenIndex >= len(self.tokenList) - 1:
            print("Finished Syntax analysis")
            # sys.exit()  # goofy ahh
            raise Exception("Run out of tokens")
            return False
        self.tokenIndex += 1
        self.currentToken = self.tokenList[self.tokenIndex]
        return True

    def program(self):
        while self.hasTokens():
            self.block()

    def block(self):
        res = False

        self.skip_spaces_and_nl()
        if self.currentToken.recognizedString == '#}':
            self.nextToken()  # consume } lol
            return True

        while self.currentToken.recognizedString != '#}' and self.hasTokens():
            if self.declarations():
                res = True
                print("Finished declarations")

            self.skip_spaces_and_nl()
            if self.subprograms():
                res = True
                print("Finished subprograms")

            self.skip_spaces_and_nl()
            if self.blockstatements():
                res = True
                print("Finished blockstatemets")

            if self.mainPart():
                res = True
                print("Finished main")

            if res: print("Found block", self.currentToken.recognizedString)

        return res

    def declarations(self):
        print("Looking for declarations")
        self.skip_spaces_and_nl()
        if self.declaration():
            self.skip_spaces_and_nl()
            return True
        return False

    def declaration(self):
        print("Looking for declaration")
        self.consume_white_spaces()
        self.consume_new_line()
        if self.currentToken.recognizedString in ['#int', 'global']:
            print("Checking declaration", self.currentToken.recognizedString)
            if self.varlist():
                return True
            else:
                self.error("Missing variable name near declaration", self.currentToken)
        print('Didnt find any declarations')
        return False

    def varlist(self):
        print("In varlist")
        self.nextToken()  # consume #decl
        if self.currentToken.family is not WHITE_SPACE:
            self.error("Syntax error near variable declaration, missing white space", self.currentToken)
        self.consume_white_spaces()
        if self.currentToken.family is RESERVED:
            self.error("Syntax error near variable declaration, " + self.currentToken.recognizedString +
                       " is a reserved word", self.currentToken)
        if self.currentToken.family is not ID_KW:
            print("NO variables found")
            self.error("Syntax error near variable declaration, missing variable name", self.currentToken)
            return False
        while self.currentToken.family is ID_KW:
            self.symbolTable.getCurrentScope().addEntity(
                Variable(self.currentToken.recognizedString, "int", self.symbolTable.getCurrentScope().offset))
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
            return True
        print("Didnt find any subprograms")
        return False

    def subprogram(self):

        print(self.currentToken)
        self.numberOfPrograms = self.numberOfPrograms + 1
        print("NUmber of programs:", self.numberOfPrograms)
        print("Looking for subprogram")
        self.skip_spaces_and_nl()
        if self.currentToken.recognizedString == 'def':

            self.nextToken()
            if self.currentToken.family is WHITE_SPACE:
                self.nextToken()
                if self.currentToken.family is ID_KW:
                    self.symbolTable.getCurrentScope().addEntity(
                        Function(self.currentToken.recognizedString, self.generated_program.quad_counter,
                                 "frame length", "int")
                    )
                    self.symbolTable.newScope()
                    block_name = self.currentToken.recognizedString
                    self.generated_program.genQuad("begin_block", block_name, "_", "_")
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
                                            self.generated_program.genQuad("end_block", block_name, "_", "_")
                                            self.symbolTable.gotoPreviousScope()

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
                            print(self.currentToken)
                            self.error("Syntax error near function parameters, missing ':'", self.currentToken)
                    else:
                        self.error("Syntax error, missing parameters", self.currentToken)
                else:
                    if self.currentToken.family is RESERVED:
                        self.error(
                            "Syntax error near function name, " + self.currentToken.recognizedString + " is a reserved word",
                            self.currentToken)
                    else:
                        self.error("Syntax error near function name", self.currentToken)
            else:
                self.error("Syntax error near 'def' declaration", self.currentToken)
        return False

    def formalparlist(self):
        print("Reading char:", self.currentToken.recognizedString)
        if self.currentToken.recognizedString == '(':
            self.nextToken()  # consume (
            self.consume_white_spaces()
            if self.formalparitem():
                self.consume_white_spaces()
                print("Checking par list")
                while self.currentToken.recognizedString == ',':
                    self.nextToken()  # consume comma
                    self.consume_white_spaces()
                    if self.formalparitem():
                        pass
                    else:
                        self.error("Syntax error near formal parameter", self.currentToken)
                    self.consume_white_spaces()
                print("Reading char:", self.currentToken.recognizedString)
            if self.currentToken.recognizedString == ')':
                self.nextToken()  # consume )
            else:
                self.error("Missing closing parenthesis", self.currentToken)
            print("Finished par list")
        else:
            self.error("Missing opening parenthesis", self.currentToken)
        return True

    def formalparitem(self):
        if self.currentToken.family is ID_KW:
            self.symbolTable.getCurrentScope().addEntity(
                FormalParameter(self.currentToken.recognizedString, "int", "CV")
            )
            self.nextToken()  # consume ID
            return True
        return False

    def statements(self):
        print("Looking for statements")
        if self.statement():
            while self.statement():
                pass
            print('Found statements')
            return True
        return False

    def blockstatements(self):
        print("Looking for blockstatements with token:", self.currentToken)
        print(self.currentToken)
        if self.statements():
            return True
        print("Didnt find any blockstatements")
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
        elif self.currentToken.recognizedString == "print":
            return self.printStat()
        elif self.currentToken.recognizedString == 'int':
            return self.inputStat()
        elif self.currentToken.family is COMMENT:
            return self.commentStat()
        elif self.currentToken.family is ID_KW and self.currentToken.recognizedString not in reserved_words:
            return self.assignStat()

        return False

    def assignStat(self):
        print("Checking for assignment")
        id = self.currentToken.recognizedString
        self.nextToken()  # consume ID
        self.consume_white_spaces()
        if self.currentToken.recognizedString == '=':
            self.nextToken()  # consume =
            self.consume_white_spaces()

            start_index = self.tokenIndex
            if self.inputStat():
                self.generated_program.genQuad("par", self.newTemp(), "RET", "_")
                self.generated_program.genQuad("call", "input", "_", "_")
                self.generated_program.genQuad(":=", self.last_temp, "_", id)
                print('Found input assignment')
                return True
            elif self.expression():
                value = ''.join(token.recognizedString for token in self.tokenList[start_index:self.tokenIndex]).strip()
                if self.is_complex_token_between(start_index):
                    value = self.last_temp
                self.generated_program.genQuad(":=", value, "_", id)
                print("Found assignment", id, "=", self.currentToken.recognizedString)
                return True
            else:
                self.error("Missing expression after assignment", self.currentToken)
        else:
            self.error("Missing assignment operator", self.currentToken)
        return False

    def ifStat(self):
        print("Found if statement")
        self.symbolTable.newScope()
        self.nextToken()  # consume if
        if self.currentToken.family is WHITE_SPACE:  # there should be at least one space after if statement
            self.consume_white_spaces()  # consume the rest if any
            start_index = len(self.generated_program.programList)
            if self.condition():
                quads = self.generated_program.programList[start_index:self.generated_program.quad_counter]
                conds = [quads for quads in quads if
                         quads.op0 in ['<', '>', '==', '!=', '>=', '<='] and quads.op3 == '_']
                self.generated_program.backPatch(conds, self.generated_program.quad_counter)
                # Keep the jumps to backpatch them later
                jumps = [quads for quads in quads if quads.op0 == 'jump' and quads.op3 == '_']
                self.consume_white_spaces()
                if self.currentToken.recognizedString == ':':
                    self.nextToken()  # consume :
                    self.consume_white_spaces()
                    if self.currentToken.family is NL:
                        self.nextToken()  # consume new line
                        self.skip_spaces_and_nl()
                        if self.currentToken.recognizedString == '#{':
                            self.nextToken()
                            self.skip_spaces_and_nl()
                            self.block()
                        else:
                            self.statement()
                        # Backpatch the jumps of false conditions to the end of the block
                        self.generated_program.backPatch(jumps, self.generated_program.quad_counter + 1)

                        # FIXME
                        # Add am empty jump for the case that if condition was true
                        # Backpatch after else statement is done
                        self.generated_program.genQuad("jump", "_", "_", "_")
                        if_jump = [self.generated_program.getLastQuad()]

                        while self.elifStat():  # check for elif statements
                            self.skip_spaces_and_nl()

                        self.skip_spaces_and_nl()
                        self.elseStat()
                        self.generated_program.backPatch(if_jump, self.generated_program.quad_counter)
                        print("IF JUMP was backpatched to", self.generated_program.quad_counter)
                        self.symbolTable.gotoPreviousScope()
                        return True
                    else:
                        self.error("Missing new line after if", self.currentToken)
                else:
                    self.error("Missing ':' after if", self.currentToken)
        else:
            self.error("Syntax error near 'if' statement", self.currentToken)

    def elifStat(self):
        print("Checking for elif statement")
        print(self.currentToken)
        self.skip_spaces_and_nl()  # hihi
        if self.currentToken.recognizedString == 'elif':
            self.nextToken()  # consume elif
            self.symbolTable.newScope()
            print("Found elif statement")
            self.consume_white_spaces()
            # Same logic with if statement
            start_index = len(self.generated_program.programList)
            if self.condition():
                quads = self.generated_program.programList[start_index:self.generated_program.quad_counter]
                conds = [quads for quads in quads if
                         quads.op0 in ['<', '>', '==', '!=', '>=', '<='] and quads.op3 == '_']
                self.generated_program.backPatch(conds, self.generated_program.quad_counter)
                # Keep the jumps to backpatch them later
                jumps = [quads for quads in quads if quads.op0 == 'jump']
                self.consume_white_spaces()
                if self.currentToken.recognizedString == ':':
                    self.nextToken()
                    self.consume_white_spaces()
                    if self.currentToken.family is NL:
                        self.nextToken()  # consume new line
                        self.skip_spaces_and_nl()
                        if self.currentToken.recognizedString == '#{':
                            self.nextToken()
                            self.skip_spaces_and_nl()
                            self.block()
                        else:
                            self.statement()

                        # Backpatch the jumps of false conditions to the end of the block
                        self.generated_program.backPatch(jumps, self.generated_program.quad_counter)
                        self.symbolTable.gotoPreviousScope()
                        return True
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
            self.symbolTable.newScope()

            print("Found else statement")
            self.nextToken()  # consume else
            self.consume_white_spaces()
            if self.currentToken.recognizedString == ':':
                self.nextToken()  # consume :
                self.consume_white_spaces()
                if self.currentToken.family is NL:
                    self.nextToken()
                    self.skip_spaces_and_nl()
                    if self.currentToken.recognizedString == '#{':
                        self.nextToken()  # consume {
                        self.skip_spaces_and_nl()
                        self.block()
                    else:
                        self.statement()
                    self.symbolTable.gotoPreviousScope()
                    return True
                else:
                    self.error("Missing new line after else", self.currentToken)
            else:
                self.error("Missing ':' after else", self.currentToken)
        return False

    def skip_spaces_and_nl(self):
        while self.currentToken.family is WHITE_SPACE or self.currentToken.family is NL:
            self.nextToken()

    def whileStat(self):
        self.symbolTable.newScope()
        print("Found while")
        print(self.currentToken)
        self.nextToken()  # consume while
        if self.currentToken.family is WHITE_SPACE:
            self.consume_white_spaces()
            # get tokens of condition
            start_index = len(self.generated_program.programList)
            if self.condition():
                print("Found while condition")
                # Those are the condition quads
                quads = self.generated_program.programList[start_index:self.generated_program.quad_counter]
                # Backpatch the true values to get into the block
                conds = [quads for quads in quads if
                         quads.op0 in ['<', '>', '==', '!=', '>=', '<='] and quads.op3 == '_']
                self.generated_program.backPatch(conds, self.generated_program.quad_counter)

                # Keep the jumps to backpatch them later
                jumps = [quads for quads in quads if quads.op0 == 'jump']

                self.consume_white_spaces()
                if self.currentToken.recognizedString == ':':
                    self.nextToken()  # consume :
                    if self.currentToken.family is NL:
                        self.nextToken()  # consume new line
                        self.skip_spaces_and_nl()
                        if self.currentToken.recognizedString == '#{':
                            self.nextToken()  # consume {
                            self.skip_spaces_and_nl()
                            if self.block():
                                self.skip_spaces_and_nl()
                                if self.currentToken.recognizedString == '#}':
                                    # Add jump to the beginning of the block
                                    self.generated_program.genQuad("jump", "_", "_", str(quads[0].label))
                                    # Backpatch the jumps of false conditions to the end of the block
                                    self.generated_program.backPatch(jumps, self.generated_program.quad_counter)
                                    self.nextToken()
                                    self.symbolTable.gotoPreviousScope()
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
        self.consume_white_spaces()
        if self.expression():
            self.symbolTable.getCurrentScope().addEntity(
                Variable("return_var", "int", "offset")
            )
            name_of_var_to_return = self.tokenList[self.tokenIndex - 1].recognizedString
            self.generated_program.genQuad("ret", name_of_var_to_return, "_", "_")
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
        print("Checking act par list")
        self.looking_for_param = True
        start_index = self.tokenIndex
        if self.actualparitem():
            item1 = self.tokens_between(start_index)
            if self.is_complex_token_between(start_index):  # case of simple factor
                item1 = self.last_temp
            self.generated_program.genQuad("par", item1, "CV", "_")
            while self.currentToken.recognizedString == ',':
                print("Found comma, checking for next param")
                self.nextToken()
                start_index = self.tokenIndex
                if self.actualparitem():
                    self.consume_white_spaces()
                    item2 = self.tokens_between(start_index)
                    if self.is_complex_token_between(start_index):
                        item2 = self.last_temp
                    self.generated_program.genQuad("par", item2, "CV", "_")
                else:
                    self.error("Missing actual parameter", self.currentToken)
        self.looking_for_param = False
        return True

    def actualparitem(self):
        print("Checking for act param item")
        if self.expression():
            print("Found expression parameter")
            return True

        # TODO
        # REMOVE DEAD ASS CODE
        elif self.currentToken.family is ID_KW:
            self.generated_program.genQuad("par", self.currentToken.recognizedString, "CV", "_")
            print("Found actual parameter", self.currentToken.recognizedString)
            self.nextToken()  # consume id
            return True
        return False

    def condition(self):
        print("Checking for condition")
        self.consume_white_spaces()
        quad_list = []
        if self.boolTerm():
            print("Found condition")
            while self.currentToken.recognizedString == 'or':
                quad_list.append(self.generated_program.getLastQuad())
                self.generated_program.backPatch([self.generated_program.getLastQuad()],
                                                 self.generated_program.quad_counter)
                self.nextToken()  # consume or
                if not self.boolTerm():
                    self.error("Missing bool term", self.currentToken)
                    return False

            print("Returned condition")

            return True
        return False

    def boolTerm(self):
        print("Checking for bool term")
        self.consume_white_spaces()
        quad_list = []
        if self.boolFactor():
            print("Found bool term")
            self.consume_white_spaces()
            while self.currentToken.recognizedString == 'and':
                self.generated_program.backPatch([self.generated_program.getSecondLastQuad()],
                                                 self.generated_program.quad_counter)
                self.nextToken()  # consume and
                self.consume_white_spaces()
                quad_list.append(self.generated_program.getLastQuad())
                if not self.boolFactor():
                    self.error("Missing bool factor", self.currentToken)
                    return False

            print("Returned boolTerm")
            return True
        return False

    def boolFactor(self):
        print("Checking for bool factor")
        self.consume_white_spaces()
        start_index = self.tokenIndex
        if self.expression():
            expression1 = self.tokens_between(start_index)
            print("Found expression", expression1)
            if self.is_complex_token_between(start_index):
                print("Found complex expression", expression1)
                expression1 = self.last_temp
            self.consume_white_spaces()
            if self.currentToken.family is REL_OP:
                rel_op = self.currentToken.recognizedString
                self.nextToken()  # consume rel op
                self.consume_white_spaces()
                start_index = self.tokenIndex
                if self.expression():
                    expression2 = self.tokens_between(start_index)
                    self.consume_white_spaces()
                    if self.is_complex_token_between(start_index):
                        print("Found complex expression", expression2)
                        expression2 = self.last_temp
                    self.generated_program.genQuad(rel_op, expression1, expression2, "_")
                    self.generated_program.genQuad("jump", "_", "_", "_")
                    return True
                else:
                    self.error("Missing expression after relational operator", self.currentToken)

        elif self.currentToken.recognizedString == 'not':
            self.nextToken()  # consume not
            if self.condition():
                print("boolfactor found condition")
                return True
            else:
                self.error("Missing condition after not", self.currentToken)
        elif self.condition():
            print("boolfactor found condition")
            return True
        print("Didnt find bool factor")
        return False

    def expression(self):
        print("Checking for expression")
        print(self.currentToken.recognizedString)
        if self.optionalSign():
            current_list_index = self.tokenIndex
            if self.term():
                term1 = self.tokens_between(current_list_index)
                if self.is_complex_token_between(current_list_index):  # case of simple factor
                    term1 = self.last_temp
                self.consume_white_spaces()
                print(self.currentToken.recognizedString)
                while self.currentToken.family is ADD_OP:
                    operator = self.currentToken.recognizedString
                    print("Found add op", self.currentToken.recognizedString)
                    self.nextToken()  # consume add op
                    self.consume_white_spaces()
                    current_list_index = self.tokenIndex
                    if not self.term():
                        self.error("Missing term after add operator", self.currentToken)
                        return False
                    term2 = self.tokens_between(current_list_index)
                    if self.is_complex_token_between(current_list_index):
                        term2 = self.last_temp
                    self.generated_program.genQuad(operator, term1, term2, self.newTemp())
                print("Found expression")
                return True
        else:
            if self.term():
                self.consume_white_spaces()
                print(self.currentToken.recognizedString)
                while self.currentToken.family is ADD_OP:
                    print("Found add op", self.currentToken.recognizedString)
                    self.nextToken()  # consume add op
                    if not self.term():
                        self.error("Missing term after add operator", self.currentToken)
                        return False
                print("Found expression")
                return True
        return False

    def tokens_between(self, current_list_index):
        # return [token for token in self.tokenList[current_list_index,self.currentToken] if token.family is not 'WHITE_SPACE']

        return (''.join(
            token.recognizedString for token in self.tokenList[current_list_index:self.tokenIndex] if
            token.family is not WHITE_SPACE)
                .strip())

    def term(self):
        print("Checking for term")
        self.consume_white_spaces()
        start_index = self.tokenIndex
        if self.factor():
            factor1 = self.tokens_between(start_index)
            if self.is_complex_token_between(start_index):  # case of simple factor
                factor1 = self.last_temp
            self.consume_white_spaces()
            while self.currentToken.family is MUL_OP:
                operator = self.currentToken.recognizedString
                print("Found mul op", self.currentToken.recognizedString)
                self.nextToken()  # consume mul op
                self.consume_white_spaces()
                start_index = self.tokenIndex
                if not self.factor(): return False
                factor2 = self.tokens_between(start_index)
                if self.is_complex_token_between(start_index):  # case of simple factor:
                    factor2 = self.last_temp
                self.generated_program.genQuad(operator, factor1, factor2, self.newTemp())
            print("Found term")
            return True
        else:
            return False

    def is_complex_token_between(self, start_index):
        return sum(1 for token in self.tokenList[start_index:self.tokenIndex - 1] if token.family != 'WHITE_SPACE') > 1

    def factor(self):
        print("Checking for factor")
        self.consume_white_spaces()
        if self.currentToken.family is NUM:
            print("Read factor ", self.currentToken.recognizedString)
            self.nextToken()  # consume number
            return True
        elif self.currentToken.recognizedString == '(':
            self.nextToken()  # consume (
            if self.expression():
                if self.currentToken.recognizedString == ')':
                    self.nextToken()
                    return True
                else:
                    print(self.currentToken.recognizedString)
                    self.error("Missing closing parenthesis near factor", self.currentToken)
                    return False
        elif self.currentToken.family is ID_KW:
            lastId = self.currentToken.recognizedString
            self.nextToken()  # consume ID
            if self.idtail():
                self.generated_program.genQuad("par", self.newTemp(), "RET", "_")
                self.generated_program.genQuad("call", lastId, "_", "_")
            return True
        print("didnt find factor")
        return False

    def idtail(self):
        print("Checking for idtail")
        self.consume_white_spaces()
        if self.currentToken.recognizedString == '(':
            self.nextToken()
            self.consume_white_spaces()
            if self.actualparlist():
                if self.currentToken.recognizedString == ')':
                    self.nextToken()
                    return True
                else:
                    print(self.currentToken)
                    self.error("Missing closing parenthesis near id tail", self.currentToken)
            else:
                self.error("Missing actual parameters", self.currentToken)
        return False

    def optionalSign(self):
        print("Checking for optional sign")
        self.consume_white_spaces()
        if self.currentToken.recognizedString in ['+',
                                                  '-'] or self.currentToken.family is NUM or self.currentToken.family is ID_KW:
            print("Found optional sign")
            if self.currentToken.recognizedString in ['+', '-']: self.nextToken()
            return True
        print("No sign found")
        return False

    def analyze(self):
        try:
            self.program()
            print("Finished syntax analysis")
        except Exception as e:
            print("Finished syntax analysis")

    def consume_new_line(self):
        while self.currentToken.family is NL:
            self.nextToken()

    def commentStat(self):

        print("Checking for comment")
        self.nextToken()  # consume ##
        while self.currentToken.family is not COMMENT:
            if self.currentToken.family is NL:
                self.error("Missing closing comment", self.currentToken)
                return False
            else:
                self.nextToken()
        self.nextToken()  # cosnume ##
        return True

    def mainPart(self):
        self.skip_spaces_and_nl()
        if self.currentToken.recognizedString == '#def':
            self.nextToken()  # consume def
            if self.currentToken.family is WHITE_SPACE:
                self.nextToken()
                if self.currentToken.recognizedString == 'main':
                    self.symbolTable.getCurrentScope().addEntity(
                        Procedure("main", self.generated_program.quad_counter, "frameLength")
                    )
                    self.generated_program.genQuad("begin_block", "main", "_", "_")
                    #add jump at the very beginning of the program
                    self.generated_program.programList.insert(0, Quad(0, "jump", "_", "_", self.generated_program.programList[-1].label))
                    self.nextToken()
                    self.consume_white_spaces()
                    if self.currentToken.family is NL:
                        self.skip_spaces_and_nl()
                        self.declarations()
                        self.blockstatements()
                        print("\033[31m" + "Found main function" + "\033[0m")
                        self.generated_program.genQuad("halt", "_", "_", "_")
                        self.generated_program.genQuad("end_block", "main", "_", "_")
                        return True
                    else:
                        self.error("Missing new line after main", self.currentToken)
                else:
                    self.error("Missing main function", self.currentToken)
            else:
                self.error("Missing white space after def", self.currentToken)
        print("Didnt find main fun")
        return False

    def hasTokens(self):
        return self.tokenIndex < len(self.tokenList)


class QuadList:

    def __init__(self):
        self.programList = []
        self.quad_counter = 1

    def __str__(self):
        return "\n".join(str(quad) for quad in self.programList)

    def backPatch(self, list, target_label):
        for quad in list:
            quad.op3 = target_label

    def genQuad(self, op, op1, op2, op3):
        self.programList.append(Quad(self.quad_counter, op, op1, op2, op3))
        self.quad_counter += 1

    def nextQuad(self):
        return self.quad_counter + 1

    def getLastQuad(self):
        return self.programList[-1]

    def getSecondLastQuad(self):
        return self.programList[-2]


class QuadPointerList:
    def __init__(self):
        self.labelList = []

    def __str__(self):
        print(self.labelList)

    def mergeList(self, list1, list2):
        return list1 + list2  # Python moment


class QuadPointer:
    def __init__(self, label):
        self.label = label

    def __str__(self):
        print(self.label)


class Quad:
    def __init__(self, label, op0, op1, op2, op3):
        self.label = label
        self.op0 = op0
        self.op1 = op1
        self.op2 = op2
        self.op3 = op3
        print("Generated quad ", self)

    def __str__(self):
        return str(self.label) + ": " + str(self.op0) + ", " + str(self.op1) + ", " + str(self.op2) + ", " + str(
            self.op3)


### SYMBOL TABLE
class Entity:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Constant(Entity):
    def __init__(self, name, datatype, value):
        super().__init__(name)
        self.datatype = datatype
        self.value = value

    def __str__(self):
        return self.name + " " + self.datatype + " " + str(self.value)


class Variable(Entity):
    def __init__(self, name, datatype, offset):
        super().__init__(name)
        self.datatype = datatype
        self.offset = offset

    def __str__(self):
        return self.name + " " + self.datatype + " " + str(self.offset)


class FormalParameter(Entity):
    def __init__(self, name, datatype, mode):
        super().__init__(name)
        self.datatype = datatype
        self.mode = mode

    def __str__(self):
        return self.name + " " + self.datatype + " " + self.mode


class Parameter(Variable, FormalParameter):
    # Here Parameter uses the Variable super constructor
    def __init__(self, name, datatype, mode, offset):
        super().__init__(name, datatype, offset)
        self.mode = mode

    def __str__(self):
        return self.name + " " + self.datatype + " " + self.mode + " " + str(self.offset)


class Procedure(Entity):
    def __init__(self, name, startingQuad, frameLength):
        super().__init__(name)
        self.startingQuad = startingQuad
        self.frameLength = frameLength
        self.parameterList = []

    def __str__(self):
        return self.name + " " + str(self.startingQuad) + " " + str(self.frameLength)


class Function(Procedure):
    def __init__(self, name, startingQuad, frameLength, returnType):
        super().__init__(name, startingQuad, frameLength)
        self.returnType = returnType

    def __str__(self):
        return self.name + " " + str(self.startingQuad) + " " + str(self.frameLength) + " " + self.returnType


class Scope:
    def __init__(self, level, parent):
        self.level = level
        self.parent = parent
        self.entityList = []
        self.offset = 12

    def addEntity(self, entity):
        self.entityList.append(entity)
        if hasattr(entity, 'offset'):
            entity.offset = self.offset
            self.offset += 4


class Table:
    # TODO create methods
    def __init__(self):
        self.scopeList = []
        self.scopeList.append(Scope(0, None))
        self.currentScope = self.scopeList[0]

    def getCurrentScope(self):
        return self.currentScope

    def gotoPreviousScope(self):
        self.currentScope = self.currentScope.parent
        print("\033[32m ", "Went back to scope ", self.currentScope.level, "\033[0m ")

    def __str__(self):
        return "\n".join(
            str(scope.level) + " " + str(entity) for scope in self.scopeList for entity in scope.entityList)

    def addScope(self, scope):
        self.scopeList.append(scope)

    def removeScope(self, scope):
        self.scopeList.remove(scope)

    def updateEntity(self):
        pass

    def addFormalParameter(self, formalParameter):
        pass

    def searchEntity(self, entity):
        pass

    def newScope(self):
        self.addScope(Scope(len(self.scopeList), self.getCurrentScope()))
        print("\033[32m ", "Created scope", len(self.scopeList) - 1, "\033[0m")
        self.currentScope = self.scopeList[-1]


class Assembler:
    def __init__(self, quad_list, symbol_table):
        self.symbol_table = symbol_table
        self.quad_list = quad_list
        self.file = open('finalCode.asm', "w")

    def gnlvoce(self, variable_name):
        pass

    def loadvr(self, variable_name, register):
        pass

    def storerv(self, variable_name, register):
        pass

    def generate_final_code(self):
        for index, quad in enumerate(self.quad_list):
            self.file.write("L" + str(index) + ":\n")

            if quad.label == 0 and quad.op0 == "jump":
                self.file.write("   j Lmain\n\n")

            if quad.op0 == "end_block":
                self.file.write("   lw ra,(sp)\n")
                self.file.write("   jr ra\n\n")

            if quad.op0 == "begin_block" and quad.op1 != "main":
                self.file.write("   sw ra,(sp)\n\n")

            if quad.op1 == "main":
                self.file.write("Lmain:\n\n")


print("Enter the full path of the file to be compiled:")
# main part
lex = Lex(input())
lex.readFile()

if not lex.errors:
    lex.printTokenList()
    parser = Parser(lex.tokenList)
    print(parser.generated_program)
    print(parser.symbolTable)
    print(len(parser.symbolTable.scopeList))

    # create final code
    assembler = Assembler(parser.generated_program.programList, parser.symbolTable)
    assembler.generate_final_code()

    with open(lex.fileToRead.name.replace('.cpy', '') + '.int', 'w') as f:
        f.write(str(parser.generated_program))

    with open(lex.fileToRead.name.replace('.cpy', '') + '.sym', 'w') as f:
        f.write(str(parser.symbolTable))
