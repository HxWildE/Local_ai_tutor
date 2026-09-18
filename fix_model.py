file_path = 'app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('gemini-1.5-flash', 'gemini-flash-latest')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated app.py')
