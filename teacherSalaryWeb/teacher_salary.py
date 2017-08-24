#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 15:02:54 2017

@author: shaozl
"""

#import unicodecsv as csv
import datetime
from db import DB
import numpy as np
import pandas as pd


def read_answer_data(date_from, date_to):    
#    with open('answers_6.csv') as f:
#        f_reader = csv.reader(f)
#        for row in f_reader:
#            answers.append(row)
    get_answer_sql = '''
    SELECT 
    a.teacher_id,
    a.teacher_rating,
    g.grade_id,
    a.FIXED_ANSWER_TIME,
    a.answer_type
    
FROM
    ozing_answer a,
    ozing_grade g
WHERE
    a.grade_id = g.grade_id
        AND a.PREAPPOINTMENT_ID IS NULL
        AND a.begin_time < a.end_time
        AND (a.answer_time >= 30
        OR a.fixed_answer_time >= 30)
        AND a.teacher_rating > 2
        AND a.date_added > "{}"
        AND a.date_added < "{}"
        AND a.TEACHER_ID IN (SELECT 
            teacher_id
        FROM
            ozing_teacher)
        and (a.answer_type = 'free' or a.answer_type = 'charge') 
        '''.format(date_from, date_to)
        
    result =  DB().select(get_answer_sql)
    if result:   
        return [list(item) for item in result ]
    

def group_answers(answers):
    keys = ['teacher_id', 'rating', 'grade', 'answer_time', 'answer_type']
    free_answers_d = {}
    charge_answers_d = {}
    one2one_answers_d = {}
    # separste answer(list) to different groups by its type
    # change list to dict
    for answer in answers:
        if answer[4] == 'free':
            free_answers_d = {key:value for key ,value in zip(keys,answer)}
            free_answers.append(free_answers_d)
        elif answer[4] == 'charge':
            charge_answers_d = {key:value for key ,value in zip(keys,answer)}
            charge_answers.append(charge_answers_d)
        else:
            one2one_answers_d = {key:value for key ,value in zip(keys,answer)}
            one2one_answers.append(one2one_answers_d)
            

        
def charged_salary(answer):
    # charged answer, only cares rank
    # 1-6 charged answer
    salary = 0
    if answer['grade'] <= 6:
        #rank3
        if answer['rating'] == 3:
            salary = answer['answer_time'] / 60 * rank_price_charge_junior[3]
        elif 4 <= answer['rating'] <= 9:
            salary = answer['answer_time'] / 60 * rank_price_charge_junior[4]
        elif 10 <= answer['rating'] <= 24:
            salary = answer['answer_time'] / 60 * rank_price_charge_junior[10]
        else:
            salary = answer['answer_time'] / 60 * rank_price_charge_junior[25]
               
    # 7-9 charged answer
    elif 7<= answer['grade'] <= 9:
        if answer['rating'] == 3:
            salary = answer['answer_time'] / 60 * rank_price_charge_middle[3]
        elif 4 <= answer['rating'] <= 9:
            salary = answer['answer_time'] / 60 * rank_price_charge_middle[4]
        elif 10 <= answer['rating'] <= 15:
            salary = answer['answer_time'] / 60 * rank_price_charge_middle[10]
        else:
            salary = answer['answer_time'] / 60 * rank_price_charge_middle[16]
    # 9-12 charged answer
    else:
        if 3 <= answer['rating'] <= 5:
            salary = answer['answer_time'] / 60 * rank_price_charge_high[3]
        elif 6 <= answer['rating'] <= 9:
            salary = answer['answer_time'] / 60 * rank_price_charge_high[6]
        elif 10 <= answer['rating'] <= 15:
            salary = answer['answer_time'] / 60 * rank_price_charge_high[10]
        elif 16 <= answer['rating'] <= 24:
            salary = answer['answer_time'] / 60 * rank_price_charge_high[16]
        else:
            salary = answer['answer_time'] / 60 * rank_price_charge_high[25]
    return salary
       

def free_answers_split(free_answers):
    answers_split = []
    for free_answer in free_answers:
        # when answer_time > 600, split it to several records, answer_time in each one should <= 600
        # remove the old item ,add splited ones
        if free_answer['answer_time'] > 600:
            answers_split.extend(split_to_10(free_answer))
            free_answers.remove(free_answer)
            
    free_answers.extend(answers_split)
    
    
def free_salary(answer):
    salary = 0
    # grade 1~6 
    if answer['grade'] <= 6:
        #rank3
        if answer['rating'] == 3: 
            # longer than 4min
            if int(answer['answer_time']) > 240:
                salary = 4 * rank_price_free_junior_1[3]
                salary += (int(answer['answer_time']) - 240) / 60 * rank_price_free_junior_2[3]
            else:
                salary = int(answer['answer_time']) / 60 * rank_price_free_junior_1[3]
                    
        elif 4 <= answer['rating'] <= 5:
            if int(answer['answer_time']) > 240: 
                salary = 4 * rank_price_free_junior_1[4]
                salary += (int(answer['answer_time']) - 240) / 60 * rank_price_free_junior_2[4]
            else:
                salary = int(answer['answer_time']) / 60 * rank_price_free_junior_1[4]
                
        elif 6 <= answer['rating'] <= 9:
            if int(answer['answer_time']) > 240: 
                salary = 4 * rank_price_free_junior_1[6]
                salary += (int(answer['answer_time']) - 240) / 60 * rank_price_free_junior_2[6]
            else:
                salary = int(answer['answer_time']) / 60 * rank_price_free_junior_1[6]
        elif 10 <= answer['rating'] <= 15:
            if int(answer['answer_time']) > 240: 
                salary = 4 * rank_price_free_junior_1[10]
                salary += (int(answer['answer_time']) - 240) / 60 * rank_price_free_junior_2[10]
            else:
                salary = int(answer['answer_time']) / 60 * rank_price_free_junior_1[10]
        elif 16 <= answer['rating'] <= 24:
            if int(answer['answer_time']) > 240: 
                salary = 4 * rank_price_free_junior_1[16]
                salary += (int(answer['answer_time']) - 240) / 60 * rank_price_free_junior_2[16]
            else:
                salary = int(answer['answer_time']) / 60 * rank_price_free_junior_1[16]
        else:
            if int(answer['answer_time']) > 240: 
                salary = 4 * rank_price_free_junior_1[25]
                salary += (int(answer['answer_time']) - 240) / 60 * rank_price_free_junior_2[25]
            else:
                salary = int(answer['answer_time']) / 60 * rank_price_free_junior_1[25]
                
    elif 7 <= answer['grade'] <= 9:
        #rank3
        if answer['rating'] == 3: 
            # longer than 6min
            if int(answer['answer_time']) > 360: 
                salary = 6 * rank_price_free_middle_1[3]
                salary += (int(answer['answer_time']) - 360) / 60 * rank_price_free_middle_2[3]
            else:
                salary = int(answer['answer_time']) / 60 * rank_price_free_middle_1[3]
                    
        elif 4 <= answer['rating'] <= 5:
            if int(answer['answer_time']) > 360: 
                salary = 6 * rank_price_free_middle_1[4]
                salary += (int(answer['answer_time']) - 360) / 60 * rank_price_free_middle_2[4]
            else:
                salary = int(answer['answer_time']) / 60 * rank_price_free_middle_1[4]
                
        elif 6 <= answer['rating'] <= 9:
            if int(answer['answer_time']) > 360: 
                salary = 6 * rank_price_free_middle_1[6]
                salary += (int(answer['answer_time']) - 360) / 60 * rank_price_free_middle_2[6]
            else:
                salary = int(answer['answer_time']) / 60 * rank_price_free_middle_1[6]
        elif 10 <= answer['rating'] <= 15:
            if int(answer['answer_time']) > 360: 
                salary = 6 * rank_price_free_middle_1[10]
                salary += (int(answer['answer_time']) - 360) / 60 * rank_price_free_middle_2[10]
            else:
                salary = int(answer['answer_time']) / 60 * rank_price_free_middle_1[10]
        elif 16 <= answer['rating'] <= 24:
            if int(answer['answer_time']) > 360: 
                salary = 6 * rank_price_free_middle_1[16]
                salary += int(answer['answer_time']) - 360 / 60 * rank_price_free_middle_2[16]
            else: 
                salary = int(answer['answer_time']) / 60 * rank_price_free_middle_1[16]
        else: 
            if int(answer['answer_time']) > 360: 
                salary = 6 * rank_price_free_middle_1[25]
                salary += (int(answer['answer_time']) - 360) / 60 * rank_price_free_middle_2[25]
            else:
                salary = int(answer['answer_time']) / 60 * rank_price_free_middle_1[25]
    else:
        if 3 <= answer['rating'] <= 5:
            salary = int(answer['answer_time']) / 60 * rank_price_free_high[3]
        elif 6 <= answer['rating'] <= 9:
            salary = int(answer['answer_time']) / 60 * rank_price_free_high[6]
        elif 10 <= answer['rating'] <= 15:
            salary = int(answer['answer_time']) / 60 * rank_price_free_high[10]
        elif 16 <= answer['rating'] <= 24:
            salary = int(answer['answer_time']) / 60 * rank_price_free_high[16]
        else:
            salary = int(answer['answer_time']) / 60 * rank_price_free_high[25]
            
    return salary
            
    
# when answer_time > 600, split it to several records, answer_time in each one should <= 600
def split_to_10(answer):
    out = []
    n = 0
    while n < int(answer['answer_time']) // 600:
        out.append(answer.copy())
        out[-1]['answer_time'] = '600'
        n += 1
        
    out.append(answer.copy())
    out[-1]['answer_time'] = str(int(answer['answer_time']) % 600)
    return out
    


#summary salary for each teacher
def summary_salary(answers):
    answer_salary = []
    from itertools import groupby
    from operator import itemgetter
    answers_sorted = sorted(answers, key=itemgetter('teacher_id'))
    for key, group in groupby(answers_sorted, itemgetter("teacher_id")):
        answer_salary.append((key,sum(map(itemgetter("salary"), group))))
    return answer_salary


def get_teacher_info(teachers):
    
    sql = '''select  ot.teacher_id, COALESCE(au.first_name, au.last_name) as name, 
                          au.username 
                          from  acornuser.acorn_user au
                          inner join acornuser.ozing_teacher ot 
                          on ot.user_id = au.id
                          where ot.teacher_id in ({})'''.format(teachers)
                          
    result =  DB().select(sql)
    if result:
        teacher_lst = [list(x) for x in result]
        
    return teacher_lst



def to_dataFrame(dict_list):  
    to_list = []
    head = dict_list[0].keys()
    for d in dict_list:
        ls = [ d[key] for key in head ]
        to_list.append(ls)
    
    to_array = np.array(to_list)
    to_frame = pd.DataFrame(to_array, columns=head)
    return to_frame
    


if __name__ == "__main__":
    
   # answers = []
    rank_price_charge_junior = {3:0.35, 4:0.40, 10:0.45, 25:0.50}
    rank_price_charge_middle = {3:0.45, 4:0.50, 10:0.55, 16:0.60}
    rank_price_charge_high = {3:0.60, 6:0.65, 10:0.70, 16:0.75, 25:0.80}
#    
    rank_price_free_junior_1 = {3:0.35, 4:0.40, 6:0.40, 10:0.45, 16:0.45, 25:0.50}
    rank_price_free_middle_1 = {3:0.45, 4:0.50, 6:0.50, 10:0.55, 16:0.55, 25:0.60}
    
    rank_price_free_junior_2 = {3:0.20, 4:0.20, 6:0.25, 10:0.25, 16:0.3, 25:0.30}
    rank_price_free_middle_2 = {3:0.20, 4:0.20, 6:0.25, 10:0.25, 16:0.3, 25:0.30}
    rank_price_free_high = {3:0.60, 6:0.65, 10:0.70, 16:0.75, 25:0.80}
    free_answers = []
    charge_answers = []
    one2one_answers = []
    #header = ['teacher_id', '教师姓名', '教师昵称', '教师等级', '薪资']
    
    ## ----START-----
    print("*******StartTime {} *******".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    # get data from csv file
    answers = read_answer_data('2017-07-16 00:00:00','2017-07-16 08:00:00')
    
    # seprate answers
    group_answers(answers)
    
    # split free_answers 
    free_answers_split(free_answers)
    
    # counting salary for each answer
    #charged answer
    for charge_answer in charge_answers:
        charge_answer.update({'salary':charged_salary(charge_answer)})
        
    # free answer
    for free_answer in free_answers:
        free_answer.update({'salary':free_salary(free_answer)})
        

    
    #combin free answers and charged answers to 1 
    all_answers = free_answers
    all_answers.extend(charge_answers)
    all_answers_df = to_dataFrame(all_answers)
    
    
    #counting answer_time, salary per answer_type
    all_answers_df['answer_time'] = all_answers_df['answer_time'].astype(int)
    all_answers_df['salary'] = all_answers_df['salary'].astype(float)
    salary_per_type = all_answers_df.groupby(['teacher_id', 'rating', 'answer_type']).sum()
    salary_per_type2 = salary_per_type.reset_index() 
    salary_per_type2['teacher_id'] = salary_per_type2['teacher_id'].astype(int) #'teacher_id','rating','answer_type','answer_time','salary'
    
    
    #salarysum per teacher
    salary_per_teacher = all_answers_df.groupby('teacher_id').sum().reset_index().loc[:, ['teacher_id', 'salary']] 
    salary_per_teacher = salary_per_teacher.rename(columns = {'salary':'salarySum'})
    salary_per_teacher['teacher_id'] = salary_per_teacher['teacher_id'].astype(int) #'teacher_id', 'salarySum'
    
    #get teacher info
    teacher_ids = ','.join('{}'.format(item[0]) for item in answers)
    teacher_infos = get_teacher_info(teacher_ids)
    teacher_infos_df = pd.DataFrame(teacher_infos, columns=['teacher_id','name','username'])
    teacher_infos_df['teacher_id'] = teacher_infos_df['teacher_id'].astype(int) #'teacher_id','name','username'
    
    
    df = pd.merge(teacher_infos_df, salary_per_teacher, on='teacher_id')
    df['cc'] = df.groupby('teacher_id').cumcount()
    
    salary_per_type2['cc'] = salary_per_type2.groupby('teacher_id').cumcount()
    
    teacher_info_salary = pd.merge(salary_per_type2, df, on=('teacher_id', 'cc'), how='outer')
    teacher_info_salary = teacher_info_salary.loc[:, ['teacher_id','name','username','rating','answer_type','answer_time','salary','salarySum']]
    
    
    teacher_info_salary.to_csv('result99.csv', encoding='utf-8-sig')

    
    
        
    print("*******EndTime {} *******".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))    
        
    