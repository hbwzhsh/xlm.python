#_*_encoding:gb2312_*_
#-------------------------------------------------------------------------------
# Name:
# Purpose:
#
# Author:      xlm
#
# Created:     21/02/2014
# Copyright:   (c) xlm 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from operator import add,sub
from random import randint,choice

d_ops={'+':add,'-':sub}
v_max_times=2

def jisuan():
    v_op=choice('+-')  #ѡ������һ��+or-
    l_nums=[randint(1,10) for i in range(2)]
    v_text='%d %s %d='%(l_nums[0],v_op,l_nums[1])
    answer=d_ops[v_op](*l_nums) #�� #add������ʹ���� add(1,3)#l_nums�ǲ�����list,
    v_times=0;
    while 1:
        try:
            v_times+=1
            if int(raw_input(v_text))==answer:
                print '��ȷ'
                break
            else:
                print '�𰸴���,�㻹��%d�λ���'%(v_max_times-v_times)
            if v_times==v_max_times:
                print '���Ѿ�û�л�����'
                break

        except:
            print '�����������ȷ����'

def main():
    while 1:
        jisuan()
        try:
            flag=raw_input('again?[y]')
            if flag=='y' or flag=='Y':
                continue
            else:
                break
        except:
            break
if __name__ == '__main__':
    main()