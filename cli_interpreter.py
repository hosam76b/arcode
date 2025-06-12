# cli_interpreter.py
import sys
import os # لإضافة المسار الحالي إلى sys.path

# إضافة المسار الحالي لتمكين استيراد الملفات المحلية
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# استيراد المكونات اللازمة
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from ast_nodes import Program # ستحتاج إلى Program من ast_nodes.py

def run_arcode_file(file_path):
    """
    يقوم بقراءة وتنفيذ كود ArabiCode من ملف.
    """
    if not os.path.exists(file_path):
        print(f"خطأ: الملف '{file_path}' غير موجود.")
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        print(f"--- تم قراءة الكود من '{file_path}': ---\n{code}\n----------------------------------") # DEBUG: Show loaded code

        lexer = Lexer(code)
        # يمكنك إلغاء التعليق عن هذا الجزء إذا أردت رؤية التوكنات الناتجة عن المحلل اللغوي
        # from token_types import EOF
        # tokens = []
        # while True:
        #     token = lexer.get_next_token()
        #     tokens.append(token)
        #     if token.type == EOF:
        #         break
        # print(f"--- التوكنات الناتجة: ---\n{tokens}\n----------------------------------")
        # lexer = Lexer(code) # أعد تهيئة المحلل اللغوي للمحلل النحوي بعد قراءة التوكنات

        parser = Parser(lexer)
        print("--- بدء التحليل النحوي... ---") # DEBUG
        tree = parser.parse()
        print("--- تم التحليل النحوي بنجاح. ---") # DEBUG
        # يمكنك إلغاء التعليق عن هذا الجزء إذا أردت رؤية نوع عقدة الشجرة الجذرية
        # print(f"--- عقدة الشجرة الجذرية (AST Root): {type(tree).__name__} ---") 
        # if isinstance(tree, Program):
        #     print(f"--- عدد العبارات في البرنامج: {len(tree.statements)} ---")

        # لا نمرر كائن GUI حقيقي هنا، سيستخدم المفسر الـ MockTurtleWidget
        interpreter = Interpreter(gui=None) 
        print("--- بدء التنفيذ... ---") # DEBUG
        
        # دالة interpret في Interpreter تتوقع كائن Program
        output = interpreter.interpret(tree) 
        
        print("--- تم التنفيذ. ---") # DEBUG

        if output:
            print("\n--- إخراج الكود: ---")
            print(output)
            print("--------------------\n")
        else:
            print("\n--- تم تنفيذ الكود بنجاح (لا يوجد إخراج للطباعة). ---\n")

    except Exception as e:
        print(f"\n--- خطأ في التنفيذ: ---\n{str(e)}\n-----------------------\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("الاستخدام: python cli_interpreter.py <مسار_الملف.arcode>")
        print("مثال: python cli_interpreter.py test.arcode")
        sys.exit(1)
    
    file_path = sys.argv[1]
    run_arcode_file(file_path)