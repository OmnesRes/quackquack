from itertools import combinations_with_replacement
from itertools import permutations
def one_way(means,sds,sizes):
    x=sum([u*n for u,n in zip(means,sizes)])/sum(sizes)
    sb=sum([n*(u-x)**2 for u,n in zip(means,sizes)])/(len(means)-1)
    sw=sum([(n-1)*s**2 for s,n in zip(sds,sizes)])/(sum(sizes)-len(means))
    return sb/sw



print 'Bottomless Bowls: Why Visual Cues of Portion Size May Influence Intake'
print
print 'Table 1. Biased visual cues unknowingly influence overconsumption'
f1=open('soup.txt')
data=[i.strip().split() for i in f1]
for i in data:
    sizes=[27,27]
    means=[float(i[0]),float(i[2])]
    sds=[float(i[1]),float(i[3])]
    exact_test=one_way(means,sds,sizes)
    ##for min make sds larger, means closer together
    min_sds=[sd+.05 for sd in sds]
    if means[0]<means[1]:
        min_means=[means[0]+.05,means[1]-.05]
    elif means[1]<means[0]:
        min_means=[means[0]-.05,means[1]+.05]
    else:
        min_means=means
    min_test=one_way(min_means,min_sds,sizes)
    ##for max make sds smaller, means farther apart
    max_sds=[sd-.05 for sd in sds]
    if means[0]<means[1]:
        max_means=[means[0]-.05,means[1]+.05]
    elif means[1]<means[0]:
        max_means=[means[0]+.05,means[1]-.05]
    else:
        max_means=[means[0]-.05,means[1]+.05]
    max_test=one_way(max_means,max_sds,sizes)
    print 'Reported:'+'\t'+i[4]+'\t'+'Exact:'+'\t'+str(round(exact_test,2))+\
          '\t'+'Possible:'+'\t'+str(round(min_test,2))+'-'+str(round(max_test,2))



def unequal(means,sds,sizes):
    return (means[0]-means[1])/(sds[0]**2/sizes[0]+sds[1]**2/sizes[1])**.5


import numpy as np
from rpy2 import robjects as ro
import rpy2.robjects.numpy2ri
rpy2.robjects.numpy2ri.activate()
ro.r('library(rpsychi)')

print
print 'Ice Cream Illusions Bowls, Spoons, and Self-Served Portion Sizes'
print
print 'Table 1. How bowl and serving spoon size influence self-served portions'
f1=open('ice_cream.txt')
data=[i.strip().split() for i in f1]
##all possible changes:
combos={}
for combo in combinations_with_replacement([0,.005,-.005],4):
    for permut in permutations(combo):
        combos[permut]=''
ro.globalenv['n']=ro.r.matrix(np.array([20,26,17,22]),nrow=2)
for i in data:
    u=np.array([float(i[0]),float(i[2]),float(i[4]),float(i[6])])
    s=np.array([float(i[1]),float(i[3]),float(i[5]),float(i[7])])
    ro.globalenv['u']=ro.r.matrix(u,nrow=2)
    ro.globalenv['s']=ro.r.matrix(s,nrow=2)
    exact_test=ro.r('ind.twoway.second(u,s,n,digits=10)').rx2('anova.table')[-1]
    
    ##for min test make sds larger
    ro.globalenv['s']=ro.r.matrix(s+.005,nrow=2)
    
    ##for means make all possible changes
    between_row=[]
    between_column=[]
    between_row_column=[]
    for combination in combos:
        ro.globalenv['u']=ro.r.matrix(u+combination,nrow=2)
        test=ro.r('ind.twoway.second(u,s,n,digits=10)')
        between_row.append(test.rx2('anova.table')[-1][1])
        between_column.append(test.rx2('anova.table')[-1][2])
        between_row_column.append(test.rx2('anova.table')[-1][3])
        
    min_row=sorted(between_row)[0]
    min_column=sorted(between_column)[0]
    min_row_column=sorted(between_row_column)[0]

    ##for max test make the sds smaller
    ro.globalenv['s']=ro.r.matrix(s-.005,nrow=2)
    ##for means make all possible changes
    between_row=[]
    between_column=[]
    between_row_column=[]
    for combination in combos:
        ro.globalenv['u']=ro.r.matrix(u+combination,nrow=2)
        test=ro.r('ind.twoway.second(u,s,n,digits=10)')
        between_row.append(test.rx2('anova.table')[-1][1])
        between_column.append(test.rx2('anova.table')[-1][2])
        between_row_column.append(test.rx2('anova.table')[-1][3])
    max_row=sorted(between_row)[-1]
    max_column=sorted(between_column)[-1]
    max_row_column=sorted(between_row_column)[-1]
    print 'Reported:'+'\t'+i[8]+'\t'+i[9]+'\t'+i[10]+'\t'\
          +'Exact:'+'\t'+str(round(exact_test[2],2))+'\t'+str(round(exact_test[1],2))+'\t'+str(round(exact_test[3],2))+'\t'\
          +'Possible:'+'\t'+str(round(min_column,2))+'-'+str(round(max_column,2))+'\t'+\
          str(round(min_row,2))+'-'+str(round(max_row,2))+'\t'+\
          str(round(min_row_column,2))+'-'+str(round(max_row_column,2))

