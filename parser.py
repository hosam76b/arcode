# parser.py
from token_types import *
from lexer import Lexer, Token
from ast_nodes import *

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise Exception(f"خطأ في التحليل: المتوقع {token_type}، لكن وجد {self.current_token.type} عند الموضع {self.lexer.pos}")

    def parse(self):
        statements = []
        while self.current_token.type != EOF:
            statement = self.parse_statement()
            if statement is not None:
                statements.append(statement)
            
            # يجب أن تنتهي كل عبارة بفاصلة منقوطة، ما لم تكن كتلة (مثل if/while/def)
            # أو كانت آخر عبارة في الملف
            if self.current_token.type == SEMICOLON:
                self.eat(SEMICOLON)
            elif self.current_token.type != EOF and not (isinstance(statement, (IfStatement, WhileLoop, RepeatLoop, ForLoop, FunctionDef)) or (isinstance(statement, FunctionCall) and statement.name in ["ابدأ_تعبئة", "انته_تعبئة"])):
                # إذا لم تكن فاصلة منقوطة وليست نهاية ملف وليست كتلة أو أمر تعبئة، ارفع خطأ
                raise Exception(f"خطأ في التحليل: المتوقع فاصلة منقوطة بعد البيان، لكن وجد {self.current_token.type} عند الموضع {self.lexer.pos}")
            
            if self.current_token.type == EOF:
                break
        return Program(statements)

    def parse_block(self):
        self.eat(LBRACE)
        statements = []
        # allow empty blocks
        while self.current_token.type != RBRACE:
            statement = self.parse_statement()
            if statement is not None:
                statements.append(statement)
            if self.current_token.type == SEMICOLON:
                self.eat(SEMICOLON)
            elif self.current_token.type != RBRACE: # لا تتطلب فاصلة منقوطة قبل RBRACE مباشرة إذا كان البيان الأخير
                raise Exception(f"خطأ في التحليل: المتوقع فاصلة منقوطة أو قوس إغلاق كتلة، لكن وجد {self.current_token.type} عند الموضع {self.lexer.pos}")
        self.eat(RBRACE)
        return statements

    def parse_statement(self):
        token_type = self.current_token.type

        if token_type == IDENTIFIER:
            # يمكن أن يكون تعيين متغير أو استدعاء دالة (بما في ذلك أوامر Turtle)
            if self.lexer.peek() and self.lexer.peek().type == ASSIGN:
                return self.parse_assignment()
            else:
                return self.parse_function_or_turtle_call()
        elif token_type == PRINT:
            return self.parse_print_statement()
        elif token_type == DEF:
            return self.parse_function_def()
        elif token_type == RETURN:
            return self.parse_return_statement()
        elif token_type == REPEAT:
            return self.parse_repeat_loop()
        elif token_type == WHILE:
            return self.parse_while_loop()
        elif token_type == FOR:
            return self.parse_for_loop()
        elif token_type == IF:
            return self.parse_if_statement()
        
        # أوامر Turtle كـ statements مباشرة (ليس function calls)
        elif token_type == FORWARD:
            return self.parse_forward()
        elif token_type == BACKWARD:
            return self.parse_backward()
        elif token_type == RIGHT:
            return self.parse_right()
        elif token_type == LEFT:
            return self.parse_left()
        elif token_type == GOTO:
            return self.parse_goto()
        elif token_type == SET_HEADING:
            return self.parse_set_heading()
        elif token_type == PEN_UP:
            return self.parse_pen_up()
        elif token_type == PEN_DOWN:
            return self.parse_pen_down()
        elif token_type == SET_PEN_SIZE:
            return self.parse_set_pen_size()
        elif token_type == CHANGE_COLOR:
            return self.parse_change_color()
        elif token_type == BEGIN_FILL:
            return self.parse_begin_fill()
        elif token_type == END_FILL:
            return self.parse_end_fill()
        elif token_type == CLEAR_SCREEN:
            return self.parse_clear_screen()
        elif token_type == RESET:
            return self.parse_reset()
        
        raise Exception(f"خطأ في التحليل: بيان غير متوقع {self.current_token.type} عند الموضع {self.lexer.pos}")

    def parse_assignment(self):
        var_node = Var(self.current_token.value)
        self.eat(IDENTIFIER)
        self.eat(ASSIGN)
        expr_node = self.parse_expression()
        return Assign(var_node, expr_node)

    def parse_print_statement(self):
        self.eat(PRINT)
        self.eat(LPAREN)
        expr = self.parse_expression()
        self.eat(RPAREN)
        return Print(expr)

    def parse_function_def(self):
        self.eat(DEF)
        name = self.current_token.value
        self.eat(IDENTIFIER)
        self.eat(LPAREN)
        params = []
        if self.current_token.type != RPAREN:
            params.append(self.current_token.value)
            self.eat(IDENTIFIER)
            while self.current_token.type == COMMA:
                self.eat(COMMA)
                params.append(self.current_token.value)
                self.eat(IDENTIFIER)
        self.eat(RPAREN)
        body = self.parse_block()
        return FunctionDef(name, params, body)

    def parse_function_call(self):
        name = self.current_token.value
        self.eat(IDENTIFIER)
        self.eat(LPAREN)
        args = []
        if self.current_token.type != RPAREN:
            args.append(self.parse_expression())
            while self.current_token.type == COMMA:
                self.eat(COMMA)
                args.append(self.parse_expression())
        self.eat(RPAREN)
        return FunctionCall(name, args)
    
    # دالة لتمييز استدعاء الدوال عن أوامر Turtle التي تُعامل كـ statements
    def parse_function_or_turtle_call(self):
        name = self.current_token.value
        # التحقق من الكلمات المفتاحية لـ Turtle التي تُعامل كـ statements
        if name == "تقدم":
            return self.parse_forward()
        elif name == "تراجع":
            return self.parse_backward()
        # ... أضف هنا جميع أوامر Turtle التي تم التعامل معها كـ statements في parse_statement
        # بما أن parse_statement تتعامل معها مباشرة، فهذه الدالة قد لا تكون ضرورية بهذا الشكل
        # ولكن للتوضيح، هذا هو المكان الذي يمكن أن يحدث فيه التباس
        # الأفضل هو أن parser.parse_statement تحدد النوع مباشرة بناءً على token_type
        # بما أننا نقوم بذلك بالفعل، فهذه الدالة يمكن أن تُبسط لاستدعاء دالة.
        
        # إذا لم تكن أمر Turtle، فهي استدعاء دالة عادية
        return self.parse_function_call()

    def parse_return_statement(self):
        self.eat(RETURN)
        value = self.parse_expression()
        return ReturnStatement(value)

    def parse_repeat_loop(self):
        self.eat(REPEAT)
        times = self.parse_expression()
        self.eat(TIMES)
        body = self.parse_block()
        return RepeatLoop(times, body)

    def parse_while_loop(self):
        self.eat(WHILE)
        condition = self.parse_expression()
        body = self.parse_block()
        return WhileLoop(condition, body)

    def parse_for_loop(self):
        self.eat(FOR)
        var_name = self.current_token.value
        self.eat(IDENTIFIER)
        self.eat(IN)
        start_expr = self.parse_expression()
        self.eat(TO)
        end_expr = self.parse_expression()
        body = self.parse_block()
        return ForLoop(var_name, start_expr, end_expr, body)

    def parse_if_statement(self):
        self.eat(IF)
        condition = self.parse_expression()
        then_body = self.parse_block()
        
        elif_branches = []
        while self.current_token.type == ELIF:
            self.eat(ELIF)
            elif_condition = self.parse_expression()
            elif_body = self.parse_block()
            elif_branches.append((elif_condition, elif_body))
        
        else_body = None
        if self.current_token.type == ELSE:
            self.eat(ELSE)
            else_body = self.parse_block()
        
        return IfStatement(condition, then_body, elif_branches, else_body)

    # دوال تحليل أوامر Turtle
    def parse_forward(self):
        self.eat(FORWARD)
        self.eat(LPAREN)
        distance = self.parse_expression()
        self.eat(RPAREN)
        return Forward(distance)

    def parse_backward(self):
        self.eat(BACKWARD)
        self.eat(LPAREN)
        distance = self.parse_expression()
        self.eat(RPAREN)
        return Backward(distance)

    def parse_right(self):
        self.eat(RIGHT)
        self.eat(LPAREN)
        angle = self.parse_expression()
        self.eat(RPAREN)
        return Right(angle)

    def parse_left(self):
        self.eat(LEFT)
        self.eat(LPAREN)
        angle = self.parse_expression()
        self.eat(RPAREN)
        return Left(angle)

    def parse_goto(self):
        self.eat(GOTO)
        self.eat(LPAREN)
        x = self.parse_expression()
        self.eat(COMMA)
        y = self.parse_expression()
        self.eat(RPAREN)
        return GoTo(x, y)

    def parse_set_heading(self):
        self.eat(SET_HEADING)
        self.eat(LPAREN)
        angle = self.parse_expression()
        self.eat(RPAREN)
        return SetHeading(angle)

    def parse_pen_up(self):
        self.eat(PEN_UP)
        self.eat(LPAREN)
        self.eat(RPAREN)
        return PenUp()

    def parse_pen_down(self):
        self.eat(PEN_DOWN)
        self.eat(LPAREN)
        self.eat(RPAREN)
        return PenDown()
    
    def parse_set_pen_size(self):
        self.eat(SET_PEN_SIZE)
        self.eat(LPAREN)
        size = self.parse_expression()
        self.eat(RPAREN)
        return SetPenSize(size)

    def parse_change_color(self):
        self.eat(CHANGE_COLOR)
        self.eat(LPAREN)
        color = self.parse_expression() # اللون يمكن أن يكون نص (مثل "أحمر")
        self.eat(RPAREN)
        return ChangeColor(color)

    def parse_begin_fill(self):
        self.eat(BEGIN_FILL)
        self.eat(LPAREN)
        color = self.parse_expression() # اللون يمكن أن يكون نص
        self.eat(RPAREN)
        return BeginFill(color)

    def parse_end_fill(self):
        self.eat(END_FILL)
        self.eat(LPAREN)
        self.eat(RPAREN)
        return EndFill()

    def parse_clear_screen(self):
        self.eat(CLEAR_SCREEN)
        self.eat(LPAREN)
        self.eat(RPAREN)
        return ClearScreen()
        
    def parse_reset(self):
        self.eat(RESET)
        self.eat(LPAREN)
        self.eat(RPAREN)
        return Reset()

    # قواعد التحليل للتعبيرات
    def parse_expression(self):
        return self.parse_logical_expression()

    def parse_logical_expression(self):
        node = self.parse_logical_term()
        while self.current_token.type == OR_OP:
            token = self.current_token
            self.eat(OR_OP)
            node = BinOp(left=node, op=token.value, right=self.parse_logical_term())
        return node

    def parse_logical_term(self):
        node = self.parse_comparison()
        while self.current_token.type == AND_OP:
            token = self.current_token
            self.eat(AND_OP)
            node = BinOp(left=node, op=token.value, right=self.parse_comparison())
        return node

    def parse_comparison(self):
        node = self.parse_arithmetic_expression()
        while self.current_token.type in (EQ, NEQ, LT, LTE, GT, GTE):
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left=node, op=token.value, right=self.parse_arithmetic_expression())
        return node

    def parse_arithmetic_expression(self):
        node = self.parse_term()
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)
            node = BinOp(left=node, op=token.value, right=self.parse_term())
        return node

    def parse_term(self):
        node = self.parse_factor()
        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)
            node = BinOp(left=node, op=token.value, right=self.parse_factor())
        return node

    def parse_factor(self):
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return Number(token.value)
        elif token.type == FLOAT:
            self.eat(FLOAT)
            return Number(token.value)
        elif token.type == STRING:
            self.eat(STRING)
            return String(token.value)
        elif token.type == TRUE: # إضافة للقيم المنطقية
            self.eat(TRUE)
            return Boolean(True)
        elif token.type == FALSE: # إضافة للقيم المنطقية
            self.eat(FALSE)
            return Boolean(False)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.parse_expression()
            self.eat(RPAREN)
            return node
        elif token.type == IDENTIFIER:
            # هنا يجب أن نحدد ما إذا كان هذا استدعاء دالة أو مجرد متغير
            if self.lexer.peek() and self.lexer.peek().type == LPAREN:
                return self.parse_function_call()
            else:
                self.eat(IDENTIFIER)
                return Var(token.value)
        elif token.type in (PLUS, MINUS):
            op = token.value # هنا لا تزال القيمة الحرفية مناسبة لـ UnaryOp
            self.eat(token.type)
            return UnaryOp(op=op, expr=self.parse_factor())
        elif token.type == NOT_OP:
            self.eat(NOT_OP)
            return UnaryOp(op="ليس", expr=self.parse_factor()) # استخدم "ليس" كقيمة العامل
        
        raise Exception(f"خطأ في التحليل: عامل غير متوقع {self.current_token.type} عند الموضع {self.lexer.pos}")