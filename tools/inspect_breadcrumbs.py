with open('nsejs/chemistry/core1/recovery/chem-atomic-structure-r1/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('core1-recovery.html')
print('Snippet from chem-atomic-structure-r1:')
print(text[idx-100:idx+200])

with open('nsejs/physics/core1/recovery/nsejs-mechanics-r1/index.html', 'r', encoding='utf-8') as f:
    text2 = f.read()

idx2 = text2.find('core1-recovery.html')
print('Snippet from nsejs-mechanics-r1:')
print(text2[idx2-100:idx2+200])
