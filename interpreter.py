# interpreter.py
from ast_nodes import *
from token_types import AND_OP, OR_OP, EQ, NEQ, LT, LTE, GT, GTE, PLUS, MINUS, MUL, DIV, NOT_OP
import math
import sys

# قم بإنشاء كلاس وهمي (Mock) لدوال السلحفاة للتشغيل بدون واجهة رسومية
# هذا الكلاس يجب أن يحاكي جميع الدوال التي يستدعيها المفسر على كائن السلحفاة
class MockTurtleWidget:
    def __init__(self):
        # يمكنك طباعة رسائل لتتبع الأوامر إذا أردت
        # print("MockTurtleWidget initialized (CLI mode)")
        pass

    def forward(self, distance):
        # print(f"Mock Turtle: تقدم {distance}")
        pass

    def backward(self, distance):
        # print(f"Mock Turtle: تراجع {distance}")
        pass

    def right(self, angle):
        # print(f"Mock Turtle: يمين {angle}")
        pass

    def left(self, angle):
        # print(f"Mock Turtle: يسار {angle}")
        pass

    def goto(self, x, y):
        # print(f"Mock Turtle: اذهب_إلى ({x}, {y})")
        pass
    
    def set_heading(self, angle):
        # print(f"Mock Turtle: تعيين الاتجاه {angle}")
        pass

    def pen_up(self):
        # print("Mock Turtle: ارفع_القلم")
        pass

    def pen_down(self):
        # print(f"Mock Turtle: أنزل_القلم")
        pass
    
    def set_pen_size(self, size):
        # print(f"Mock Turtle: تعيين حجم القلم {size}")
        pass

    def set_pen_color(self, color):
        # print(f"Mock Turtle: تغيير لون القلم إلى {color}")
        pass
    
    def begin_fill(self, color):
        # print(f"Mock Turtle: بدء تعبئة باللون {color}")
        pass
    
    def end_fill(self):
        # print("Mock Turtle: إنهاء تعبئة")
        pass
    
    def clear(self):
        # print("Mock Turtle: مسح الشاشة")
        pass
        
    def reset(self):
        # print("Mock Turtle: إعادة تعيين")
        pass


class Environment:
    def __init__(self, parent=None):
        self.variables = {}
        self.functions = {}
        self.return_value = None
        self.parent = parent

