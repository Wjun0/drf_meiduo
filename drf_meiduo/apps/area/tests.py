from django.test import TestCase

# Create your tests here.


list = [1,2,3,4]
new_list = []
for index,value in enumerate(list):
    new_list.append(value)
    if value == 4:
        print(new_list[index-1])