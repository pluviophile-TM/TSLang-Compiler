from os import error
import ply.lex as lex
import ply.yacc as yacc

tokens = (
    'COMMENT',
    'LPAREN',
    'RPAREN',
    'LSQUAREBR',
    'RSQUAREBR',
    'QUESTIONMARK',
    'COLON',
    'SEMICOLON',
    'COMA',
    'EQUAL',
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'MOD',
    'LESS_THAN',
    'GREATER_THAN',
    'EQUALEQUAL',
    'NOT_EQUAL',
    'LESS_EQUAL',
    'GREATER_EQUAL',
    'OROR',
    'ANDAND',
    'NOT',
    'IDEN',
    'FUNCTION',
    'RETURNS',
    'RETURN' ,
    'END',
    'IF',
    'ELSE',
    'WHILE',
    'DO',
    'FOREACH',
    'OF',
    'INT',
    'ARRAY',
    'NIL',
    'VAL'
 )

line = 1
t_LPAREN= r'\('
t_RPAREN=r'\)'
t_LSQUAREBR=r'\['
t_RSQUAREBR=r'\]'
t_QUESTIONMARK=r'\?'
t_COLON=r'\:'
t_SEMICOLON=r'\;'
t_COMA=r'\,'
t_EQUAL=r'\='
t_PLUS = r'\+'
t_MINUS=r'\-'
t_TIMES=r'\*'
t_DIVIDE=r'\/'
t_MOD=r'%'
t_LESS_THAN=r'\<'
t_GREATER_THAN=r'>'
t_EQUALEQUAL=r'\=\='
t_NOT_EQUAL=r'\!\='
t_LESS_EQUAL=r'\<\='
t_GREATER_EQUAL=r'>='
t_ANDAND=r'\&\&'
t_OROR=r'\|\|'
t_NOT=r'\!'

def t_NUMBER(t):
    r'[0-9]+'
    t.value=int(t.value)
    return t

t_ignore=' \t' 

t_ignore_COMMENT = r'\-\-.*\n'

reserved = {
    'function' : 'FUNCTION',
    'returns' : 'RETURNS',
    'return' : 'RETURN' ,
    'end' : 'END',
    'if' : 'IF',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'do' : 'DO',
    'foreach' : 'FOREACH',
    'of' : 'OF',
    'Int' : 'INT',
    'Array' : 'ARRAY',
    'Nil' : 'NIL',
    'val' : 'VAL'
 }

def t_IDEN(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reserved.get(t.value,'IDEN')    # Check for reserved words
     return t
    
def t_error(t):
    print('LEXICAL ERORR AT Line : ',t.lexer.lineno+1)
    print(f'Illegal character {t.value[0]!r}')
    t.lexer.skip(1)



def t_newline(t):
     r'\n+'
     global line
     line +=1
     t.lexer.lineno += len(t.value)

lexer=lex.lex()
file = open("D:/Uni/Compiler/project/vsCode/parser-03/test.txt")
data = file.read()
file.close()
 # Give the lexer some input
lexer.input(data)
 
 # Tokenize
# while True:
#     tok = lexer.token()
#     if not tok: 
#         break      # No more input
#     print(tok)
class Table:
    paramList=[]
    def __init__(self, name, type,isFunc,paramNum):
        self.name = name
        self.type = type
        self.isFunc=isFunc
        self.paramNum=paramNum


funcNames = ['getInt','printInt','createArray','arrayLength','exit']
idenInfo={}
definedIden=[]
allIden=[]
returnType={}
curFunc=''
curRetType=''

# a
idenInfo['getInt']=Table('getInt','Int',True,0)
f=Table('printInt','Int',True,1)
f.paramList=['Int']
idenInfo['printInt']=f
f=Table('createArray','Array',True,1)
f.paramList=['Int']
idenInfo['createArray']=f
f=Table('arrayLength','Int',True,1)
f.paramList=['Array']
idenInfo['arrayLength']=f
f=Table('exit','Nil',True,1)
f.paramList=['Int']
idenInfo['exit']=f


 
def checkDefined(t,line):
    if t in allIden:
        if not t in definedIden:
            print('line',line,':',t,'is not defined!')
            return True
    return False

def newFCheck(t):
    if t in funcNames:
        print('function',t,'already exist!')
    else:
        funcNames.append(t)

def whatType(t):
    if isinstance(t, int):
        return 'Int'
    if t in definedIden:
        # print(idenInfo[t].type)
        return idenInfo[t].type

def p_prog(p):
    '''prog : func
            | func prog'''
    # print('prog')
    if len(p)==2:
        p[0]=p[1]
    else:
        p[0]=[p[1],p[2]]

def p_func(p):
    '''func : FUNCTION iden LPAREN flist RPAREN RETURNS type COLON body END'''
   
    newFCheck(p[2])

    f=Table(p[2],p[7],True,len(p[4]))
    f.paramList=[x[0] for x in p[4]]
    idenInfo[p[2]]=f
    definedIden.append(p[2])

    if p[7]!=curRetType:
        print('line',p.lineno(2),': return type at function',p[2],"don't match what it return")
    
    

    p[0]=[p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8],p[9],p[10]] #ke chi

def p_body(p):
    '''body : stmt
            | stmt body'''
    # print('body')

