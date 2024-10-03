from collections import defaultdict as dd
import re, numpy
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

year='2024'
clss='LTI'

f = open(f"{year}-survey-edited.tsv")
out = open(f"{year}-{clss}-survey.html",'w')

lines=f.readlines()

atr=lines[0].strip().split('\t')
#print(atr)
timea=dd(list)
timeb=dd(list)
comments=dd(list)


students = 0
for l in lines[2:]:  # skip first line and my entry
    if l.startswith('#'):
        continue
    line=l.strip().split('\t')
    if not year in line[0]: #Only look at current year
        continue
    for (at,v) in zip(atr,line):
        #print (at,v)
        if at in ('Timestamp','Name (enough so I can identify your participation)') \
                or not v:
            continue
        m1 = r'(\d+)'
        m2 = r'(\d+)/(\d+)'
        m3 = r'(\d+)\s*\(([^)]+)\)'
        m4 = r'(\d+)/(\d+)\s*\(([^)]+)\)'
        #print (re.findall(m3,v.strip()))
        if re.findall(m4,v.strip()):
            for (a,b,c) in re.findall(m4,v.strip()):
                timea[at].append(int(a))
                timeb[at].append(int(b))
                comments[at].append(c)
        #        print  (a,b,c)
        elif re.findall(m3,v.strip()):
            for (a,c) in re.findall(m3,v.strip()):
                timea[at].append(int(a))
                comments[at].append(c)
#                print  (a,c)
        elif re.findall(m2,v.strip()):
            for (a,b) in re.findall(m2,v.strip()):
                timea[at].append(int(a))
                timeb[at].append(int(b))
#                print  (a,b)
        elif re.findall(m1,v.strip()):
            for (a) in re.findall(m1,v.strip()):
                timea[at].append(int(a))
        else:
             timea[at].append(0)
             #timea[b].append(0)
             print ("""can't parse %s <<%s>> %s""" % (v, at, line))
    print(timea)
    students += 1

# for a in atr:
#     if a in ('Timestamp','Name (enough so I can identify your participation)'):
#         continue
#     print (a)
#     print ([i for i in timea[a] if i >0])
#     print ([i for i in timeb[a] if i >0])
#     print (numpy.mean([i for i in timea[a] if i >0]))
#     print (numpy.std([i for i in timea[a] if i >0]))
#     print (", ".join(comments[a]))
#     print ()



media = sorted(atr[2:])
aidem = media[::-1]
###
###  Results for all people
###

print (atr[2:], media)



y_pos = np.arange(len(aidem))
amean = tuple([numpy.mean(timea[a]) for a in  aidem])
astd =  tuple([numpy.std(timea[a]) for a in  aidem])
plt.figure()
#plt.barh(y_pos, performance, xerr=error, align='center', alpha=0.4)
plt.barh(y_pos, amean,   color='r', xerr=astd, align='center', alpha=0.4)
#plt.barh(y_pos, bmean,   color='y', bottom=amean, xerr=bstd, align='center', alpha=0.4)

plt.yticks(y_pos, ["%s (%d)" % (a, len(timea[a])) for a in aidem ])
plt.yticks()
plt.xlabel('Time using Medium (minutes)')
plt.title("""Language use over various medium in one day (%d students)
Averaged over all students""" % students)
# ax2 = ax.twinx()
# ax2.set_yticks(ax1.get_yticks())
# ax2.set_yticklabels([len(timea[a]) for a in  aidem])
plt.tight_layout()
plt.savefig(f'{year}-all.png', bbox_inches='tight')

# plt.figure()
# data = [timea[a] for a in aidem]
# #fig1, ax1 = plt.subplots()
# plt.title('''Language use over various medium in one day ({} students) 
# Averaged over all students'''.format(students))
# plt.yticks(y_pos,aidem)
# plt.yticks()
# plt.boxplot(data, vert=False )
# plt.show()