class Interpreter:
    def __init__(self, gui=None): # اجعل gui اختيارياً
        self.env = Environment()
        # هنا التعديل الرئيسي: تحديد كائن السلحفاة بناءً على ما إذا كانت الواجهة الرسومية موجودة
        if gui is None:
            self.turtle_target = MockTurtleWidget()
        else:
            # gui هو ArabicLangApp، ويحتوي على turtle_widget
            self.turtle_target = gui.turtle_widget 
        
        self.output_buffer = [] # لتخزين المخرجات (Print)
        
        # تعريف الدوال المدمجة (Built-in functions)
        self.built_in_functions = {
            "س_كنص": self._builtin_str_as_text,
            "طول": self._builtin_len,
            "قيمة_مطلقة": self._builtin_abs,
        }

    def _builtin_str_as_text(self, args):
        if len(args) != 1:
            raise Exception("الدالة 'س_كنص' تتطلب وسيطاً واحداً.")
        return str(args[0])

    def _builtin_len(self, args):
        if len(args) != 1:
            raise Exception("الدالة 'طول' تتطلب وسيطاً واحداً.")
        if isinstance(args[0], (str, list, tuple)): # أضف tuple أيضاً
            return len(args[0])
        else:
            raise Exception("الدالة 'طول' تتطلب نصاً أو قائمة أو مجموعة.")

    def _builtin_abs(self, args):
        if len(args) != 1:
            raise Exception("الدالة 'قيمة_مطلقة' تتطلب وسيطاً واحداً.")
        if isinstance(args[0], (int, float)):
            return abs(args[0])
        else:
            raise Exception("الدالة 'قيمة_مطلقة' تتطلب رقماً.")

    def interpret(self, program):
        self.output_buffer = [] # مسح المخرجات السابقة
        if program and hasattr(program, 'statements') and isinstance(program.statements, list):
            for stmt in program.statements:
                if stmt is None:
                    continue
                try:
                    self.eval(stmt)
                except ReturnValueException as e:
                    # إذا كانت هناك قيمة إرجاع على المستوى الأعلى من البرنامج، قم بطباعتها
                    self.output_buffer.append(f"قيمة الإرجاع: {e.value}") # لا تعتبر خطأ، بل إخراج
                    break
                except Exception as e:
                    self.output_buffer.append(f"خطأ: {str(e)}")
                    break # توقف عند أول خطأ
        return "\n".join(self.output_buffer)

    def eval(self, node):
        node_type = type(node).__name__
        
        if isinstance(node, Number):
            return node.value

        elif isinstance(node, String):
            return node.value
        
        elif isinstance(node, Boolean):
            return node.value

        elif isinstance(node, BinOp):
            left = self.eval(node.left)
            right = self.eval(node.right)

            if node.op == AND_OP:
                if isinstance(left, bool) and isinstance(right, bool):
                    return left and right
                else:
                    raise Exception(f"خطأ في النوع: عامل 'و' يتطلب قيمًا منطقية، لكن وجد {type(left).__name__} و {type(right).__name__}.")
            elif node.op == OR_OP:
                if isinstance(left, bool) and isinstance(right, bool):
                    return left or right
                else:
                    raise Exception(f"خطأ في النوع: عامل 'أو' يتطلب قيمًا منطقية، لكن وجد {type(left).__name__} و {type(right).__name__}.")

            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                if node.op == PLUS: return left + right
                elif node.op == MINUS: return left - right
                elif node.op == MUL: return left * right
                elif node.op == DIV: 
                    if right == 0: raise Exception("القسمة على صفر!")
                    return left / right
                elif node.op == EQ: return left == right
                elif node.op == NEQ: return left != right
                elif node.op == LT: return left < right
                elif node.op == LTE: return left <= right
                elif node.op == GT: return left > right
                elif node.op == GTE: return left >= right
            
            elif isinstance(left, str) and isinstance(right, str):
                if node.op == PLUS: return left + right
                elif node.op == EQ: return left == right
                elif node.op == NEQ: return left != right
            
            raise Exception(f"عملية غير مدعومة بين {type(left).__name__} و {type(right).__name__} باستخدام العامل {node.op}")

        elif isinstance(node, UnaryOp):
            expr_val = self.eval(node.expr)
            if node.op == PLUS: return +expr_val
            elif node.op == MINUS: return -expr_val
            elif node.op == NOT_OP:
                if isinstance(expr_val, bool):
                    return not expr_val
                else:
                    raise Exception(f"العملية 'ليس' تتطلب قيمة منطقية، لكن وجدت {type(expr_val).__name__}.")
            
        elif isinstance(node, Var):
            current_env = self.env
            while current_env:
                if node.name in current_env.variables:
                    return current_env.variables[node.name]
                current_env = current_env.parent
            raise Exception(f"المتغير غير معرف: {node.name}")

        elif isinstance(node, Assign):
            var_name = node.var.name
            value = self.eval(node.expr)
            self.env.variables[var_name] = value
            return None

        elif isinstance(node, Print):
            value_to_print = self.eval(node.expr)
            self.output_buffer.append(str(value_to_print))
            return None

        elif isinstance(node, FunctionDef):
            self.env.functions[node.name] = {'params': node.params, 'body': node.body}
            return None
        
        elif isinstance(node, ReturnStatement):
            self.env.return_value = self.eval(node.value)
            raise ReturnValueException(self.env.return_value)

        elif isinstance(node, FunctionCall):
            func_name = node.name
            args = [self.eval(arg) for arg in node.args]

            if func_name in self.built_in_functions:
                return self.built_in_functions[func_name](args)
            
            elif func_name in self.env.functions:
                func_info = self.env.functions[func_name]
                params = func_info['params']
                body = func_info['body']

                if len(args) != len(params):
                    raise Exception(f"خطأ: الدالة '{func_name}' تتوقع {len(params)} وسيط، ولكن تم تمرير {len(args)}.")

                original_env = self.env
                self.env = Environment(parent=original_env) # نطاق جديد للدالة

                for param_name, arg_value in zip(params, args):
                    self.env.variables[param_name] = arg_value
                
                return_value = None
                try:
                    for stmt in body:
                        self.eval(stmt)
                except ReturnValueException as e:
                    return_value = e.value
                finally:
                    self.env = original_env # استعادة النطاق الأصلي
                
                return return_value

            else:
                raise Exception(f"الدالة غير معرفة: {func_name}")

        elif isinstance(node, RepeatLoop):
            times = self.eval(node.times)
            if not isinstance(times, int) or times < 0:
                raise Exception("عدد مرات التكرار يجب أن يكون عدداً صحيحاً موجباً.")
            for _ in range(times):
                for stmt in node.body:
                    self.eval(stmt)
            return None

        elif isinstance(node, WhileLoop):
            while self.eval(node.condition):
                for stmt in node.body:
                    self.eval(stmt)
            return None

        elif isinstance(node, ForLoop):
            start = self.eval(node.start_expr)
            end = self.eval(node.end_expr)
            
            if not isinstance(start, int) or not isinstance(end, int):
                raise Exception("قِيم بداية ونهاية حلقة 'لكل' يجب أن تكون أعداداً صحيحة.")
            
            original_env = self.env
            self.env = Environment(parent=original_env)

            for i in range(start, end + 1):
                self.env.variables[node.var_name] = i
                for stmt in node.body:
                    self.eval(stmt)
            
            self.env = original_env
            return None

        elif isinstance(node, IfStatement):
            if self.eval(node.condition):
                for stmt in node.then_body:
                    self.eval(stmt)
            else:
                executed_elif = False
                for elif_condition, elif_body in node.elif_branches:
                    if self.eval(elif_condition):
                        for stmt in elif_body:
                            self.eval(stmt)
                        executed_elif = True
                        break
                if not executed_elif and node.else_body:
                    for stmt in node.else_body:
                        self.eval(stmt)
            return None
        
        # تنفيذ أوامر الرسم (Turtle Graphics) - تم تعديلها لاستدعاء self.turtle_target مباشرة
        elif isinstance(node, Forward):
            distance = self.eval(node.distance)
            self.turtle_target.forward(distance)
            return None

        elif isinstance(node, Backward):
            distance = self.eval(node.distance)
            self.turtle_target.backward(distance)
            return None

        elif isinstance(node, Right):
            angle = self.eval(node.angle)
            self.turtle_target.right(angle)
            return None

        elif isinstance(node, Left):
            angle = self.eval(node.angle)
            self.turtle_target.left(angle)
            return None

        elif isinstance(node, GoTo):
            x = self.eval(node.x)
            y = self.eval(node.y)
            self.turtle_target.goto(x, y)
            return None

        elif isinstance(node, SetHeading):
            angle = self.eval(node.angle)
            self.turtle_target.set_heading(angle)
            return None

        elif isinstance(node, PenUp):
            self.turtle_target.pen_up()
            return None

        elif isinstance(node, PenDown):
            self.turtle_target.pen_down()
            return None
        
        elif isinstance(node, SetPenSize):
            size = self.eval(node.size)
            self.turtle_target.set_pen_size(size)
            return None

        elif isinstance(node, ChangeColor):
            color_val = self.eval(node.color)
            self.turtle_target.set_pen_color(str(color_val))
            return None

        elif isinstance(node, BeginFill):
            color_val = self.eval(node.color)
            self.turtle_target.begin_fill(str(color_val))
            return None

        elif isinstance(node, EndFill):
            self.turtle_target.end_fill()
            return None

        elif isinstance(node, ClearScreen):
            self.turtle_target.clear()
            return None
            
        elif isinstance(node, Reset):
            self.turtle_target.reset()
            return None

        else:
            raise Exception(f"نوع عقدة غير معروف للتنفيذ: {node_type}")

class ReturnValueException(Exception):
    """استثناء مخصص للتعامل مع قيم الإرجاع من الدوال."""
    def __init__(self, value):
        self.value = value