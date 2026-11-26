# coding: utf-8

from sly import Lexer
import os
import re
import sys


class CoolLexer(Lexer):
    tokens = {
        OBJECTID,
        INT_CONST,
        BOOL_CONST,
        TYPEID,
        ELSE,
        IF,
        FI,
        THEN,
        NOT,
        IN,
        CASE,
        ESAC,
        CLASS,
        INHERITS,
        ISVOID,
        LET,
        LOOP,
        NEW,
        OF,
        POOL,
        THEN,
        WHILE,
        NUMBER,
        STR_CONST,
        LE,
        DARROW,
        ASSIGN,
        ERROR,
    }
    # ignore = '\t '
    literals = {}
    # Ejemplo
    ELSE = r"\b[eE][lL][sS][eE]\b"


    CARACTERES_CONTROL = [
        bytes.fromhex(i + hex(j)[-1]).decode("ascii")
        for i in ["0", "1"]
        for j in range(16)
    ] + [bytes.fromhex(hex(127)[-2:]).decode("ascii")]

    @_(r"\t| |\v|\r|\f")
    def spaces(self, t):
        pass

    @_(r"\n+")
    def newline(self, t):
        self.lineno += t.value.count("\n")

    def error(self, t):
        self.index += 1

    def salida(self, texto):
        lexer = CoolLexer()
        list_strings = []
        for token in lexer.tokenize(texto):
            result = f"#{token.lineno} {token.type} "
            if token.type == "OBJECTID":
                result += f"{token.value}"
            elif token.type == "BOOL_CONST":
                result += "true" if token.value else "false"
            elif token.type == "TYPEID":
                result += f"{str(token.value)}"
            elif token.type in self.literals:
                result = f"#{token.lineno} '{token.type}' "
            elif token.type == "STR_CONST":
                result += token.value
            elif token.type == "INT_CONST":
                result += str(token.value)
            elif token.type == "ERROR":
                result = f"#{token.lineno} {token.type} {token.value}"
            else:
                result = f"#{token.lineno} {token.type}"
            list_strings.append(result)
        return list_strings

    # all_else_true #######################################
    @_(r"\b(t(?i:rue)|f(?i:alse))\b")
    def BOOL_CONST(self, t):
        t.value = t.value.lower() == 'true'
        return t

    @_(r"\b[T][rR][uU][eE]\b")
    def TYPEID(self, t):
        t.type = "TYPEID"
        return t
    #######################################################

    # keywords ############################################
    @_(r"\b[cC][aA][sS][eE]\b")
    def CASE(self, t):
        t.type = "CASE"
        return t

    @_(r"\b[cC][lL][aA][sS][sS]\b")
    def CLASS(self, t):
        t.type = "CLASS"
        return t

    @_(r"\b[eE][sS][aA][cC]\b")
    def ESAC(self, t):
        t.type = "ESAC"
        return t

    @_(r"\b[fF][iI]\b")
    def FI(self, t):
        t.type = "FI"
        return t

    @_(r"\b[iI][fF]\b")
    def IF(self, t):
        t.type = 'IF'
        return t

    @_(r'\b(?i:in)\b')
    def IN(self, t):
        t.type = 'IN'
        return t

    @_(r'\b(?i:inherits)\b')
    def INHERITS(self, t):
        t.type = 'INHERITS'
        return t

    @_(r'\b(?i:isvoid)\b')
    def ISVOID(self, t):
        t.type = 'ISVOID'
        return t

    @_(r'\b(?i:let)\b')
    def LET(self, t):
        t.type = 'LET'
        return t

    @_(r'\b(?i:loop)\b')
    def LOOP(self, t):
        t.type = 'LOOP'
        return t

    @_(r'\b(?i:new)\b')
    def NEW(self, t):
        t.type = 'NEW'
        return t

    @_(r'\b(?i:not)\b')
    def NOT(self, t):
        t.type = 'NOT'
        return t

    @_(r'\b(?i:of)\b')
    def OF(self, t):
        t.type = 'OF'
        return t

    @_(r'\b(?i:pool)\b')
    def POOL(self, t):
        t.type = 'POOL'
        return t

    @_(r'\b(?i:then)\b')
    def THEN(self, t):
        t.type = 'THEN'
        return t

    @_(r'\b(?i:while)\b')
    def WHILE(self, t):
        t.type = 'WHILE'
        return t
    #######################################################