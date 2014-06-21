#!/usr/bin/env python
# -*- coding: utf8 -*-


import sys, os

GENDERS = {u'f' : u'девушки', u'm': u'юноши'}

def process_data():
    f = open('arkhan_math_2012.tsv', 'r')
    i = 0
    gendernum = {'f' : 0, 'm' : 0}
    gendersumm = {'f' : 0, 'm' : 0}
    schools = {}
    summ = 0
    totalnum = 0
    for l in f:
        i += 1
        if i == 1: continue
        parts = l.strip().decode('utf8').split(u'\t')
#        if parts[2] != '195': continue
        summ += float(parts[8])
        totalnum += 1
        # Gender
        gen = parts[10]
        if gen in gendersumm.keys():
            gendernum[gen] += 1
            gendersumm[gen] += float(parts[8])

        # Школы
        ou = parts[2]
        if ou not in schools.keys():
            schools[ou] = {'summ' : 0, 'num' : 0, 'avg' : 0, 'numfailed' : 0, 'f_num' : 0, 'f_sum' : 0, 'm_num': 0, 'm_sum' : 0, 'f_avg' : 0, 'm_avg' : 0}
        schools[ou]['summ'] += float(parts[8])
        schools[ou]['num'] += 1
        if gen in gendersumm.keys():
            schools[ou]['%s_num' %(gen)] += 1
            schools[ou]['%s_sum' %(gen)] += float(parts[8])
        if float(parts[8]) < 24:
            schools[ou]['numfailed'] += 1

    # Data enrichment
    for k in schools.keys():
        schools[k]['avg'] = schools[k]['summ'] / schools[k]['num']
        schools[k]['failedpercent'] = float(schools[k]['numfailed']) * 100 / schools[k]['num']
        schools[k]['f_avg'] = schools[k]['f_sum'] / schools[k]['f_num'] if schools[k]['f_num'] > 0 else 0
        schools[k]['m_avg'] = schools[k]['m_sum'] / schools[k]['m_num'] if schools[k]['m_num'] > 0 else 0

    items = sorted(schools.items(), lambda x, y: cmp(x[1]['avg'], y[1]['avg']), reverse=True)
    pos = 1
    for k, v in items:
        schools[k]['pos'] = pos
        pos += 1

    items = sorted(schools.items(), lambda x, y: cmp(x[1]['failedpercent'], y[1]['failedpercent']), reverse=False)
    pos = 1
    for k, v in items:
        schools[k]['possuccess'] = pos
        pos += 1


    totalsumm = summ / float(totalnum)
    print 'Всего сдававших:', totalnum
    print 'Общий средний балл:', totalsumm
    print '---'
    for k in gendernum.keys():
        print 'Средний балл - ', GENDERS[k], ':', gendersumm[k] / gendernum[k]
    print '---'
    items = sorted(schools.items(), lambda x, y: cmp(x[1]['pos'], y[1]['pos']), reverse=True)
    for k, v in items:
        print 'ОУ ID ', k, 'число сдававших:', v['num']
        print '- позиция (ср.балл):', v['pos'],'Средний балл:', v['summ'] / v['num']
        print '- позиция (успешность):', v['possuccess'],'Процент проваливших:', v['failedpercent']
        print '- девушки - число:', v['f_num'], 'средний балл:', v['f_avg']
        print '- юноши - число:', v['m_num'], 'средний балл:', v['m_avg']

    f = open('arch_math_2012_schools.csv', 'w')
    s = u'\t'.join([u'ОУ',u'число сдававших', u'позиция ср.балл', u'средний балл',
                    u'число праваливших', u'процент проваливших', u'рейтинг по успешности',
                    u'число юношей', u'средний балл юношей', u'число девушек', u'средний балл девушек'])
    f.write(s.encode('utf8') + '\n')
    for k, v in items:
        s = u'\t'.join([k, str(v['num']), str(v['pos']), str(round(v['avg'])),
                       str(v['numfailed']), str(round(v['failedpercent'])), str(v['possuccess']),
                        str(v['m_num']), str(round(v['m_avg'])), str(v['f_num']), str(round(v['f_avg']))])
        f.write(s.encode('utf8') + '\n')
    f.close()




if __name__ == "__main__":
    process_data()