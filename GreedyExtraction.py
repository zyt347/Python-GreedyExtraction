#!/usr/bin/env python
#-*encoding:utf-8*-
from math import *
import random

data=[random.uniform(15,16) for _ in range(100)] #用来测试的列表
#################################################################

def std(n,F):#计算标准差，等同于=numpy.std(n,ddof=1)；n必须是"list";F是设置保留标准差小数位
    sum=0
    for i in n:sum+=i
    sum_m=sum/len(n)
    sum_dd=0
    for j in n: sum_dd=sum_dd+pow(j-sum_m,2)
    sum_d=pow(sum_dd/(len(n)-1),0.5)
    sum_d="{0:.{1}f}".format(sum_d,F)
    return sum_d

def getEffe(initial_data,difference,Minimum=3,limit_l=-99999,limit_u=99999):
    #initial_data:需要处理的列表
    #limit_l&limit_u：设置有效数据区间
    #difference：设置提取数据的差异值范围
    if Minimum < 3: #最终筛选出的元素最小个数
        raise(ValueError("Minimum>2"))
    if difference <= 0: #差值必须为正数
        raise(ValueError("difference>0"))
    
    b=initial_data[:]
    b.sort()
    b=[float(i) for i in b if limit_l<i<limit_u]
    filter1=[]
    for l in range(0,len(b)-1,2):
        if b[l+1]-b[l] <= difference:
            filter1.append(b[l])
            filter1.append(b[l+1])
    if len(filter1) < Minimum:
        return 
    node=[0]
    for n in range(len(filter1)-1):
        if filter1[n+1]-filter1[n] > difference:
            node.append(n+1)
    if len(node) == 2:
        return filter1
    else:
        node.append(len(filter1))
        filter2=[filter1[node[i]:node[i+1]] for i in range(len(node)-1)]
        filter2=[i for i in filter2 if len(i) >= Minimum ]
        for groupnode in filter2:
            while groupnode[-1]-groupnode[0] > difference:
                if groupnode[Minimum-1]-groupnode[0] > difference:
                    groupnode.remove(groupnode[0])
                elif groupnode[-1]-groupnode[-Minimum] > difference:
                    groupnode.remove(groupnode[-1])
                else:
                    tmp1=[i for i in groupnode if i <= groupnode[0]+difference]
                    tmp2=[i for i in groupnode if i >= groupnode[-1]-difference]
                    if len(tmp1) < len(tmp2):
                        groupnode.remove(groupnode[0])
                    elif len(tmp1) > len(tmp2):
                        groupnode.remove(groupnode[-1])
                    else:
                        if std(tmp1,2) < std(tmp2,2):
                            groupnode.remove(groupnode[0])
                        elif std(tmp1,2) > std(tmp2,2):
                            groupnode.remove(groupnode[-1])
                        else:
                            T=0
                            for t in groupnode:T+=t
                            G_mean=float(T/len(groupnode))
                            if G_mean-groupnode[0] > groupnode[-1]-G_mean:
                                groupnode.remove(groupnode[0])
                            elif G_mean-groupnode[0] < groupnode[-1]-G_mean:
                                groupnode.remove(groupnode[-1])
                            else:
                                print("Unknow:%s&%s"%(str(tmp1,tmp2)))
                                return
        filter2=[i for i in filter2 if len(i) >= Minimum ]
        if not filter2:
        	return
        else:
        	lenList=[len(i) for i in filter2 ]
        	Maxlen=max(lenList)
        	filter2=[ i for i in filter2 if len(i)==Maxlen]
        	if len(filter2) == 1:
        	    return filter2[0]
        	else:
        	    f2std_l=[std(i,2) for i in filter2]
        	    stdmin=min(f2std_l)
        	    filter2=[i for i in filter2 if std(i,2) == stdmin]
        	    if len(filter2) == 1:
        	    	return filter2[0]
        	    else:
					b_mean=eval("("+"+".join([str(i) for i in b])+")/len(b)")
					for indexF2 in range(len(filter2)-1):
						tmp1_m=eval("("+"+".join([str(i) for i in filter2[indexF2]])+")/len(filter2[indexF2])")
						tmp2_m=eval("("+"+".join([str(i) for i in filter2[indexF2+1]])+")/len(filter2[indexF2])")
						if abs(tmp1_m-b_mean) > abs(tmp2_m-b_mean):
							filter2.remove(filter2[indexF2])
	
						elif abs(tmp1_m-b_mean) < abs(tmp2_m-b_mean):
							filter2.remove(filter2[indexF2+1])
	
						else:
							print("Unknow:%s"%(str(filter2)))
							return
        			
					if len(filter2) == 1:
						return filter2[0]
					else:
						print("Unknow:%s"%(str(filter2)))
						return

a=getEffe(data,0.03,3)
print(a)
