#! /usr/bin/env python26
# coding: utf-8 
class SSexpr:
    """
    A Simple Simplified Sexprs Reader.
    Author ee.zsy
    Date Mar.2012
    type SSexpr = Symbol of string | Block of SSexpr list;
    function parse : string - > SSexpr;
    >>> parse(r'(1 2 "3\" 4"( 1 2 3))')
    ['1', '2', '3" 4', ['1', '2', '3']]
    Notice that Python evaluates expressions from left to right.
    """
    w = " \n\t"
    e = " \n\t()[]"
    b = (lambda i:lambda s,x:i(x).pop())(set(')]').difference)
    m = 'Brackets or Parentheses do not match.'
    a = dict(zip('\"\'nt\\','\"\'\n\t\\'))
    f = 'Escape character is not recognized.'
    def __init__(s,code):
        s.s, s.p = code, 0
    def read(s):
        try:return s.exp()
        except RuntimeError as e:raise SyntaxError(e)
    @classmethod
    def parse(c,code):
        return c(code).read()
    def peek(s):
        return s.s[s.p] if s.p<len(s.s) else None
    def eat(s):
        s.p += 1;return s.s[s.p-1]
    def exp(s,cm=0):
        c = s.peek()
        if c is None:return None  
        elif c in s.w:return s.eat() and s.exp()
        elif c == '(':return s.eat() and s.blk(')')
        elif c == '[':return s.eat() and s.blk(']')
        elif c == '"':return s.eat() and s.str()
        else:return s.sym()
    def sym(s):
        c = s.peek()
        if c is None or c in s.e:return ""
        else:return s.eat() and c+s.sym()
    def str(s):
        c = s.peek()
        if c is None:raise EOFError
        elif c == '"':return s.eat() and ''
        elif c =='\\':return s.eat() and s.esc(s.eat())+s.str()
        else:return s.eat() and c+s.str()
    def esc(s,c):
        if c in s.a:return s.a[c]
        else:raise SyntaxError(s.f)
    def blk(s,end):
        c = s.peek()
        if c is None:raise EOFError
        elif c == s.b(end):raise SyntaxError(s.m)
        elif c in s.w:return s.eat() and s.blk(end)
        elif c == end:return s.eat() and tuple()
        else:return tuple([s.exp()])+s.blk(end) 
        
if 1:
    assert SSexpr("""123 12""").read() == '123'
    assert SSexpr("""(1 2 3 4(1 2 3))""").read() == ('1', '2', '3', '4', ('1', '2', '3'))
    assert SSexpr("""(1 2 "3 4"( 1 2 3))""").read() == ('1', '2', '3 4', ('1', '2', '3'))
    assert SSexpr.parse(r"""(1 2 "3\" 4"( 1 2 3))""") == ('1', '2', '3" 4', ('1', '2', '3'))
    assert SSexpr.parse(r"""[]""") == tuple()

if __name__ == '__main__':
    print SSexpr("""[hello world]""").read()
    while 1:
        print SSexpr(raw_input()).read()