bmean = tuple([numpy.mean(timeb[a]) for a in  aidem])
bstd =  tuple([numpy.std(timeb[a]) for a in  aidem])

plt.figure()
#plt.barh(y_pos, performance, xerr=error, align='center', alpha=0.4)
plt.barh(y_pos, bmean,   color='r', xerr=bstd, align='center', alpha=0.4)
#plt.barh(y_pos, bmean,   color='y', bottom=amean, xerr=bstd, align='center', alpha=0.4)

plt.yticks(y_pos, ["%s (%d)" % (a, len(timeb[a])) for a in aidem ])
plt.yticks()
plt.xlabel('Time using Medium (minutes)')
plt.title("""Language use over various medium in one day (%d students)
Averaged over all students""" % students)
# ax2 = ax.twinx()
# ax2.set_yticks(ax1.get_yticks())
# ax2.set_yticklabels([len(timea[a]) for a in  aidem])
plt.tight_layout()
plt.savefig(f'{year}-allb.png', bbox_inches='tight')



###
###  Results for only those who use things
###

y_pos = np.arange(len(aidem))
performance = [numpy.mean([i for i in timea[a] if i >0]) for a in  aidem]
error = [numpy.std([i for i in timea[a] if i >0]) for a in  aidem]

plt.figure()
plt.barh(y_pos, performance, xerr=error, align='center', alpha=0.4)
plt.yticks(y_pos, ["%s (%d)" % (a, len(timea[a])) for a in aidem ])
plt.yticks()
plt.xlabel('Time using Medium (minutes)')
plt.title("""Language use over various medium in one day (%d students)
Just for those students who used the Media""" % students)
# ax2 = ax.twinx()
# ax2.set_yticks(ax1.get_yticks())
# ax2.set_yticklabels([len(timea[a]) for a in  aidem])
plt.tight_layout()
plt.savefig(f'{year}-nonzero.png', bbox_inches='tight')


bmean = tuple([numpy.mean([i for i in timeb[a] if i >0]) for a in  aidem])
bstd =  tuple([numpy.std([i for i in timeb[a] if i >0]) for a in  aidem])

plt.figure()
#plt.barh(y_pos, performance, xerr=error, align='center', alpha=0.4)
plt.barh(y_pos, bmean,  xerr=bstd, align='center', alpha=0.4)
#plt.barh(y_pos, bmean,   color='y', bottom=amean, xerr=bstd, align='center', alpha=0.4)
plt.yticks(y_pos, ["%s (%d)" % (a, len(timeb[a])) for a in aidem ])
plt.yticks()
plt.xlabel('Time using Medium (minutes)')
plt.title("""Language use over various medium in one day (%d students)
Just for those students who used the Media""" % students)
# ax2 = ax.twinx()
# ax2.set_yticks(ax1.get_yticks())
# ax2.set_yticklabels([len(timea[a]) for a in  aidem])
plt.tight_layout()
plt.savefig(f'{year}-nonzerob.png', bbox_inches='tight')



print (f"""<html><head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>{clss}: Media Usage Survey {year}</title>
</head>
<body>
<h1>{clss}: Media Usage Survey {year}</h1>

One day in the life of {clss} students in {year}.

<h2>All Usage</h2>
<table>
<tr>
  <td><img src="{year}-all.png" alt="all"></td>
  <td><img src="{year}-nonzero.png" alt="non-zero"></td>
</tr>
</table>
<h2>Creating</h2>
<table>
<tr>
  <td><img src="{year}-allb.png" alt="all"></td>
  <td><img src="{year}-nonzerob.png" alt="non-zero"></td>
</tr>
</table>

<h2>Comments</h2>""", file=out)

for a in  comments:
    if comments[a]:
        print ("""<p><b>{}</b>: {}""".format(a, ", ".join(comments[a])),file=out)

print (f"<hr><p><a href='../index.html'>{clss}</a></body></html>",file=out)
