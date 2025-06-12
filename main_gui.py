import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QFileDialog, QLabel, QSplitter, QGraphicsView, QGraphicsScene
)
from PyQt5.QtCore import Qt, QPointF, QRectF
from PyQt5.QtGui import QPen, QColor, QPainter, QPainterPath, QIcon 
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
import math 

class TurtleWidget(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)
        
        self.pen = QPen(QColor(0, 0, 0), 2)
        self.current_position = QPointF(0, 0)
        self.heading = 0 # 0 degrees is facing upwards (North)
        self.pen_is_down = True
        self.fill_color = None
        self.fill_path = None # QPainterPath for filling

        self.reset_turtle() # لتهيئة السلحفاة عند البدء

    def reset_turtle(self):
        self.scene.clear()
        # تعيين مركز المشهد عند (0,0)
        self.scene.setSceneRect(-250, -250, 500, 500) # على سبيل المثال، مشهد 500x500 بكسل
        self.current_position = QPointF(0, 0) # ابدأ من المنتصف
        self.heading = 0 # اتجاه للأعلى (North)
        self.pen_is_down = True
        self.pen = QPen(QColor(0, 0, 0), 2) # قلم أسود بحجم 2 افتراضياً
        self.fill_color = None
        self.fill_path = None
        self.scene.addEllipse(-3, -3, 6, 6, QPen(Qt.black), QColor(Qt.red)) # نقطة البداية (اختياري)


    def forward(self, distance):
        if not isinstance(distance, (int, float)):
            raise TypeError("المسافة يجب أن تكون رقمًا (عددًا صحيحًا أو عشريًا).")
        angle_rad = (self.heading + 90) * (math.pi / 180.0) # 0 درجة تشير للأعلى، math.cos/sin تستخدم 0 لليمين (الشرق)
        new_x = self.current_position.x() + distance * math.cos(angle_rad)
        new_y = self.current_position.y() + distance * math.sin(angle_rad)
        new_position = QPointF(new_x, new_y)

        if self.fill_path:
            if self.fill_path.elementCount() == 0:
                self.fill_path.moveTo(self.current_position)
            self.fill_path.lineTo(new_position)

        if self.pen_is_down:
            self.scene.addLine(self.current_position.x(), self.current_position.y(),
                               new_position.x(), new_position.y(), self.pen)
        self.current_position = new_position
        self.scene.update()

    def backward(self, distance):
        self.forward(-distance)

    def right(self, angle):
        if not isinstance(angle, (int, float)):
            raise TypeError("الزاوية يجب أن تكون رقمًا (عددًا صحيحًا أو عشريًا).")
        self.heading = (self.heading - angle) % 360
        # print(f"Heading changed to: {self.heading}")

    def left(self, angle):
        if not isinstance(angle, (int, float)):
            raise TypeError("الزاوية يجب أن تكون رقمًا (عددًا صحيحًا أو عشريًا).")
        self.heading = (self.heading + angle) % 360
        # print(f"Heading changed to: {self.heading}")

    def goto(self, x, y):
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            raise TypeError("الإحداثيات يجب أن تكون أرقامًا (أعدادًا صحيحة أو عشرية).")
        new_position = QPointF(x, y)
        if self.fill_path:
            if self.fill_path.elementCount() == 0:
                self.fill_path.moveTo(self.current_position)
            self.fill_path.lineTo(new_position)

        if self.pen_is_down:
            self.scene.addLine(self.current_position.x(), self.current_position.y(),
                               new_position.x(), new_position.y(), self.pen)
        self.current_position = new_position
        self.scene.update()
        
    def set_heading(self, angle):
        if not isinstance(angle, (int, float)):
            raise TypeError("الزاوية يجب أن تكون رقمًا (عددًا صحيحًا أو عشريًا).")
        self.heading = angle % 360
        # print(f"Heading explicitly set to: {self.heading}")

    def pen_up(self):
        self.pen_is_down = False

    def pen_down(self):
        self.pen_is_down = True
    
    def set_pen_size(self, size):
        if not isinstance(size, (int, float)) or size <= 0:
            raise ValueError("حجم القلم يجب أن يكون رقمًا موجبًا.")
        self.pen.setWidth(int(size)) # عرض القلم يجب أن يكون عددًا صحيحًا

    def set_pen_color(self, color_name):
        # يمكن تحويل color_name إلى QColor
        color = QColor(color_name)
        if not color.isValid():
            raise ValueError(f"اللون '{color_name}' غير صالح. استخدم أسماء ألوان CSS (مثل 'red', 'blue') أو قيم سداسية عشرية (مثل '#RRGGBB').")
        self.pen.setColor(color)

    def begin_fill(self, color_name):
        color = QColor(color_name)
        if not color.isValid():
            raise ValueError(f"اللون '{color_name}' غير صالح للتعبئة.")
        self.fill_color = color
        self.fill_path = QPainterPath()
        self.fill_path.moveTo(self.current_position) # ابدأ المسار من الموضع الحالي

    def end_fill(self):
        if self.fill_path and self.fill_color:
            self.fill_path.closeSubpath()
            self.scene.addPath(self.fill_path, QPen(Qt.NoPen), QColor(self.fill_color))
        self.fill_path = None
        self.fill_color = None

    def clear(self):
        self.scene.clear()
        self.current_position = QPointF(0, 0)
        self.heading = 0
        self.pen_is_down = True
        self.pen = QPen(QColor(0, 0, 0), 2)
        self.fill_color = None
        self.fill_path = None
        self.scene.addEllipse(-3, -3, 6, 6, QPen(Qt.black), QColor(Qt.red)) # نقطة البداية (اختياري)
        
    def reset(self): # إعادة تعيين كاملة تشمل الموضع والاتجاه وكل شيء
        self.reset_turtle()


class ArabicLangApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('ArabiCode Editor')
        self.setGeometry(100, 100, 1000, 700) # زيادة حجم النافذة

        # Text Editor
        self.text_area = QTextEdit(self)
        self.text_area.setFontPointSize(14)
        self.text_area.setPlaceholderText("اكتب الكود الخاص بك هنا...")

        # Output Area
        self.output_area = QTextEdit(self)
        self.output_area.setReadOnly(True)
        self.output_area.setFontPointSize(12)
        self.output_area.setPlaceholderText("مخرجات البرنامج ستظهر هنا...")

        # Turtle Graphics Area
        self.turtle_widget = TurtleWidget(self)
        # قم بتهيئة المفسر مع مرجع إلى turtle_widget
        self.interpreter = Interpreter(gui=self) # نمرر self لأن ArabicLangApp يحتوي على turtle_widget

        # Splitter to resize text_area and output_area/turtle_widget
        right_panel_splitter = QSplitter(Qt.Vertical)
        right_panel_splitter.addWidget(self.output_area)
        right_panel_splitter.addWidget(self.turtle_widget)
        right_panel_splitter.setStretchFactor(0, 1) # Output area can stretch
        right_panel_splitter.setStretchFactor(1, 2) # Turtle graphics area stretches more

        main_splitter = QSplitter(Qt.Horizontal)
        main_splitter.addWidget(self.text_area)
        main_splitter.addWidget(right_panel_splitter)
        main_splitter.setStretchFactor(0, 1) # Text area can stretch
        main_splitter.setStretchFactor(1, 1) # Right panel can stretch

        # Buttons
        btn_run = QPushButton('تشغيل الكود')
        btn_run.clicked.connect(self.run_code)
        btn_run.setStyleSheet("background-color: #4CAF50; color: white; font-size: 16px; padding: 10px;")

        btn_clear_editor = QPushButton('مسح المحرر')
        btn_clear_editor.clicked.connect(self.clear_editor)
        btn_clear_editor.setStyleSheet("background-color: #f44336; color: white; font-size: 16px; padding: 10px;")

        btn_clear_drawing = QPushButton('مسح الرسم')
        btn_clear_drawing.clicked.connect(self.clear_drawing)
        btn_clear_drawing.setStyleSheet("background-color: #2196F3; color: white; font-size: 16px; padding: 10px;")
        
        btn_open = QPushButton('فتح ملف')
        btn_open.clicked.connect(self.load_code)
        btn_open.setStyleSheet("background-color: #FFC107; color: black; font-size: 16px; padding: 10px;")

        btn_save = QPushButton('حفظ ملف')
        btn_save.clicked.connect(self.save_code)
        btn_save.setStyleSheet("background-color: #607D8B; color: white; font-size: 16px; padding: 10px;")


        button_layout = QHBoxLayout()
        button_layout.addWidget(btn_run)
        button_layout.addWidget(btn_clear_editor)
        button_layout.addWidget(btn_clear_drawing)
        button_layout.addWidget(btn_open)
        button_layout.addWidget(btn_save)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(main_splitter)
        main_layout.addLayout(button_layout)

    def run_code(self):
        code = self.text_area.toPlainText()
        lexer = Lexer(code)
        parser = Parser(lexer)
        self.turtle_widget.reset_turtle() # إعادة تعيين السلحفاة قبل كل تشغيل
        try:
            tree = parser.parse()
            output = self.interpreter.interpret(tree)
            self.show_output(output)
        except Exception as e:
            self.show_output(f"خطأ في التنفيذ:\n{str(e)}")

    def clear_editor(self):
        self.text_area.clear()
        self.output_area.clear()
        self.turtle_widget.reset_turtle() # مسح الرسم أيضاً عند مسح المحرر

    def clear_drawing(self):
        self.turtle_widget.clear()

    def show_output(self, text):
        self.output_area.setPlainText(text)

    def load_code(self):
        path, _ = QFileDialog.getOpenFileName(self, "فتح ملف", "", "AR Code (*.arcode);;All Files (*)")
        if path:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                self.text_area.setPlainText(content)
            self.output_area.clear() # مسح الإخراج عند تحميل ملف جديد
            self.turtle_widget.reset_turtle() # مسح الرسم أيضاً

    def save_code(self):
        path, _ = QFileDialog.getSaveFileName(self, "حفظ ملف", "", "AR Code (*.arcode);;All Files (*)")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.text_area.toPlainText())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ArabicLangApp()
    ex.show()
    sys.exit(app.exec_())