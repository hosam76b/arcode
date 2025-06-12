# ast_nodes.py

class Program:
    def __init__(self, statements):
        self.statements = statements

class Number:
    def __init__(self, value):
        self.value = value

class String:
    def __init__(self, value):
        self.value = value

class Boolean: # إضافة عقدة للقيم المنطقية
    def __init__(self, value):
        self.value = value

class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class UnaryOp:
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

class Var:
    def __init__(self, name):
        self.name = name

class Assign:
    def __init__(self, var, expr):
        self.var = var
        self.expr = expr

class Print:
    def __init__(self, expr):
        self.expr = expr

class FunctionDef:
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class FunctionCall:
    def __init__(self, name, args):
        self.name = name
        self.args = args

class ReturnStatement:
    def __init__(self, value):
        self.value = value

class RepeatLoop:
    def __init__(self, times, body):
        self.times = times
        self.body = body

class WhileLoop:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class ForLoop:
    def __init__(self, var_name, start_expr, end_expr, body):
        self.var_name = var_name
        self.start_expr = start_expr
        self.end_expr = end_expr
        self.body = body

class IfStatement: # إضافة عقدة لبيان If
    def __init__(self, condition, then_body, elif_branches=None, else_body=None):
        self.condition = condition
        self.then_body = then_body
        self.elif_branches = elif_branches if elif_branches is not None else []
        self.else_body = else_body

# عقد أوامر Turtle (لتعامل أسهل معها في المفسر)
class Forward:
    def __init__(self, distance):
        self.distance = distance

class Backward:
    def __init__(self, distance):
        self.distance = distance

class Right:
    def __init__(self, angle):
        self.angle = angle

class Left:
    def __init__(self, angle):
        self.angle = angle

class GoTo:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class SetHeading:
    def __init__(self, angle):
        self.angle = angle

class PenUp:
    def __init__(self):
        pass

class PenDown:
    def __init__(self):
        pass

class SetPenSize:
    def __init__(self, size):
        self.size = size

class ChangeColor:
    def __init__(self, color):
        self.color = color

class BeginFill:
    def __init__(self, color):
        self.color = color

class EndFill:
    def __init__(self):
        pass

class ClearScreen:
    def __init__(self):
        pass
        
class Reset:
    def __init__(self):
        pass