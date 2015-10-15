#-------------------------------------------------------------------------------
# Name:        urlretrieve
# Purpose:
#
# Author:      xlm
#
# Created:     24/02/2014
# Copyright:   (c) xlm 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import urllib
def callbackfunc(blocknum, blocksize, totalsize):
    '''�ص�����
    @blocknum: �Ѿ����ص����ݿ�
    @blocksize: ���ݿ�Ĵ�С
    @totalsize: Զ���ļ��Ĵ�С
    '''
    percent = 100.0 * blocknum * blocksize / totalsize
    if percent > 100:
        percent = 100
    print "%.2f%%"% percent

url = 'http://www.sina.com.cn'
local = 'd:\\sina.html'
res=urllib.urlretrieve(url, local, callbackfunc)
print res  #����ֵ��ӡ

