# -*- coding:gb2312 -*-
import re
import urllib

#��Դ����
def get_html(url):
    try:
        page=urllib.urlopen(url)
        html=page.read()
        page.close()
        return html
    except:
        return None
#����html
def dowload_html(url,filename):
    try:
        #urllib.urlretrieve(url,'%s.html' %(filename))
        html=get_html(url)
        f=open(filename,'w')
        if not str.strp(html):
            pass
        else:
            f.write(html)
    except:
        f.close()



#ͨ��html���ݻ�ȡurl�б�,pattern Ϊ������ʽ
def getUrls(html,pattern):
    try:
        reg=re.compile(pattern)
        urls=re.findall(reg,html)
        return urls
    except:
        print 'getUrls fail'
        return []

#ͨ��url��ȡhtml,��ͨ��html��ȡurl�б�,pattern Ϊ������ʽ
def getUrls_2(url,pattern):
    try:
        html=get_html(url)
        reg=re.compile(pattern)
        urls=re.findall(reg,html)
        return urls
    except:
        print 'getUrls fail'
        return []

#�������
def spider(start_url,pattern):
##    try:
        i=0
        urls=[] #url�б� �� 
        #��hash����ã��� {},�ں����ж��Ƿ����ʱ���� urls.has_key()��Ч�ʸ��ߡ�
        #��Ϊlist�ߵ��Ǳ��������ֵ���hash
        v_url=start_url
        urls.append(v_url)
        #��url����һ���б�
        while i<=200 and i<len(urls):
            v_url=urls[i]
            if v_url:
                dowload_html(v_url,'E:\\temp\%s.html'%(str(i))) #����html
                print str(i)+'_'+v_url
                #������ҳ��ȡurl
                urllist=getUrls_2(v_url,pattern)
                for cr_url in urllist:
                    if urls.count(cr_url)==0:   #����б��Ѿ����ڸõ�ַ���򲻲��룬�������
                        urls.append(cr_url)
            i+=1
            print len(urls)

##    except:
##        print urls.index(v_url)




start_url='http://blog.sina.com.cn/u/2130809547'
reg=r'href="(http://blog\.sina\.com\.cn/s/blog.+?\.html)"'
spider(start_url,reg)

