"""скрипт для чтения вопросов из xlsx и записи в json"""
import json

from openpyxl import load_workbook


wb = load_workbook('excel_files/quiz.xlsx')
ws = wb.active

questions = []
for row in ws:
    questions.append({
        'text': row[0].value,
        'answer': str(row[1].value),
        'complexity': row[2].value,
        'category': row[3].value,
    })

with open('questions.json', 'w') as f:
    json.dump(questions, f)
