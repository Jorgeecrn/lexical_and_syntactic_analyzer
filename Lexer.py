# coding: utf-8

from sly import Lexer
import os
import re
import sys





class CoolLexer(Lexer):
    tokens = {OBJECTID, INT_CONST, BOOL_CONST, TYPEID,
              ELSE, IF, FI, THEN, NOT, IN, CASE, ESAC, CLASS,
              INHERITS, ISVOID, LET, LOOP, NEW, OF,
              POOL, THEN, WHILE, NUMBER, STR_CONST, LE, DARROW, ASSIGN, ERROR}
    #ignore = '\t '
    literals = {';'}

    #al else true
    ELSE = r'\b[eE][lL][sS][eE]\b'
    
    @_(r'\b[t][rR][uU][eE]\b')
    def BOOL_CONST(self, t):
        t.type = 'BOOL_CONST'
        return t

    @_(r'\b[T][rR][uU][eE]\b')
    def TYPEID(self, t):
        t.type = 'TYPEID'
        return t

    #BAD KEYWORDS

    #TIPO False
    @_(r'\b[F][aA][lL][sS][eE]\b')
    def type_false(self, t):
        t.type = 'TYPEID'
        return t

    #TIPO CASE
    @_(r'\b[Cc][aA][sS][eE]\b')
    def CASE(self, t):
        t.type='CASE'
        return t

    #TIPO ESAC
    @_(r'\b[Ee][Ss][Aa][Cc]\b')
    def ESAC(self, t):
        t.type='ESAC'
        return t

    #TIPO LOOP
    @_(r'\b[Ll][oO][oO][pP]\b')
    def LOOP(self, t):
        t.type='LOOP'
        return t

    #tipo THEN
    @_(r'\b[Tt][Hh][Ee][Nn]\b')
    def THEN(self, t):
        t.type='THEN'
        return t

    #TIPO OBJECTID
    @_(r'\b[a-z][a-zA-Z0-9_]*\b')
    def OBJECTID(self, t):
        t.type= 'OBJECTID'
        return t

    #TIPO Oid
    @_(r'\b[O][iI][dD]\b')
    def Oid_type(self, t):
        t.type= 'TYPEID'
        return t

    #TIPO LOOPNEW
    @_(r'\b[L][oO][oO][pP][nN][eE][wW]\b')
    def Loopnew_typeid(self, t):
        t.type= 'TYPEID'
        return t


    CARACTERES_CONTROL = [bytes.fromhex(i+hex(j)[-1]).decode('ascii')
                          for i in ['0', '1']
                          for j in range(16)] + [bytes.fromhex(hex(127)[-2:]).decode("ascii")]

    @_(r'\t| |\v|\r|\f')
    def spaces(self, t):
        pass

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    
    def error(self, t):
        self.index += 1

    def salida(self, texto):
        lexer = CoolLexer()
        list_strings = []
        for token in lexer.tokenize(texto):
            result = f'#{token.lineno} {token.type} '
            if token.type == 'OBJECTID':
                result += f"{token.value}"
            elif token.type == 'BOOL_CONST':
                result += "true" if token.value else "false"
            elif token.type == 'TYPEID':
                result += f"{str(token.value)}"
            elif token.type in self.literals:
                result = f'#{token.lineno} \'{token.type}\' '
            elif token.type == 'STR_CONST':
                result += token.value
            elif token.type == 'INT_CONST':
                result += str(token.value)
            elif token.type == 'ERROR':
                result = f'#{token.lineno} {token.type} {token.value}'
            else:
                result = f'#{token.lineno} {token.type}'
            list_strings.append(result)
        return list_strings


    