a_rubli = 10 #int(input('Ã±ÃªÃ®Ã«Ã¼ÃªÃ® Ã°Ã³Ã¡Ã«Ã¥Ã© Ã±Ã²Ã®Ã¨Ã² Ã¯Ã¨Ã°Ã®Ã¦Ã®Ãª'))
b_coins = 15 #int(input('Ã±ÃªÃ®Ã«Ã¼ÃªÃ® ÃªÃ®Ã¯Ã¥Ã¥Ãª Ã±Ã²Ã®Ã¨Ã² Ã¯Ã¨Ã°Ã®Ã¦Ã®Ãª'))
n_cake = 2#int(input('Ã±ÃªÃ®Ã«Ã¼ÃªÃ® Ã¯Ã¨Ã°Ã®Ã¦ÃªÃ®Ã¢ Ã­Ã³Ã¦Ã­Ã® ÃªÃ³Ã¯Ã¨Ã²Ã¼'))

a_coins = a_rubli * 100
print(a_coins)
vsego = (a_coins+b_coins)/n_cake
vrublyah = ((a_coins+b_coins)/n_cake)//100
print(vsego)
print(vrublyah)
#print(((a_coins+b_coins)/n_cake)//100, ((a_coins+b_coins)/n_cake)%100)