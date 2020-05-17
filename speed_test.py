#from PIL import Image
#from matplotlib import pylab
#from time import time
#from ImageEngine import ElipsAva, WritePersProfile

#tik = time()
#image_city_map = Image.open('materials_bot/Market.jpg')
#tok = time()
#print(tok-tik)

#tik = time()
#image_city_map1 = pylab.imread('materials_bot/Market.jpg')
#tok = time()
#print(tok-tik)

#ElipsAva(1,2)
#state_list=["Иван", "1", "100", "255", "100%", "99%", "80%", "30%", "12%","23%"]
#WritePersProfile(state_list)
from operator import itemgetter

a = [
    [80,17,23,14,16],
    [83,12,21,17,114],
    [81,12,23,14,11],
]

a.append([19,32,13,421,561])
print(a)