print
print 'How descriptive food names bias sensory perceptions in restaurants'
print
print 'Table 1. Descriptive food names influence sensory perceptions in restaurants'
f1=open('descriptive_table1.txt')
data=[i.strip().split() for i in f1]
for i in data:
    sizes=[56,84]
    means=[float(i[0]),float(i[2])]
    sds=[float(i[1]),float(i[3])]
    exact_test=one_way(means,sds,sizes)
    ##for min make sds larger, means closer together
    min_sds=[sd+.005 for sd in sds]
    if means[0]<means[1]:
        min_means=[means[0]+.005,means[1]-.005]
    elif means[1]<means[0]:
        min_means=[means[0]-.005,means[1]+.005]
    else:
        min_means=means
    min_test=one_way(min_means,min_sds,sizes)
    ##for max make sds smaller, means farther apart
    max_sds=[sd-.005 for sd in sds]
    if means[0]<means[1]:
        max_means=[means[0]-.005,means[1]+.005]
    elif means[1]<means[0]:
        max_means=[means[0]+.005,means[1]-.005]
    else:
        max_means=[means[0]-.005,means[1]+.005]
    max_test=one_way(max_means,max_sds,sizes)
    print 'Reported:'+'\t'+i[4]+'\t'+'Exact:'+'\t'+str(round(exact_test,2))+\
          '\t'+'Possible:'+'\t'+str(round(min_test,2))+'-'+str(round(max_test,2))


print
print 'Table 2. There were no differences betwen the two samples of consumers'
f1=open('descriptive_table2.txt')
data=[i.strip().split() for i in f1]
for i in data:
    sizes=[56,84]
    means=[float(i[0]),float(i[2])]
    sds=[float(i[1]),float(i[3])]
    exact_test=one_way(means,sds,sizes)
    ##for min make sds larger, means closer together
    min_sds=[sd+.005 for sd in sds]
    if means[0]<means[1]:
        min_means=[means[0]+.005,means[1]-.005]
    elif means[1]<means[0]:
        min_means=[means[0]-.005,means[1]+.005]
    else:
        min_means=means
    min_test=one_way(min_means,min_sds,sizes)
    ##for max make sds smaller, means farther apart
    max_sds=[sd-.005 for sd in sds]
    if means[0]<means[1]:
        max_means=[means[0]-.005,means[1]+.005]
    elif means[1]<means[0]:
        max_means=[means[0]+.005,means[1]-.005]
    else:
        max_means=[means[0]-.005,means[1]+.005]
    max_test=one_way(max_means,max_sds,sizes)
    print 'Reported:'+'\t'+i[4]+'\t'+'Exact:'+'\t'+str(round(exact_test,2))+\
          '\t'+'Possible:'+'\t'+str(round(min_test,2))+'-'+str(round(max_test,2))



print
print 'The Flat-Rate Pricing Paradox: Conflicting Effects of "All-You-Can-Eat" Buffet Pricing'
print
print 'Table 1. How All-You-Can-Eat Buffets Influence Consumption and Satisfaction'
f1=open('pizza.txt')
data=[i.strip().split() for i in f1]
for i in data:
    sizes=[31,35]
    means=[float(i[0]),float(i[2])]
    sds=[float(i[1]),float(i[3])]
    exact_test=one_way(means,sds,sizes)
    ##for min make sds larger, means closer together
    min_sds=[sd+.005 for sd in sds]
    if means[0]<means[1]:
        min_means=[means[0]+.005,means[1]-.005]
    elif means[1]<means[0]:
        min_means=[means[0]-.005,means[1]+.005]
    else:
        min_means=means
    min_test=one_way(min_means,min_sds,sizes)
    ##for max make sds smaller, means farther apart
    max_sds=[sd-.005 for sd in sds]
    if means[0]<means[1]:
        max_means=[means[0]-.005,means[1]+.005]
    elif means[1]<means[0]:
        max_means=[means[0]+.005,means[1]-.005]
    else:
        max_means=[means[0]-.005,means[1]+.005]
    max_test=one_way(max_means,max_sds,sizes)
    print 'Reported:'+'\t'+i[4]+'\t'+'Exact:'+'\t'+str(round(exact_test,2))+\
          '\t'+'Possible:'+'\t'+str(round(min_test,2))+'-'+str(round(max_test,2))




