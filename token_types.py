# token_types.py
# تعريف أنواع التوكنات والكلمات المفتاحية

INTEGER = "INTEGER"
FLOAT = "FLOAT"
STRING = "STRING"
IDENTIFIER = "IDENTIFIER"
PLUS = "PLUS"
MINUS = "MINUS"
MUL = "MUL"
DIV = "DIV"
LPAREN = "LPAREN"
RPAREN = "RPAREN"
LBRACE = "LBRACE"
RBRACE = "RBRACE"
ASSIGN = "ASSIGN"
SEMICOLON = "SEMICOLON"
COMMA = "COMMA"
EOF = "EOF"

# كلمات مفتاحية عربية
DEF = "DEF"
RETURN = "RETURN"
IF = "IF"
ELSE = "ELSE"
ELIF = "ELIF" # إضافة elif
WHILE = "WHILE"
REPEAT = "REPEAT"
TIMES = "TIMES"
FOR = "FOR"
IN = "IN"
TO = "TO"

PRINT = "PRINT"

# أوامر Turtle
FORWARD = "FORWARD"
BACKWARD = "BACKWARD"
RIGHT = "RIGHT"
LEFT = "LEFT"
GOTO = "GOTO"
SET_HEADING = "SET_HEADING"
PEN_UP = "PEN_UP"
PEN_DOWN = "PEN_DOWN"
SET_PEN_SIZE = "SET_PEN_SIZE"
CHANGE_COLOR = "CHANGE_COLOR"
BEGIN_FILL = "BEGIN_FILL"
END_FILL = "END_FILL"
CLEAR_SCREEN = "CLEAR_SCREEN"
RESET = "RESET" # إضافة reset

# العوامل المنطقية وعوامل المقارنة
EQ = "EQ"       # ==
NEQ = "NEQ"     # !=
LT = "LT"       # <
LTE = "LTE"     # <=
GT = "GT"       # >
GTE = "GTE"     # >=
AND_OP = "AND_OP" # و
OR_OP = "OR_OP"   # أو
NOT_OP = "NOT_OP" # ليس

# الكلمات المفتاحية المنطقية
TRUE = "TRUE"   # صحيح
FALSE = "FALSE" # خطأ

KEYWORDS = {
    "تعريف": DEF,
    "ارجع": RETURN,
    "إذا": IF,
    "وإلا_إذا": ELIF, # إضافة وإلا_إذا
    "وإلا": ELSE,
    "طالما": WHILE,
    "كرر": REPEAT,
    "مرات": TIMES,
    "لكل": FOR,
    "في": IN,
    "إلى": TO,
    "اطبع": PRINT,

    # كلمات مفتاحية Turtle
    "تقدم": FORWARD,
    "تراجع": BACKWARD,
    "يمين": RIGHT,
    "يسار": LEFT,
    "اذهب_إلى": GOTO,
    "تعيين_الاتجاه": SET_HEADING,
    "ارفع_القلم": PEN_UP,
    "أنزل_القلم": PEN_DOWN,
    "تعيين_حجم_القلم": SET_PEN_SIZE,
    "غيّر_لون_القلم": CHANGE_COLOR,
    "ابدأ_تعبئة": BEGIN_FILL,
    "انته_تعبئة": END_FILL, # تصحيح: انته_تعبئة
    "امسح_الشاشة": CLEAR_SCREEN,
    "إعادة_تعيين": RESET,

    # كلمات مفتاحية منطقية
    "صحيح": TRUE,
    "خطأ": FALSE,
    "و": AND_OP,
    "أو": OR_OP,
    "ليس": NOT_OP,
}

# قائمة لعوامل العمليات الثنائية لسهولة التحقق في الـ parser
BIN_OPS = (PLUS, MINUS, MUL, DIV, EQ, NEQ, LT, LTE, GT, GTE, AND_OP, OR_OP)
UNARY_OPS = (PLUS, MINUS, NOT_OP)