### Краткое описание того, как будут описано ревью:
### 1) Все строки ревью начинаются с "###", отступов от начала строки
### нет, соответственно, для того, чтобы прочитать все комментарии,
### можно воспользоваться поиском по "###".
### 2) Перед текстом программы будет общие замечания/советы.
### 3) Внутри программы комментарий ревью пишется перед строкой
### к которой этот комментарий относится.


### Общие советы/замечания:
### Не хватает комментариев к программе. Представьте, что вы сейчас
### работаете программистом в компании, где приняты такие стандарты для
### документирования программ. Большую часть рабочего времени вместо
### использования написанными вашими коллегами инструментами, вам
### придётся полностью перечитывать код и разбираться, как его 
### использовать, какие аргументы передавать в функции. Это совсем 
### неудобно.
### Могу посоветовать почитать, например, про Docstrings
### Например - https://habr.com/ru/post/499358/
### Также посоветую аннотировать типы
### Например - https://habr.com/ru/company/lamoda/blog/432656/

import datetime as dt


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
### Такое разделение на строке, как мне кажется, не особо удобно
### Нужно суметь заметить if в конце строки, при этом not
### "повис" в отдельной строке. Можно, например, отделить по строкам
### значение, if часть и else часть тернарного оператора
### date.now().date() - нехорошо использовать. Есть date.today()
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        for Record in self.records:
### ниже использован более правильное описание для такого -
### не нужно на каждой итерации вычислять "сегодня"
            if Record.date == dt.datetime.now().date():
### везде ниже используется "+=", нужно использовать одинаковые решения
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
### Лучше docstrings и лучше комментарий на другой строке.
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        x = self.limit - self.get_today_stats()
        if x > 0:
### Не используем обратный слеш. Если везде используется отступ,
### кратный 4, то лучше этому следовать и здесь
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
### Эта ситуация описана в требованиях к коду явно 
        else:
### лишние скобки
            return('Хватит есть!')


class CashCalculator(Calculator):
### А вот в таких комментариях нет смысла - по имени переменной можно
### понять, что имеется в виду
### Для валюты лучше использовать decimal - float имеет свои "проблемы"
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

### передавать USD_RATE и EURO_RATE не нужно
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
### Очень много действий подряд (без пустых строк). 
### Хочется разделить всё это - придумайте, как это сделать лучше
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
### Категория "совет" (то есть, изменений по этому комментарию вносить
### не надо). Несмотря на то, что такое описание курсов
### требовалось в условии, но если бы на код таких ограничений не
### налагалось, то можно бы было описать dict со всеми курсами. Это
### позволило бы заметно сократить количество строк, да и расширяемость
### нашей программы была бы проще - не надо добавлять в текст программы
### ещё один elif, и работало бы быстрее 
### Совет №2. Хорошим тоном было бы определить поведение, если currency
### это не одно из трёх указанных
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
### Эта строка не имеет смысла
### (посмотрите, что происходит в результате её выполнения)
            cash_remained == 1.00
            currency_type = 'руб'
        if cash_remained > 0:
### Ограничения на f-строки из требования к коду
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
### Если явно запрещено пользоваться else в такой ситуации, наверное,
### лучше elif не использовать также (elif == else if)
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
### Обратный слеш
### Если везде используются f-строки, то, наверное, лучше продолжить
### использовать их
### Если везде отступ кратен 4, то и тут лучше подправить
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

### Зачем этот метод?
    def get_week_stats(self):
        super().get_week_stats()
