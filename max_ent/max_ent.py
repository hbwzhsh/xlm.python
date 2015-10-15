#-------------------------------------------------------------------------------
# Name:        ģ��1
# Purpose:
#
# Author:      xlm
#
# Created:     05/03/2014
# Copyright:   (c) xlm 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

# -*- coding:utf8 -*-
import math
import sys

def load_data(fname):
        """
                ���ļ�����ѵ�����������
                ���صõ����������x���������y��
                �Լ�x��ά���������ֵx_max��y�����ֵy_max������ȷ��x,y��ȡֵ��Χ�����Ƕ�����ɢֵ��
        """
        f = open(fname)
        y=[]
        x=[]
        for line in f: #����line=f.readlines()
                line=line.strip('\n')  #trim
                str_list=line.split(' ')
                xi=[]
                for v in str_list:  #v=c5 , f20
                        if v[0] == 'c':
                                yi=v[1:]
                                y.append(int(yi))
                        if v[0] == 'f':
                                xij=v[1:]
                                xi.append(int(xij))
                x.append(xi)  #x�Ǿ���
        f.close()
        y_max=1
        for yval in y:
                if yval > y_max:
                        y_max=yval
        x_max=[]
        for a in x[0]:
                x_max.append(a)
        for b in x:
                for i in range(len(b)):
                        if b[i] > x_max[i]:
                                x_max[i] = b[i]
        return x,y,x_max,y_max

# �������������Ӧ�Ĳ���

class FeatureParam:
        def __init__(self,ft_index,y_int,x_int):
                self.w=0.0
                self.ft_index=ft_index
                self.y_int=y_int
                self.x_int=x_int
        def feature_func(self,xvec,y): #�������������x=xi and y=yi��1
                if y == self.y_int and xvec[self.ft_index] == self.x_int:
                        return 1
                else:
                        return 0

def init_feature_func_and_param(x_max_vec,y_max):
        # ������������:
        # ÿ����ͬ��<����i������ֵ��ֵv�������ǩlabel��ֵc>��Ԫ�鶼ȷ��һ����������f
        # f(x,y)��������x�ĵ�iά=v����y=cʱ����������ֵΪ1������Ϊ0.
        fvec=[]
        ft_index=-1
        for x_max in x_max_vec:
                ft_index+=1
                for xval in range(0,x_max+1):
                        for yval in range(1,y_max+1):
                                fp=FeatureParam(ft_index,yval,xval)
                                fvec.append(fp)
        return fvec

def estimated_except_feature_val(x_mat,y_vec,fparam):
        esti_efi = 0.0
        n_data=len(y_vec)
        # ��ÿ��ѵ�����ݵ���������ֵ���
        # ����ѵ���������������þ���������������ֵ
        for i in range(n_data):
                x_vec = x_mat[i]
                esti_efi += fparam.feature_func(x_vec,y_vec[i])
        # perhaps there's no data match the feature function
        # to make the computation possible, let it be a small float number
        if esti_efi == 0.0:
                esti_efi = 0.0000001
        esti_efi /= 1.0*n_data
        return esti_efi

def max_ent_predict_unnormalized(x_vec,y,fvec):
        """
                δ��һ���ĸ���ֵ
                ������������ֵ�ļ�Ȩ��
                ��Ȩϵ������ģ��ѵ�������Ĳ���
        """
        weighted_sum=0.0
        for fparam in fvec:
                weighted_sum += fparam.w * fparam.feature_func(x_vec,y)
        return math.exp(weighted_sum)

def max_ent_normalizer(x_vec,y_max,fvec):
        zw=0.0
        for y in range(1,y_max+1):
                zw += max_ent_predict_unnormalized(x_vec,y,fvec)
        return zw

def model_except_feature_val(x_mat,y_max,fparam,fvec,p_cached):
        data_size=len(x_mat)
        efi=0.0
        index=0
        ix=-1
        # �Ը�ѵ������x�������п��ܵ�y��ȡֵ����P(y|x)����������ֵ�ĳ˻���
        # ������ƽ��ֵ
        # ����ģ�͵�Ԥ��������������ֵ
        for x_vec in x_mat:
                ix += 1
                zw=0.0
                tmp_efi=0.0
                for y in range(1,y_max+1):
                        # compute p(y|x) at current w
                        # in same iteration, p(y|x) not change, so can cache it
                        if index < len(p_cached):
                                p_y_given_x = p_cached[index]
                        else:
                                p_y_given_x = max_ent_predict_unnormalized(x_vec,y,fvec)
                                p_cached.append(p_y_given_x)
                        zw += p_y_given_x
                        tmp_efi += p_y_given_x * fparam.feature_func(x_vec,y)
                        index+=1
                tmp_efi /= zw
                efi += tmp_efi
        efi /= data_size
        if efi == 0.0:
                efi = 0.0000001
        return efi

def feature_func_sum(fvec,xvec,y):
        m = 0.0
        for f in fvec:
                m += f.feature_func(xvec,y)
        return m

