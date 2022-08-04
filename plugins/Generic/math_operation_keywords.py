#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      prudhvi.gujjuboyina
#
# Created:     24-10-2016
# Copyright:   (c) prudhvi.gujjuboyina 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------


from pyparsing import (Literal,CaselessLiteral,Word,Combine,Group,Optional,
                       ZeroOrMore,Forward,nums,alphas,oneOf)
import math
import operator

import logger
from constants import *

import logging


log = logging.getLogger('math_operation_keywords.py')

class NumericStringParser(object):
    '''
    Most of this code comes from the fourFn.py pyparsing example

    '''
    def pushFirst(self, strg, loc, toks ):
        self.exprStack.append( toks[0] )
    def pushUMinus(self, strg, loc, toks ):
        if toks and toks[0]=='-':
            self.exprStack.append( 'unary -' )
    def __init__(self):
        """
        expop   :: '^'
        multop  :: '*' | '/'
        addop   :: '+' | '-'
        integer :: ['+' | '-'] '0'..'9'+
        atom    :: PI | E | real | fn '(' expr ')' | '(' expr ')'
        factor  :: atom [ expop factor ]*
        term    :: factor [ multop factor ]*
        expr    :: term [ addop term ]*
        """
        point = Literal( "." )
        e     = CaselessLiteral( "E" )
        fnumber = Combine( Word( "+-"+nums, nums ) +
                           Optional( point + Optional( Word( nums ) ) ) +
                           Optional( e + Word( "+-"+nums, nums ) ) )
        ident = Word(alphas, alphas+nums+"_$")
        plus  = Literal( "+" )
        minus = Literal( "-" )
        mult  = Literal( "*" )
        div   = Literal( "/" )
        lpar  = Literal( "(" ).suppress()
        rpar  = Literal( ")" ).suppress()
        addop  = plus | minus
        multop = mult | div
        expop = Literal( "^" )
        pi    = CaselessLiteral( "PI" )
        expr = Forward()
        atom = ((Optional(oneOf("- +")) +
                 (pi|e|fnumber|ident+lpar+expr+rpar).setParseAction(self.pushFirst))
                | Optional(oneOf("- +")) + Group(lpar+expr+rpar)
                ).setParseAction(self.pushUMinus)
        # by defining exponentiation as "atom [ ^ factor ]..." instead of
        # "atom [ ^ atom ]...", we get right-to-left exponents, instead of left-to-right
        # that is, 2^3^2 = 2^(3^2), not (2^3)^2.
        factor = Forward()
        factor << atom + ZeroOrMore( ( expop + factor ).setParseAction( self.pushFirst ) )
        term = factor + ZeroOrMore( ( multop + factor ).setParseAction( self.pushFirst ) )
        expr << term + ZeroOrMore( ( addop + term ).setParseAction( self.pushFirst ) )
        # addop_term = ( addop + term ).setParseAction( self.pushFirst )
        # general_term = term + ZeroOrMore( addop_term ) | OneOrMore( addop_term)
        # expr <<  general_term
        self.bnf = expr
        # map operator symbols to corresponding arithmetic operations
        epsilon = 1e-12
        self.opn = { "+" : operator.add,
                "-" : operator.sub,
                "*" : operator.mul,
                "/" : operator.truediv,
                "^" : operator.pow }
        self.fn  = { "sin" : math.sin,
                "cos" : math.cos,
                "tan" : math.tan,
                "abs" : abs,
                "trunc" : lambda a: int(a),
                "round" : round,
                "sgn" : lambda a: abs(a)>epsilon and cmp(a,0) or 0}

    def evaluateStack(self, s ):
        op = s.pop()
        if op == 'unary -':
            return -self.evaluateStack( s )
        if op in "+-*/^":
            op2 = self.evaluateStack( s )
            op1 = self.evaluateStack( s )
            return self.opn[op]( op1, op2 )
        elif op == "PI":
            return math.pi # 3.1415926535
        elif op == "E":
            return math.e  # 2.718281828
        elif op in self.fn:
            return self.fn[op]( self.evaluateStack( s ) )
        elif op[0].isalpha():
            return 0
        else:
            if '.' in op:
                opt=op.split('.')
                opi=int(opt[0])
                opd=float('0.'+opt[1])
                op=opi+opd
                return op
            else:
                return int(op)

    def eval(self,num_string,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=None
        err_msg=None
        self.exprStack=[]
        parseAll=True
        try:
            if len(args)>1 and args[1] is not None:
                logger.print_on_console('Input expression is',args[1],'\n')
            else:
                logger.print_on_console('Input expression is',num_string,'\n')
            if args[0] is not None:
                errs=args[0].split('\n')
                for err in errs:
                    logger.print_on_console(err+'\n')
                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
            elif not (num_string is None or num_string is ''):
                log.debug('Parsing the expression')
                #logger.print_on_console('Parsing the expression')
                results=self.bnf.parseString(num_string,parseAll)
                log.debug('Evaluating the expression')
                #logger.print_on_console('Evaluating the expression')
                output=self.evaluateStack( self.exprStack[:] )
                if isinstance(output,float):
                    if output % 1 == 0.0:
                        output = int(output)
                    output=round(output,2)
                elif isinstance(output,int):
                    output=str(output)
                log.debug('Got the result : %s', output)
                #logger.print_on_console('Got the result : ', output)
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE
            else:
                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
        except Exception as e:
            log.error(e)
            err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
        if err_msg!=None:
            logger.print_on_console(err_msg)
        return status,methodoutput,output,err_msg


    def currencyConverter(self, num_string, *args):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        output=None
        err_msg=None
        try:
            if len(args)>1 and args[1] is not None:
                logger.print_on_console('Input expression is',args[1],'\n')
            else:
                logger.print_on_console('Input expression is',num_string,'\n')
            if len(args)>0 and args[0] is not None:
                errs=args[0].split('\n')
                for err in errs:
                    logger.print_on_console(err+'\n')
                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
            elif not (num_string is None or num_string is ''):
                log.debug('Converting the variable value')
                # logger.print_on_console('Converting the currency')
                output = "{:,.2f}".format(float(num_string))
                if isinstance(output,float):
                    if output % 1 == 0.0:
                        output = str(output)
                    output=round(output,2)
                elif isinstance(output,int):
                    output=str(output)
                log.debug('Got the result : %s', output)
                # logger.print_on_console('Got the result : ', output)
                status = TEST_RESULT_PASS
                methodoutput = TEST_RESULT_TRUE
            else:
                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
        except Exception as e:
            log.error(e)
            err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
        if err_msg!=None:
            logger.print_on_console(err_msg)
        return status,methodoutput,output,err_msg
