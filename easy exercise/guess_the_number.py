#_*_encoding:gb2312_*_
#-------------------------------------------------------------------------------
# Name:        guess the number
# Purpose:     �������һ��0-9�����֣�����3�λ������£��¶Ե�����you are very good!
#
# Author:      xlm
#
# Created:     30/07/2014
# Copyright:   (c) xlm 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from random import randint,choice

#�������һ��0-9������
target=choice(range(10))
target=6
n=0
#
a=int(raw_input('��³�����Ҫ������,��Χ0-9��'))

while a<>target:
    n=n+1
    if n>=3:
        print '��û�л�����!'
        break

    if a>target:
        a=int(raw_input( '������ִ��ˣ�����������'))
    else:
        a=int(raw_input( '�������С�ˣ�����������'))


else:
    print '��̫NB��!'