def update_param(x_mat,y_vec,y_max,fvec):
        """
                ����ÿ������������Ӧ�Ĳ���:
                x_mat: ѵ�����ݵ��������
                y_vec: ѵ�����ݵ�label����
                y_max: label�����ȡֵ��labelȡֵ��ΧΪ[1,y_max]
                fvec: ������������Ӧ������ɵ�����
        """
        # ��������������ֵ��ӣ��Բ�ͬ��x,y��˵������һ������
        m = feature_func_sum(fvec,x_mat[0],y_vec[0])
        # �Ƿ�����
        convergenced = True
        # ��������������ά��ƽ���ͣ���ģ��ƽ��
        sigma_sqr_sum=0.0
        # ���º�Ĳ���
        w_updated=[]
        # ����P(y|x)�Ľ���������ظ�����
        p_cached=[]
        # ��ÿһ�������������ֱ���¶�Ӧ�Ĳ���
        for fparam in fvec:
                # ����ѵ�����ݵ���������ƽ��ֵ
                esti_efi = estimated_except_feature_val(x_mat,y_vec,fparam)
                # ���㵱ǰģ�͵�������������ֵ
                efi = model_except_feature_val(x_mat,y_max,fparam,fvec,p_cached)
                # ���㵱ǰ�����ĸ���ֵ
                # ����m�Ǹ����������Կ��������ַ�������
                sigma_i= math.log(esti_efi/efi) / m
                w_updated.append(fparam.w + sigma_i)
                # ����Բ����ĸ��½ϴ�����Ϊ������
                if abs(sigma_i/(fparam.w+0.000001)) >= 0.10:
                        convergenced = False
                sigma_sqr_sum += sigma_i*sigma_i
        i=0
        for fparam in fvec:
                fparam.w = w_updated[i]
                i+=1
        # ��ӡ��ǰ���������ĳ���
        print("sigma_len=%f"%math.sqrt(sigma_sqr_sum))
        return convergenced

def log_likelihood(x_mat,y_vec,y_max,fvec):
        """
                ԭ����p�ж������ֵ������ѡ��ʱ�����ǻ�ѡȡ����ֵ��Ϊ����ֵ������Ǽ�����Ȼ���Ʒ���
                ���������ϸ����ܶ�Ϊ����f,���ǳ�Ϊ��Ȼ����.�������һ������xʹ����Ȼ���������ô���ֵ���������Ȼ���Ʒ�
                ��ÿ��ѵ�����ݵ�x������ģ��Ԥ�����P(y|x)��
                ��˲�ȡ���������ö�����Ȼ����ֵ��
                ��ֵԽ��˵��ģ�Ͷ�ѵ�����ݵ����Խ׼ȷ
        """
        ix=-1
        log_likelihood = 0.0
        data_size = len(x_mat)  #����x���������
        for i in range(data_size):
                x_vec = x_mat[i]
                y = y_vec[i]
                log_likelihood += math.log(max_ent_predict_unnormalized(x_vec,y,fvec))
                log_likelihood -= math.log(max_ent_normalizer(x_vec,y_max,fvec))
        log_likelihood /= data_size
        return log_likelihood

def max_ent_train(x_matrix,y_vec,x_max_vec,y_max):
        """
                �����ģ��ѵ����ʹ��IIS(improved iterative scaling)�����㷨
        """
        fvec = init_feature_func_and_param(x_max_vec,y_max)
        iter_time=0
        while True:
                # ���²���,�����Ƿ�����
                convergenced=update_param(x_matrix,y_vec,y_max,fvec)
                # ���������Ȼֵ
                log_lik=log_likelihood(x_matrix,y_vec,y_max,fvec)
                print("log_likelihood=%0.12f"%log_lik)
                if convergenced:
                        break
                iter_time+=1
                if iter_time >= 100000:
                        break
        # ��ѵ���õ���ģ��д���ļ���һ��һ������
        fmodel=open('E:\python\python��ϰ\max_ent\model.txt','w')
        for fparam in fvec:
                fmodel.write(str(fparam.w))
                fmodel.write('\n')
        fmodel.close()
        print("Max-ent train ok!")

def load_model():
        """
                ������ѵ���õ������ģ��
        """
        x_mat,y_vec,x_max_vec,y_max=load_data("E:\python\python��ϰ\max_ent\zoo.train")
        fvec = init_feature_func_and_param(x_max_vec,y_max)
        fmod=open('E:\python\python��ϰ\max_ent\model.txt')
        i=-1
        for line in fmod:
                i+=1
                line=line.strip('\n')
                fvec[i].w=float(line)
        fmod.close()
        return fvec,y_max

def max_ent_test():
        fvec,y_max = load_model()
        x_mat_test,y_vec_test,x_max_vec_test,y_max_test=load_data("E:\python\python��ϰ\max_ent\zoo.test")
        test_size=len(x_mat_test)
        ok_num=0
        for i in range(test_size):
                x_vec=x_mat_test[i]
                y=y_vec_test[i]
                most_possible_predict_y=0
                max_p=0.0
                sum_p=0.0
                for predict_y in range(1,y_max+1):
                        p = max_ent_predict_unnormalized(x_vec,predict_y,fvec)
                        sum_p += p
                        if p > max_p:
                                most_possible_predict_y = predict_y
                                max_p = p
                if y == most_possible_predict_y:
                        ok_num += 1
                p_normalized = max_p / sum_p
                print("y=%d predict_y=%d p=%f"%(y,most_possible_predict_y,p_normalized))
        print("precision-ratio=%f"%(1.0*ok_num/test_size))

if __name__=="__main__":
        flag =raw_input('train?or test?' )
        if flag=='train':
                # �����ģ��ѵ��
                # ѵ������zoo.train,ģ��������ļ�model.txt
                x_matrix,y_list,x_max_list,y_max=load_data("E:\python\python��ϰ\max_ent\zoo.train")
                max_ent_train(x_matrix,y_list,x_max_list,y_max)

        if flag=='test':
                # �����ģ�Ͳ���
                max_ent_test()