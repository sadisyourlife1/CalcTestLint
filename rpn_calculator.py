import operator
import re


class RPNSyntaxError(Exception):
    """Ошибка синтаксиса во входном выражении"""
    pass


class RPNCalculator:
    """Калькулятор, использующий обратную польскую запись (ОПЗ)"""

    OPERATORS = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
    }

    PRIORITY = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2,
    }

    def __init__(self):
        self.stack = []
        self.output = []
        self.operators = []

    def parse_expression(self, expression):
        """Разбирает выражение и преобразует в ОПЗ"""
        self._validate_expression(expression)
        tokens = self._tokenize(expression)

        self.output = []
        self.operators = []

        for token in tokens:
            if self._is_number(token):
                self.output.append(float(token))
            elif token in self.OPERATORS:
                while (self.operators and
                       self.operators[-1] != '(' and
                       self.PRIORITY[self.operators[-1]] >= self.PRIORITY[token]):
                    self.output.append(self.operators.pop())
                self.operators.append(token)
            elif token == '(':
                self.operators.append(token)
            elif token == ')':
                while self.operators[-1] != '(':
                    self.output.append(self.operators.pop())
                if self.operators[-1] == '(':
                    self.operators.pop()

        while self.operators:
            self.output.append(self.operators.pop())

        return self.output

    def evaluate(self, expression):
        """Вычисляет значение выражения"""
        rpn = self.parse_expression(expression)
        stack = []

        for token in rpn:
            if isinstance(token, float):
                stack.append(token)
            else:
                if len(stack) < 2:
                    raise RPNSyntaxError("Недостаточно операндов для операции")
                b = stack.pop()
                a = stack.pop()
                try:
                    result = self.OPERATORS[token](a, b)
                except ZeroDivisionError:
                    raise ValueError("Деление на ноль")
                stack.append(result)

        if len(stack) != 1:
            raise RPNSyntaxError("Ошибка в выражении")

        return stack[0]

    def _tokenize(self, expression):
        """Разбивает выражение на токены"""
        # Удаляем все пробелы
        expr = expression.replace(' ', '')
        # Используем регулярное выражение для разбиения на токены
        tokens = re.findall(r"(\d+\.?\d*|[-+*/()])", expr)
        return tokens

    def _is_number(self, token):
        """Проверяет, является ли токен числом"""
        try:
            float(token)
            return True
        except ValueError:
            return False

    def _validate_expression(self, expression):
        """Проверяет выражение на корректность"""
        if not expression:
            raise RPNSyntaxError("Пустое выражение")

        # Проверка на недопустимые символы
        valid_chars = r'[\d+\-*/()\.\s]'
        for char in expression:
            if not re.match(valid_chars, char):
                raise RPNSyntaxError(f"Недопустимый символ: '{char}'")

        # Проверка сбалансированности скобок
        balance = 0
        for char in expression:
            if char == '(':
                balance += 1
            elif char == ')':
                balance -= 1
                if balance < 0:
                    raise RPNSyntaxError("Несбалансированные скобки")
        if balance != 0:
            raise RPNSyntaxError("Несбалансированные скобки")


def main():
    """Основная функция для взаимодействия с пользователем"""
    calculator = RPNCalculator()
    print("Калькулятор (для выхода введите 'q')")

    while True:
        try:
            expression = input("Введите выражение: ").strip()
            if expression.lower() == 'q':
                break

            result = calculator.evaluate(expression)
            print(f"Результат: {result}")

        except (RPNSyntaxError, ValueError) as e:
            print(f"Ошибка: {e}")
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")


if __name__ == "__main__":
    main()
