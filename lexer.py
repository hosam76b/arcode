# lexer.py
import unicodedata # إضافة هذا السطر
from token_types import *

class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __str__(self):
        return f"Token({self.type}, {self.value})"

    def __repr__(self):
        return self.__str__()

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if len(self.text) > 0 else None

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def skip_comment(self):
        while self.current_char is not None and self.current_char != '\n':
            self.advance()
        # بعد التعليق، قد يكون هناك مسافات بيضاء أو EOF
        self.skip_whitespace()

    def _read_number_string(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        
        # التعامل مع الأرقام العشرية
        if self.current_char == '.' and self.peek_char() is not None and self.peek_char().isdigit():
            result += self.current_char
            self.advance()
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()
            return float(result)
        
        return int(result)

    def _read_string(self):
        self.advance() # تخطي علامة الاقتباس الافتتاحية "
        result = ''
        while self.current_char is not None and self.current_char != '\"':
            result += self.current_char
            self.advance()
        self.advance() # تخطي علامة الاقتباس الختامية "
        return result

    def _read_identifier(self):
        result = ''
        # الحروف العربية تحتاج إلى unicodedata.category لتحديد إذا كانت حرفاً
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_' or unicodedata.category(self.current_char).startswith('L')):
            result += self.current_char
            self.advance()
        
        # التحقق من الكلمات المفتاحية
        token_type = KEYWORDS.get(result, IDENTIFIER)
        return Token(token_type, result)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            # التعامل مع التعليقات
            if self.current_char == '#':
                self.skip_comment()
                continue

            if self.current_char.isdigit():
                num_str = ''
                is_float = False
                while self.current_char is not None and self.current_char.isdigit():
                    num_str += self.current_char
                    self.advance()
                if self.current_char == '.':
                    is_float = True
                    num_str += self.current_char
                    self.advance()
                    while self.current_char is not None and self.current_char.isdigit():
                        num_str += self.current_char
                        self.advance()
                
                value = float(num_str) if is_float else int(num_str)
                return Token(FLOAT if is_float else INTEGER, value)

            if self.current_char == '\"':
                return Token(STRING, self._read_string())

            # التحقق من الكلمات المفتاحية والحروف العربية
            if self.current_char.isalpha() or self.current_char == '_' or unicodedata.category(self.current_char).startswith('L'):
                return self._read_identifier()

            # عوامل العمليات
            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            if self.current_char == '{':
                self.advance()
                return Token(LBRACE, '{')

            if self.current_char == '}':
                self.advance()
                return Token(RBRACE, '}')
            
            if self.current_char == '=':
                if self.peek_char() == '=':
                    self.advance(); self.advance()
                    return Token(EQ, '==')
                else:
                    self.advance()
                    return Token(ASSIGN, '=')

            if self.current_char == '!':
                if self.peek_char() == '=':
                    self.advance(); self.advance()
                    return Token(NEQ, '!=')
                else:
                    raise Exception(f"رمز غير معروف: {self.current_char}")

            if self.current_char == '<':
                if self.peek_char() == '=':
                    self.advance(); self.advance()
                    return Token(LTE, '<=')
                else:
                    self.advance()
                    return Token(LT, '<')
            
            if self.current_char == '>':
                if self.peek_char() == '=':
                    self.advance(); self.advance()
                    return Token(GTE, '>=')
                else:
                    self.advance()
                    return Token(GT, '>')
            
            if self.current_char == ';':
                self.advance()
                return Token(SEMICOLON, ';')

            if self.current_char == ',':
                self.advance()
                return Token(COMMA, ',')
            
            # إذا لم يتم التعرف على الحرف، فإنه خطأ
            raise Exception(f"رمز غير معروف: {self.current_char} عند الموضع {self.pos}")

        return Token(EOF, None)

    def peek_char(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    # هذا الـ peek هو الذي كان مفقوداً أو غير صحيح في بعض الإصدارات
    def peek(self):
        """
        ينظر إلى التوكن التالي دون استهلاكه.
        """
        # حفظ الحالة الحالية للمحلل
        saved_pos = self.pos
        saved_current_char = self.current_char

        # الحصول على التوكن التالي (مما سيؤدي إلى تقدم الحالة الداخلية)
        try:
            token = self.get_next_token()
        except Exception: # يمكن أن تحدث أخطاء أثناء النظر للأمام (مثلاً، رمز غير معروف)
            token = None # نعتبره لا يوجد توكن صالح

        # استعادة الحالة الأصلية "للتراجع" عن القراءة
        self.pos = saved_pos
        self.current_char = saved_current_char
        return token