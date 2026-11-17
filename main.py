import re

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty

KV = '''
<CalcButton@Button>:
    font_size: '24sp'
    background_normal: ''
    background_color: (0.10, 0.15, 0.24, 1)
    color: (1,1,1,1)
    bold: True

BoxLayout:
    orientation: 'vertical'
    padding: '14dp'
    spacing: '10dp'
    canvas.before:
        Color:
            rgba: (0.035, 0.055, 0.09, 1)
        Rectangle:
            pos: self.pos
            size: self.size
    Label:
        text: 'ماشین حساب'
        font_name: 'Roboto'
        font_size: '25sp'
        bold: True
        color: (0.35, 0.72, 1, 1)
        size_hint_y: .14
    Label:
        text: app.display
        font_size: '34sp'
        halign: 'right'
        valign: 'middle'
        text_size: self.size
        color: (1,1,1,1)
        size_hint_y: .22
    GridLayout:
        cols: 4
        spacing: '8dp'
        size_hint_y: .64
        CalcButton:
            text: 'AC'
            on_release: app.clear()
        CalcButton:
            text: '⌫'
            on_release: app.backspace()
        CalcButton:
            text: '%'
            on_release: app.add('%')
        CalcButton:
            text: '÷'
            background_color: (0.05, 0.35, 0.58, 1)
            on_release: app.add('/')
        CalcButton:
            text: '7'
            on_release: app.add('7')
        CalcButton:
            text: '8'
            on_release: app.add('8')
        CalcButton:
            text: '9'
            on_release: app.add('9')
        CalcButton:
            text: '×'
            background_color: (0.05, 0.35, 0.58, 1)
            on_release: app.add('*')
        CalcButton:
            text: '4'
            on_release: app.add('4')
        CalcButton:
            text: '5'
            on_release: app.add('5')
        CalcButton:
            text: '6'
            on_release: app.add('6')
        CalcButton:
            text: '−'
            background_color: (0.05, 0.35, 0.58, 1)
            on_release: app.add('-')
        CalcButton:
            text: '1'
            on_release: app.add('1')
        CalcButton:
            text: '2'
            on_release: app.add('2')
        CalcButton:
            text: '3'
            on_release: app.add('3')
        CalcButton:
            text: '+'
            background_color: (0.05, 0.35, 0.58, 1)
            on_release: app.add('+')
        CalcButton:
            text: '±'
            on_release: app.negate()
        CalcButton:
            text: '0'
            on_release: app.add('0')
        CalcButton:
            text: '.'
            on_release: app.add('.')
        CalcButton:
            text: '='
            background_color: (0.0, 0.48, 0.78, 1)
            on_release: app.calculate()
'''

class RaminCalculator(App):
    display = StringProperty('0')

    def build(self):
        self.expression = ''
        return Builder.load_string(KV)

    def add(self, value):
        if self.display == 'خطا':
            self.clear()

        if value == '%':
            match = re.search(r'(\d+(?:\.\d*)?|\.\d+)$', self.expression)
            if not match:
                return
            number = match.group(1)
            prefix = self.expression[:match.start()]
            if (prefix.endswith(('+', '-')) and len(prefix) > 1
                    and prefix[-2] not in '+-*/('):
                operator = prefix[-1]
                left = prefix[:-1]
                percent = f'(({left})*({number})/100)'
                self.expression = f'{left}{operator}{percent}'
            else:
                self.expression = f'{prefix}({number}/100)'
        else:
            self.expression += value

        self.display = self.expression or '0'

    def clear(self):
        self.expression = ''
        self.display = '0'

    def backspace(self):
        self.expression = self.expression[:-1]
        self.display = self.expression or '0'

    def negate(self):
        if not self.expression:
            return
        if self.expression.startswith('-(') and self.expression.endswith(')'):
            self.expression = self.expression[2:-1]
        else:
            self.expression = f'-({self.expression})'
        self.display = self.expression

    def calculate(self):
        try:
            allowed = set('0123456789+-*/.() ')
            if not self.expression or any(c not in allowed for c in self.expression):
                raise ValueError('invalid')
            result = eval(self.expression, {'__builtins__': {}}, {})
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            self.expression = str(result)
            self.display = self.expression
        except Exception:
            self.expression = ''
            self.display = 'خطا'

if __name__ == '__main__':
    RaminCalculator().run()
