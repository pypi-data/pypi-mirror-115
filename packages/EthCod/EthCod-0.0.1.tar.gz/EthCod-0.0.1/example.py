from random import randrange
from time import time
from . import Generator

try:
    from web3.auto.infura import w3
except:
    print("You first need to type:")
    exit("export WEB3_INFURA_PROJECT_ID=*******FIND YOUR PROJECT ID*****; export WEB3_INFURA_API_SECRET=*******FIND YOUR PROJECT SECRET*****")

start = time()
for i in range(3):
    data = Generator(randrange(0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF))
    addr = data[0]
    key = data[1]
    b = w3.eth.getBalance(addr)
    if b != 0:
        f = open('keys.txt', 'a')
        f.write('\n|' + key + '_' + addr)
        f.close()
        print('Found!')

print(time()-start)
