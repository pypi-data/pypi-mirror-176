from utf_table_generator.table import Table

titles = ('number', 'float', 't', 'boolean', 'a')
variables = (123, 12345.4564876435, 'test', True, 1)
t = Table(titles, variables, precision=3)  # precision -- количество знаков после запятой, по умолчанию 5
print(t.get_code())

print("╔" + "═" * 8 + "╦" + "═" * 13 + "╦" + "═" * 7 + "╦" + "═" * 9 + "╦" + "═" * 4 + "╗")
print("║%7s ║%12s ║%6s ║%8s ║%3s ║" % ("number", "float", "t", "boolean", "a"))
print("╠" + "═" * 8 + "╬" + "═" * 13 + "╬" + "═" * 7 + "╬" + "═" * 9 + "╬" + "═" * 4 + "╣")
print("║%7d ║%12.3f ║%6s ║%8s ║%3d ║" % variables)
print("╚" + "═" * 8 + "╩" + "═" * 13 + "╩" + "═" * 7 + "╩" + "═" * 9 + "╩" + "═" * 4 + "╝")
