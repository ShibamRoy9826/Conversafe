from random import shuffle
import string

s=string.ascii_letters+string.digits

a=[x for x in s]
shuffle(a)
newString=""

for i in a:
	newString+=i
	
print(newString[:16])