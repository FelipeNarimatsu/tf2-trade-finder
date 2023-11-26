import os
os.remove('items_names.txt') 

f1 = open('items.txt', 'r') 
f2 = open('items_names.txt', 'a+')


full_text = f1.read()
full_text = full_text.split('<span class="item-name">')

first_line_jump = True
for line in full_text:
    if(first_line_jump != True):
        item_name = line.split('</span>',1)[0]
        # if("#" in item_name):
        #    break
        print(item_name)
        f2.write(item_name+'\n')
    first_line_jump = False

f1.close()
f2.close()
