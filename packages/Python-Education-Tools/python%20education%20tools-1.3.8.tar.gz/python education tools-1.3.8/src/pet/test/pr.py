content = open('py001.txt', encoding='utf-8').read().splitlines()
con=content[2::4]
open('zm.txt','w',encoding='utf-8').write(''.join(con))


