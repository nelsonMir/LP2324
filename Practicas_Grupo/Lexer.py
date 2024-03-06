# coding: utf-8

from sly import Lexer

import os
import re
import sys





class CoolLexer(Lexer):
    tokens = {OBJECTID, INT_CONST, BOOL_CONST, TYPEID,
              ELSE, IF, FI, THEN, NOT, IN, CASE, ESAC, CLASS,
              INHERITS, ISVOID, LET, LOOP, NEW, OF,
              POOL, THEN, WHILE, NUMBER, STR_CONST, LE, DARROW, ASSIGN, IN, INT_CONST, COMMENTS}
    #ignore = "\t "
    literals = {}

    # Ejemplo
    INT_CONST = "[0-9]+"

    TYPEID = "^[A-Z][a-zA-Z0-9_]]*$"
    OBJECTID =  "^[a-z][a-zA-Z0-9_]*$"
    

    LE = r'<='
    DARROW = r'=<'
    ASSIGN = r'<-'
    IF = r'\b[iI][fF]\b'
    FI = r'\b[fF][iI]\b'
    THEN = r'\b[tT][hH][eE][nN]\b'
    NOT = r'\b[nN][oO][tT]\b'
    IN = r'\b[iI][nN]\b'
    CASE = r'\b[cC][aA][sS][eE]\b'
    ELSE = r'\b[eE][lL][sS][eE]\b'
    ESAC = r'\b[eE][sS][aA][cC]\b'
    CLASS = r'\b[cC][lL][aA][sS][sS]\b'
    INHERITS = r'\b[iI][nN][hH][eE][rR][iI][tT][sS]\b'
    ISVOID = r'\b[iI][sS][vV][oO][iI][dD]\b'
    LET = r'\b[lL][eE][tT]\b'
    LOOP = r'\b[lL][oO][oO][pP]\b'
    NEW = r'\b[nN][eE][wW]\b'
    OF = r'\b[oO][fF]\b'
    POOL = r'\b[pP][oO][oO][lL]\b'
    WHILE = r'\b[wW][hH][iI][lL][eE]\b'
   
    
    
    

    CARACTERES_CONTROL = [bytes.fromhex(i+hex(j)[-1]).decode('ascii')
                          for i in ['0', '1']
                          for j in range(16)] + [bytes.fromhex(hex(127)[-2:]).decode("ascii")]
    

    @_(r'[a-zA-Z]+')
    def PALABRAS(self, t):
        if t.value.lower() in ("true", "false") and t.value[0].islower():
            t.type = 'BOOL_CONST'
            t.value = True if t.value[0] == 't' else False
        else:
            t.type = "TYPEID" if t.value[0].isupper() else "OBJECTID"
        return t
  #  @_(r'[]')
   # def COMENTARIOS(self, t):
        #pass
    
    

    @_(r'"(?:\\.|[^\\"])*"')
    def STR_CONST(self, t):
        # Eliminar las comillas del token y escapar las secuencias especiales si es necesario
        value = t.value[1:-1]
        value = value.replace('\\"', '"')  # Eliminar escape de comillas
        value = value.replace('\\\\', '\\')  # Eliminar escape de barra invertida
        value = value.replace('\\b', '\b')  # Convertir escape de backspace a carácter
        value = value.replace('\\t', '\t')  # Convertir escape de tabulación a carácter
        value = value.replace('\\n', '\n')  # Convertir escape de nueva línea a carácter
        value = value.replace('\\r', '\r')  # Convertir escape de retorno de carro a carácter
        t.value = value
        return t
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
