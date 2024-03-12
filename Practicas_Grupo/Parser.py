# coding: utf-8

from Lexer import CoolLexer
from sly import Parser
import sys
import os
from Clases import *


class CoolParser(Parser):
    nombre_fichero = ''
    tokens = CoolLexer.tokens
    debugfile = "salida.out"
    errores = []

    @_("Clase") #clase
    def Programa(self, p):

        return Programa(secuencia=[p.Clase])

    @_("Programa Clase") #subprograma u otra clase
    def Programa(self, p):
        
        return Programa(secuencia=p.Programa.secuencia + [p.clase])

    @_("CLASS TYPEID opcional '{' lista_atr_metodos '}'") #subprograma u otra clase
    def Clase(self, p):
        return Clase(nombre=p[1], padre = p[2], caracteristica = p[4])



    @_("'{' bloque '}'")
    def expresion(self, p):
        pass

    @_("expresion ';'")
    def bloque(self, p):
        pass


    @_("bloque expresion ';'")
    def bloque(self, p):
        pass


    @_("eror ';'")
    def bloque(self, p):
        pass

   
    def error(self, p):
        pass


    @_("")
    def opcionalPadre(self, p):
    
        return "Object"
    @_("INHERITS TYPEID ")
    def opcionalPadre(self, p):
        return p[1]


    @_("")
    def list_atr_metodos(self, p):
        pass

    @_("Atributo lista_atr_metodos ")
    def list_atr_metodos(self, p):
        pass

    @_("Metodo lista_atr_metodos ")
    def list_atr_metodos(self, p):
        pass


    @_("OBJECTID ':' TYPEID opcional_expr")
    def Atributos(self, p):
        pass
        



