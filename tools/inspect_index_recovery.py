with open('nsejs/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('core1-recovery.html')
print('Snippet from nsejs/index.html:')
print(text[idx-200:idx+300])
