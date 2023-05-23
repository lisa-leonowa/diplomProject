"""
Дипломный проект по специальности 09.02.07 «Информационные системы и программирование»
по теме «Разработка программной системы управления клиентами предприятия ООО «Кибер класс»».
Название: manage.py.
Разработал: Леонова Е. А., группа ТИП-81.
Дата и номер версии: 19.05.2023 v3.0.
Язык: Python.
Краткое описание:
Данный модуль отвечает за запуск сервера Системы управления клиентами.

Сторонние библиотеки, используемые в программе:
os – модуль, для работы с Операционной системой;
sys - модуль, позволяющий на прямую работать с интерпретатором;
"""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diplomLeonova.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