def p_stmt(p):
    '''stmt : expr SEMICOLON
            | defvar SEMICOLON
            | IF LPAREN expr RPAREN COLON stmt END
            | IF LPAREN expr RPAREN COLON stmt ELSE COLON stmt END
            | WHILE LPAREN expr RPAREN DO stmt
            | FOREACH LPAREN iden OF expr RPAREN stmt
            | RETURN expr SEMICOLON
            | COLON body END'''
    # print('stmt')
    if len(p)==3: #expr SEMICOLON | defvar SEMICOLON
        p[0]=p[1]
    if len(p)==4: # | RETURN expr SEMICOLON | COLON body END
        if p[1]=='return':
            p[0]=p[2]
            global curRetType
            curRetType=whatType(p[2])
            
        p[0]=p[2]
    if len(p)==7:
        p[0]=[p[1],p[2],p[3],p[4],p[5],p[6]]
    if len(p)==8:
        if p[1]=='if': #IF LPAREN expr RPAREN COLON stmt END
            if p[3]:
                p[0]=p[6]
        else: #FOREACH LPAREN iden OF expr RPAREN stmt
            definedIden.append(p[3])
            # print(p[3])
            p[0]=[p[1],p[2],p[3],p[4],p[5],p[6],p[7]]
            
def p_defvar(p):
    '''defvar : VAL type iden'''
    # print('defvar')
    p[0]=[p[2],p[3]] # ??
    definedIden.append(p[3])
    allIden.append(p[3])
    idenInfo[p[3]]=Table(p[3],p[2],False,0)

def p_expr(p):
    '''expr : iden LPAREN clist RPAREN  
            | expr LSQUAREBR expr RSQUAREBR
            | expr QUESTIONMARK expr COLON expr
            | expr EQUAL expr
            | expr PLUS expr
            | expr MINUS expr
            | expr TIMES expr
            | expr DIVIDE expr
            | expr MOD expr
            | expr LESS_THAN expr
            | expr GREATER_THAN expr
            | expr EQUALEQUAL expr
            | expr NOT_EQUAL expr
            | expr LESS_EQUAL expr
            | expr GREATER_EQUAL expr
            | expr OROR expr
            | expr ANDAND expr
            | NOT expr
            | MINUS expr
            | PLUS expr
            | LPAREN expr RPAREN
            | iden
            | number'''
    # print('exprlen',len(p))
    if len(p)==6: # expr QUESTIONMARK expr COLON expr
        if p[1]:
            p[0]=p[3]
        else:
            p[0]=p[5]
    if len(p)==5: 
        if p[2]=='(': #iden LPAREN clist RPAREN 
            if not p[1] in funcNames:
                print('line',p.lineno(1),': No such a function!')
            else:
                f=idenInfo[p[1]]
                if not f.paramNum ==len(p[3]):
                    x="line {} : function {} expects {} parameter but it's given {}"
                    print(x.format(p.lineno(1),p[1],idenInfo[p[1]].paramNum,len(p[3])))
                else:
                    l=idenInfo[p[1]].paramList
                    for i in range(len(p[3])):
                        if not whatType(p[3][i]) == l[i]:
                            
                            x="line {} : wrong type for argument {} of function {}!"
                            print(x.format(p.lineno(1),(i+1),p[1]))
                            print("\tit's given ",p[3][i],'of type',whatType(p[3][i]),'instead of',l[i])
                p[0]=p[1]
        #     p[0]=p[1] # ?? 
        # else : #expr LSQUAREBR expr RSQUAREBR
        #     p[0]=
   
    if len(p)==4:  # (expr) | expr sign expr 
        if p[1]=='(': # (expr)
            p[0]=p[2]
        else: # expr sign expr -> sign = {=,-,+,*,/,>,<,==,<=,>=,!=,||,&&}
            p[0]=[p[1],p[2],p[3]]
          
    if len(p)==3: #| NOT expr | MINUS expr | PLUS expr
        p[0]=[p[1],p[2]]

    if len(p)==2: # iden | number
        p[0]=p[1]
        if whatType(p[1])!='Int': #iden
            checkDefined(p[1],p.lineno(1))
            
def p_flist(p):
    '''flist :
            | type iden
            | type iden COMA flist'''
    if len(p)==1:
        p[0]=[]
    elif len(p)==3:
        definedIden.append(p[2])
        idenInfo[p[2]]=Table(p[2],p[1],False,0)
        p[0]=[(p[1],p[2])]
    else:
        definedIden.append(p[2])
        idenInfo[p[2]]=Table(p[2],p[1],False,0)
        p[0]=[(p[1],p[2])]+p[4]
    # print('flist',p[0])

def p_clist(p):
    '''clist :
            | expr
            | expr COMA clist'''
    
    if len(p)==1:
        p[0]=[]
    elif len(p)==2:
        p[0]=[p[1]]
       
    else:
        
        p[0]=[p[1]]+p[3]
    # print('clist',p[0])

def p_type(p):
    '''type : INT
            | ARRAY
            | NIL'''
    p[0]=p[1]
    # print('type',p[0])

def p_iden(p):
    """iden : IDEN"""
    p[0]=p[1]
    allIden.append(p[0])
    # print('iden',p[0])

def p_number(p):
    """number : NUMBER"""
    p[0]=p[1]
    # print('number',p[0])

# Error rule for syntax errors
def p_error(p):
    if p:
        print("Syntax error at token", p.type)
        print("Syntax error at '%s'" % p.value)
        print("line : '%s'" % p.lineno)
        print(p)
        parser.errok()
    else:
        print("Syntax error at EOF")

#Set up precedence
precedence = (
    ('left', 'ANDAND', 'NOT', 'OROR', 'LESS_EQUAL', 'GREATER_EQUAL', 'NOT_EQUAL', 'EQUALEQUAL', 'LESS_THAN', 'GREATER_THAN'),
    ('left', 'EQUAL', 'QUESTIONMARK', 'COLON'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MOD'),
    ('left', 'LPAREN', 'RPAREN', 'LSQUAREBR', 'RSQUAREBR')
)
# Build the parser
parser = yacc.yacc(debug=True)

parser.parse(data,tracking=True)