print
print
print 'Bad Popcorn in Big Buckets: Portion Size Can Influence Intake as Much as Taste'
print 
print 'Table 1. Random Assignment of Moviegoers Showed No Age or Gender Differences '
f1=open('popcorn_table1.txt')
data=[i.strip().split() for i in f1]
##all possible changes:
combos={}
for combo in combinations_with_replacement([0,.05,-.05],4):
    for permut in permutations(combo):
        combos[permut]=''
for i in data:
    sizes=[38,39,40,40]
    means=np.array([float(i[0]),float(i[2]),float(i[4]),float(i[6])])
    sds=np.array([float(i[1]),float(i[3]),float(i[5]),float(i[7])])
    exact_test=one_way(means,sds,sizes)
    ##for min make sds larger
    min_sds=sds+.05
    ##for means make all possible changes
    mins=[]
    for combination in combos:
        mins.append(one_way(means+combination,min_sds,sizes))
    min_test=sorted(mins)[0]
    ##for max make sds smaller
    max_sds=sds-.05
    ##for means make all possible changes:
    maxs=[]
    for combination in combos:
        maxs.append(one_way(means+combination,max_sds,sizes))
    max_test=sorted(maxs)[-1]
    print 'Reported:'+'\t'+i[8]+'\t'+'Exact:'+'\t'+str(round(exact_test,3))+'\t'+\
    'Possible:'+'\t'+str(round(min_test,3))+'-'+str(round(max_test,3))



print
print 'Table 2. Larger Containers Influence Consumption Volume of Both Fresh and Stale Popcorn'
f1=open('popcorn_table2.txt')
data=[i.strip().split() for i in f1]
##all possible changes:
combos={}
for combo in combinations_with_replacement([0,.05,-.05],4):
    for permut in permutations(combo):
        combos[permut]=''
ro.globalenv['n']=ro.r.matrix(np.array([38,39,40,40]),nrow=2)
for i in data:
    u=np.array([float(i[0]),float(i[2]),float(i[4]),float(i[6])])
    s=np.array([float(i[1]),float(i[3]),float(i[5]),float(i[7])])
    ro.globalenv['u']=ro.r.matrix(u,nrow=2)
    ro.globalenv['s']=ro.r.matrix(s,nrow=2)
    exact_test=ro.r('ind.twoway.second(u,s,n,digits=10)').rx2('anova.table')[-1]
    
    ##for min test make sds larger
    ro.globalenv['s']=ro.r.matrix(s+.05,nrow=2)
    
    ##for means make all possible changes
    between_row=[]
    between_column=[]
    between_row_column=[]
    for combination in combos:
        ro.globalenv['u']=ro.r.matrix(u+combination,nrow=2)
        test=ro.r('ind.twoway.second(u,s,n,digits=10)')
        between_row.append(test.rx2('anova.table')[-1][1])
        between_column.append(test.rx2('anova.table')[-1][2])
        between_row_column.append(test.rx2('anova.table')[-1][3])
        
    min_row=sorted(between_row)[0]
    min_column=sorted(between_column)[0]
    min_row_column=sorted(between_row_column)[0]

    ##for max test make the sds smaller
    ro.globalenv['s']=ro.r.matrix(s-.05,nrow=2)
    ##for means make all possible changes
    between_row=[]
    between_column=[]
    between_row_column=[]
    for combination in combos:
        ro.globalenv['u']=ro.r.matrix(u+combination,nrow=2)
        test=ro.r('ind.twoway.second(u,s,n,digits=10)')
        between_row.append(test.rx2('anova.table')[-1][1])
        between_column.append(test.rx2('anova.table')[-1][2])
        between_row_column.append(test.rx2('anova.table')[-1][3])
    max_row=sorted(between_row)[-1]
    max_column=sorted(between_column)[-1]
    max_row_column=sorted(between_row_column)[-1]
    print 'Reported:'+'\t'+i[8]+'\t'+i[9]+'\t'+i[10]+'\t'\
          +'Exact:'+'\t'+str(round(exact_test[2],2))+'\t'+str(round(exact_test[1],2))+'\t'+str(round(exact_test[3],2))+'\t'\
          +'Possible:'+'\t'+str(round(min_column,2))+'-'+str(round(max_column,2))+'\t'+\
          str(round(min_row,2))+'-'+str(round(max_row,2))+'\t'+\
          str(round(min_row_column,2))+'-'+str(round(max_row_column,2))






