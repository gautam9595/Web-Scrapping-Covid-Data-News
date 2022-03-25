#%%
#-----------------------------------Preliminary Work---------------------------
#------------------------------------------------------------------------------
from collections import OrderedDict
import requests
import calendar
import re
import operator
import copy
import ply.lex as lex
import ply.yacc as yaac
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import os
import os.path
from cmath import log, nan
from curses.ascii import isdigit
from datetime import date, datetime
import tkinter as tk
from tkinter import CENTER, NW, StringVar, ttk
from tkinter import *
from tkcalendar import Calendar
import datetime
import tkinter.scrolledtext as scrolledtext
from tkcalendar import DateEntry
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)

months = {}
for m in list(calendar.month_name[1:]):
    months[m] = {}

#Function to convert string to number
def convert_string_to_number(str):
    num = 0
    f = True
    if str is None or str is nan:
        return None
    for c in str:
        if c is None:
            return None
        if not c.isdigit():
            continue
        num = num*10 + int(c, 10)
        f = False
    if f:
        return None
    return num

#-----------------------------Tokens----------------------------
def t_TITLE(t):
    r'<title[^>]*>'
    return t
def t_OPENHEADER2(t):
    r'<h2[^>]*>'
    return t
def t_CLOSEHEADER2(t):
    r'</h2>'
    return t
def t_OPENHEADER3(t):
    r'<h3[^>]*>'
    return t
def t_CLOSEHEADER3(t):
    r'</h3>'
    return t
def t_OPENHEADER4(t):
    r'<h4[^>]*>'
    return t
def t_CLOSEHEADER4(t):
    r'</h4>'
    return t
def t_STARTP(t):
    r'<p[^>]*>'
    return t
def t_CLOSEP(t):
    r'</p>'
    return t
def t_OPENUL(t):
    r'<ul[^>]*>'
    return t
def t_CLOSEUL(t):
    r'</ul>'
    return t
def t_OPENLI(t):
    r'<li[^>]*>'
    return t
def t_CLOSELI(t):
    r'</li>'
    return t
def t_OPENDL(t):
    r'<dl[^>]*>'
    return t
def t_CLOSEDL(t):
    r'</dl>'
    return t
def t_GENERAL(t):
    r'<[^>]*>'
    return t
def t_AMPERSAND(t):
    r'&[^;]*;'
    return t
def t_NAME(t):
    r'[A-Za-z0-9.\-{:+};"(),%$]+'
    return t
def t_error(t):
    t.lexer.skip(1)

t_ignore = " \t"
tokens = [
    'TITLE',
    'OPENHEADER2',
    'CLOSEHEADER2',
    'OPENHEADER3',
    'CLOSEHEADER3',
    'OPENHEADER4',
    'CLOSEHEADER4',
    'STARTP',
    'CLOSEP',
    'OPENUL',
    'CLOSEUL',
    'OPENLI',
    'CLOSELI',
    'OPENDL',
    'CLOSEDL',
    'GENERAL',
    'NAME',
    'AMPERSAND',
]

#-------------------------Grammar Rule to Extract Covid News----------------------
#---------------------------------------------------------------------------------
temp_news = []
yr = 0
mont = ''

#---------------------------Grammar Rule to Extract 2019 Covid News---------------
def p_start2019(p):
    '''start2019 : getdate getnews
                 | getdate getnews start2019 '''
def p_getdate(p):
    '''getdate : OPENHEADER2 skipHTMLtags NAME NAME skipHTMLtags NAME skipHTMLtags CLOSEHEADER2
               | OPENHEADER2 skipHTMLtags NAME skipHTMLtags NAME skipHTMLtags CLOSEHEADER2'''

    global temp_news
    try:
        if len(p) == 9:
            #3rd Token is Date and 4th Token is Months
            news[2019][p[4]][p[3]] = []
            temp_news = news[2019][p[4]][p[3]]
        else:
            #Only month is given
            news[2019][p[3]] = []
            temp_news = news[2019][p[3]]
    except KeyError:
        return
    
def p_getnews(p):
    '''getnews : skipHTMLtags pname skipHTMLtags pname skipHTMLtags pname skipHTMLtags paragraph
               | paragraph'''
    #First production is just because there are some link after DD-Month
def p_paragraph(p):
    '''paragraph : skipHTMLtags pname skipHTMLtags NAME skipHTMLtags paragraph
                 | OPENHEADER3 skipHTMLtags pname skipHTMLtags pname skipHTMLtags CLOSEHEADER3 paragraph
                 | STARTP text CLOSEP
                 | STARTP text CLOSEP paragraph
                 | OPENUL text CLOSEUL
                 | OPENUL text CLOSEUL paragraph
                 | OPENDL text CLOSEDL
                 | OPENDL text CLOSEDL paragraph'''
    global temp_news
    if len(p) == 4 or len(p) == 5:
        temp_news.append(p[2])
def p_text(p):
    '''text : pname text
            | skipHTMLtags text
            | amper text
            | OPENLI text
            | CLOSELI text
            | OPENHEADER4 text
            | CLOSEHEADER4 text
            | empty '''
    if p[1] is None:
        p[0] = ''
    elif p[1][0] == '&' or p[1][0] == '<':
        #text : AMPERSAND text | skipHTMLtags text
        p[0] = p[2]
    else:
        p[0] = p[1] + ' ' + p[2]
def p_text2(p):
    '''text2 : pname text2
             | skipHTMLtags text2
             | amper text2
             | empty '''
    if p[1] is None:
        p[0] = ''
    elif p[1][0] == '&' or p[1][0] == '<':
        #text : AMPERSAND text | skipHTMLtags text
        p[0] = p[2]
    else:
        p[0] = p[1] + ' ' + p[2]
def p_amper(p):
    '''amper : AMPERSAND pname
             | AMPERSAND'''
    if len(p) == 3 and len(p[2]) > 3 and p[2].isnumeric():
        #It is 'Year' like 2020
        p[0] = p[2]
    else:
        p[0] = p[1]
def p_skipHTMLtags(p):
    '''skipHTMLtags : GENERAL
                    | GENERAL skipHTMLtags'''
    p[0] = p[1]
    if len(p) == 3:
        p[0] = p[0] + p[1]
def p_empty(p):
    'empty :'
    p[0] = None

def p_pname(p):
    '''pname : NAME
            | NAME pname'''
    if len(p) == 3:
        #First production is getting evaluated
        p[0] = p[1] + ' ' + p[2]
    else:
        #2nd Production is getting evaluated
        p[0] = p[1]

#-------------------------Grammar Rule to extract 2020 Jan covid news----------------------
#------------------------------------------------------------------------------------------
def p_startJAN2020(p):
    '''startJAN2020 : getdate2020 getnews2020
                    | getdate2020 getnews2020 startJAN2020'''
def p_getdate2020(p):
    '''getdate2020 : OPENHEADER3 skipHTMLtags pname skipHTMLtags CLOSEHEADER3'''

    #split dt into date and month. dt[0] is date and dt[1] is month
    try:
        dt = p[3].split(sep = ' ')
        if len(dt) == 1:
            return
        if len(dt) == 3 and dt[1].isnumeric():
            dt = [dt[1],dt[2]]
        global news
        global temp_news
        news[2020][dt[1]][dt[0]] = []
        temp_news = news[2020][dt[1]][dt[0]]
    except KeyError:
        return

def p_getnews2020(p):
    '''getnews2020 : text STARTP text CLOSEP text
                   | text STARTP text CLOSEP text getnews2020
                   | text OPENUL text CLOSEUL text
                   | text OPENUL text CLOSEUL text getnews2020'''
    global temp_news
    temp_news.append(p[3])   

#-----------------------------Grammar to extract news of Feb-Dec 2020, 2021 and 2022------------------------------------
#--------------------------------------------------------------------------------------------------------
def p_start202122(p):
    '''start202122 : title
                   | getdate202122 getnews202122 OPENHEADER2
                   | getdate202122 getnews202122 start202122'''
    # print('year: ' + str(yr) + ', len(p): ' + str(len(p)))
def p_title(p):
    '''title : TITLE NAME NAME NAME NAME NAME NAME NAME NAME'''
    global yr
    yr = int(p[9])
def p_getdate202122(p):
    '''getdate202122 : OPENHEADER3 skipHTMLtags pname text CLOSEHEADER3'''
    try:
        dt = p[3]
        global temp_news
        global news
        global yr
        dt = dt.split(sep = ' ')
        if len(dt) != 2:
            return
        news[yr][dt[1]][dt[0]] = list()
        temp_news = news[yr][dt[1]][dt[0]]
    except KeyError:
        return
def p_getnews202122(p):
    '''getnews202122 : text STARTP text CLOSEP
                     | text STARTP text CLOSEP getnews202122
                     | text OPENUL text CLOSEUL
                     | text OPENUL text CLOSEUL getnews202122
                     | text OPENUL text OPENUL text CLOSEUL text CLOSEUL'''
    global temp_news
    if len(p) == 9:
        temp_news.append(p[5])
        temp_news.append(p[7])
        if len(p[3]) > 7:
            #Assuming if the text is of greater than 7, then it is a news.
            temp_news.append(p[3])
    elif p[2][:3] == '<ul':
        temp_news.append(p[3])

#-----------------------------------------------------------------------
#----------------------Grammar Rules for Responses----------------------
def p_response(p):
    '''response : title
                | respdate respdata OPENHEADER2
                | respdate respdata response'''
    global yr
def p_respdate(p):
    '''respdate : OPENHEADER3 skipHTMLtags NAME NAME text CLOSEHEADER3'''
    try:
        global temp_news
        global resp
        global yr
        #3rd Token is date and 4th Token is Month
        if p[4] not in list(calendar.month_name[1:]) or not str(p[3]).isnumeric(): 
            return
        if p[3] not in resp[yr][p[4]].keys():
            resp[yr][p[4]][p[3]] = []
        temp_news = resp[yr][p[4]][p[3]]
    except KeyError:
        return
def p_respdata(p):
    '''respdata : text STARTP text CLOSEP
                | text STARTP text CLOSEP respdata
                | text OPENUL text CLOSEUL
                | text OPENUL text CLOSEUL respdata '''
    global temp_news
    temp_news.append(p[3])
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------

#--------------------To get Date Range for each country------------------
#------------------------------------------------------------------------
def p_range(p):
    '''range :  OPENHEADER3 skipHTMLtags pname text CLOSEHEADER3'''
    #-----------3rd Token is Date Token
    global temp_news
    global extracting_start_date
    dd = p[3].split(sep = ' ')
    if len(dd) == 1 and dd[0] in list(calendar.month_name[1:]):
        if extracting_start_date:
            temp_news[0].append(dd[0])
            temp_news[0].append('2020')
            raise IndexError
        else:
            temp_news[1] = [dd[0], '2021']
            return
    if len(dd) != 2 or dd[0] not in list(calendar.month_name[1:]) or not str(dd[1]).isnumeric():
        return
    #--------dd[0] is month and dd[1] is Year
    if extracting_start_date:
        temp_news[0].append(dd[0])
        temp_news[0].append(dd[1])
        raise IndexError
    else:
        temp_news[1] = [dd[0], dd[1]]
    

def p_range2(p):
    '''range2 :  OPENHEADER2 skipHTMLtags pname text CLOSEHEADER2'''
    #-----------3rd Token is Date Token
    global temp_news
    global extracting_start_date
    dd = p[3].split(sep = ' ')
    if len(dd) == 1 and dd[0] in list(calendar.month_name[1:]):
        if extracting_start_date:
            temp_news[0].append(dd[0])
            temp_news[0].append('2020')
            raise IndexError
        else:
            temp_news[1] = [dd[0], '2021']
            return
    if len(dd) != 2 or dd[0] not in list(calendar.month_name[1:]) or not str(dd[1]).isnumeric():
        return
    #--------dd[0] is month and dd[1] is Year
    if extracting_start_date:
        temp_news[0].append(dd[0])
        temp_news[0].append(dd[1])
        raise IndexError
    else:
        temp_news[1] = [dd[0], dd[1]]

#---------------------Grammar Rule to extract news for given countries-----------------------------------
#--------------------------------------------------------------------------------------------------------
def p_countrynews(p):
    '''countrynews : countryname
                   | getcountrydate getcountrynews OPENHEADER2
                   | getcountrydate getcountrynews countrynews '''
def p_countryname(p):
    '''countryname : TITLE pname GENERAL'''
    dd = p[2]
    dd = dd.split()
    global country_news
    global temp_news
    try:
        if dd[6] not in country_news.keys():
            country_news[dd[6]] = {}
        temp_news = country_news[dd[6]]
    except:
        temp_news = -1

#------Production to extract the date
def p_getcountrydate(p):
    '''getcountrydate : OPENHEADER3 skipHTMLtags pname text2 CLOSEHEADER3'''

    #------p[3] is month, p[4] is year
    global yr
    global mont
    global temp_news
    dd = p[3].split()
    try:
        if len(dd) == 2:
            yr = int(dd[1])
        else:
            yr = 2020
        mont = dd[0]
        if mont not in list(calendar.month_name[1:]):
            yr = -1
            return
        if yr not in temp_news.keys():
            temp_news[yr] = {}
    except:
        yr = -1
        return

def p_getcountrynews(p):
    '''getcountrynews : STARTP text2 CLOSEP
                      | STARTP text2 CLOSEP getcountrynews
                      | text2 OPENUL getdatafromli CLOSEUL
                      | text2 OPENUL getdatafromli CLOSEUL getcountrynews'''
    global temp_news
    global yr
    global mont
    try:
        if p[1][:2] == '<p':
            if yr not in temp_news.keys():
                temp_news[yr] = {}
            if mont not in temp_news[yr].keys():
                temp_news[yr][mont] = []
            temp_news[yr][mont].append(p[2])
    except:
        return


def p_getdatafromli(p):
    '''getdatafromli : OPENLI skipHTMLtags NAME NAME skipHTMLtags text2 CLOSELI
                     | OPENLI skipHTMLtags NAME NAME skipHTMLtags text2 CLOSELI getdatafromli
                     | OPENLI skipHTMLtags NAME NAME skipHTMLtags OPENUL getdatafromli2 CLOSEUL CLOSELI
                     | OPENLI skipHTMLtags NAME NAME skipHTMLtags OPENUL getdatafromli2 CLOSEUL CLOSELI getdatafromli'''
    global yr
    global mont
    global temp_news
    #------------p[3] is date, p[4] is month
    try:
        if len(p) == 8 or len(p) == 9:
            if yr not in temp_news.keys():
                temp_news[yr] = {}
            if mont not in temp_news[yr].keys():
                temp_news[yr][mont] = {}
            if p[3] not in temp_news[yr][mont].keys():
                temp_news[yr][mont][p[3]] = []
            temp_news[yr][mont][p[3]].append(p[6])
        else:
            if yr not in temp_news.keys():
                temp_news[yr] = {}
            if mont not in temp_news[yr].keys():
                temp_news[yr][mont] = {}
            if p[3] not in temp_news[yr][mont].keys():
                temp_news[yr][mont][p[3]] = []
            temp_news[yr][mont][p[3]].append(p[7])
    except:
        return
        

def p_getdatafromli2(p):
    '''getdatafromli2 : OPENLI text2 CLOSELI
                      | OPENLI text2 CLOSELI getdatafromli2'''
    p[0] = p[2]
    if len(p) == 5:
        p[0] += p[4]


def p_text3(p):
    '''text3 : pname text3
             | skipHTMLtags text3
             | amper text3
             | OPENHEADER3 text3
             | CLOSEHEADER3 text3
             | OPENLI text3
             | CLOSELI text3
             | OPENUL text3
             | CLOSEUL text3
             | OPENDL text3
             | CLOSEDL text3
             | empty '''
    if p[1] is None:
        p[0] = ''
    elif p[1][0] == '&' or p[1][0] == '<':
        #text : AMPERSAND text | skipHTMLtags text
        p[0] = p[2]
    else:
        p[0] = p[1] + ' ' + p[2]

def p_countrynews2(p):
    '''countrynews2 : countryname
                    | getcountrydate2 getcountrynews2
                    | getcountrydate2 getcountrynews2 countrynews2'''

def p_getcountrydate2(p):
    '''getcountrydate2 : OPENHEADER2 skipHTMLtags pname text3 CLOSEHEADER2'''

    global yr
    global mont
    dd = p[3].split()
    try:
        if len(dd) == 1:
            yr = 2022
            mont = dd[0]
        else:
            yr = int(dd[1])
            mont = dd[0]
        if mont not in list(calendar.month_name[1:]):
            yr = -1
    except:
        yr = -1
        return
    
    
def p_getcountrynews2(p):
    '''getcountrynews2 : text3 STARTP text3 CLOSEP
                       | text3 STARTP text3 CLOSEP getcountrynews2'''
    global yr, mont, temp_news

    #------p[3] is the news
    try:
        if yr not in temp_news.keys():
            temp_news[yr] = {}
        if mont not in temp_news[yr].keys():
            temp_news[yr][mont] = []
        temp_news[yr][mont].append(p[3])
    except:
        print(mont)
        return


def p_error(p):
    pass

#----------------------------Parsing to get news-----------------------------
#------------------------------------------------------------------------------

news = {2019:copy.deepcopy(months),2020:copy.deepcopy(months),2021:copy.deepcopy(months),2022:copy.deepcopy(months)}
#------------Extracting 2019 Covid News---------------------
#-------Opening file
file_path = 'News20-22/2019.html'
f = open(file_path,'r')
text = f.read()
lexer = lex.lex()
lexer.input(text)
parserr = yaac.yacc(start='start2019')
parserr.parse(text,lexer=lexer)
f.close()

#------------Extracting 2020 Jan Covid News-----------------------
file_path = 'News20-22/January2020.html'
f = open(file_path,'r')
text = f.read()
lexer = lex.lex()
lexer.input(text)
parserr = yaac.yacc(start='startJAN2020')
parserr.parse(text,lexer=lexer)
f.close()

#------------Extracting 2020 Feb-Dec, 2021, 2022 Covid News---------------------

#-------------URLS of 2020 Feb-Dec, 2021 and 2022 Pages-----------
countries = [
    'February2020',
    'March2020',
    'April2020',
    'May2020',
    'June2020',
    'July2020',
    'August2020',
    'September2020',
    'October2020',
    'November2020',
    'December2020',
    'January2021',
    'February2021',
    'March2021',
    'April2021',
    'May2021',
    'June2021',
    'July2021',
    'August2021',
    'September2021',
    'October2021',
    'November2021',
    'December2021',
    'January2022',
    'February2022',
    'March2022'
]

#---------------Extracting Covid News from the web-pages in folder 'News20-22'--------------------
for c in countries:
    #-------Opening file
    file_path = 'News20-22/' + c + '.html'
    f = open(file_path,'r')
    text = f.read()

    #------Tokenizing
    lexer = lex.lex()
    lexer.input(str(text))
    #------Parsing
    parserr = yaac.yacc(start = 'start202122')
    parserr.parse(text,lexer=lexer)
    #------Closing File
    f.close()

#---------------------------Extract Response News------------------------------
#------------------------------------------------------------------------------

resp = {2019:copy.deepcopy(months),2020:copy.deepcopy(months),2021:copy.deepcopy(months),2022:copy.deepcopy(months)}
countries = [
    'January2020',
    'February2020',
    'March2020',
    'April2020',
    'May2020',
    'June2020',
    'July2020',
    'August2020',
    'September2020',
    'October2020',
    'November2020',
    'December2020',
    'January2021',
    'February2021',
    'March2021',
    'April2021',
    'May2021',
    'June2021',
    'July2021',
    'August2021',
    'September2021',
    'October2021',
    'November2021',
    'December2021',
    'January2022',
    'February2022',
    'March2022'
]

#---------------Extracting Covid Response from the web-pages in folder 'Resp20-22'--------------------

for c in countries:
    #--------Opening File
    file_path = 'Resp20-22/' + c + '.html'
    f = open(file_path,'r')
    text = f.read()

    #------Tokenizing
    lexer = lex.lex()
    lexer.input(str(text))
    #------Parsing
    parserr = yaac.yacc(start = 'response')
    parserr.parse(text,lexer = lexer)
    #------Closing File
    f.close()

#---------------------------------------------------------------------------------

#-------------Getting Covid Words in a list-----------
covid_words = []
with open('covid_word_dictionary.txt','r') as fp:
    covid_words = [line.rstrip() for line in fp]
fp.close()
temp_ = []
for i in range(len(covid_words)):
    temp_.extend(covid_words[i].split())

covid_words = temp_

#---------------------Generating Word Cloud----------------------------
#----------------------------------------------------------------------
from collections import Counter
def generate_word_cloud(str1, str2, covid = False):
    tkns1 = str1.split()
    for i in range(len(tkns1)):
        tkns1[i] = tkns1[i].lower()
    
    tkns2 = str2.split()
    for i in range(len(tkns2)):
        tkns2[i] = tkns2[i].lower()
    #---------Common Words
    common_words = list((Counter(tkns1) & Counter(tkns2)).elements())
    if covid:
        #------Common Covid Words
        common_words = list((Counter(common_words) & Counter(covid_words)).elements())
        
    common_words = ' '.join(common_words)
    #---------STOPWORDS
    stopwords = set(STOPWORDS)

    #---------Plotting WordCloud with only common words
    wordcloud = WordCloud(width = 800, height = 800, background_color ='white', stopwords = stopwords, min_font_size = 10).generate(common_words)
    return wordcloud

stop_words = ['can', 'were', 'won', 'haven', "couldn't", 'about', "didn't", 'against', 'did', 'between', 'itself', "shouldn't", 'd', 'while', 'was', 'will', 'few', 'should', 'an', "wouldn't", 'their', 'where', 'himself', 'y', "hadn't", 'before', "mustn't", 'further', 'ain', "weren't", 'its', 'she', 'this', 'all', 'below', 'what', 'up', 'ma', 'shan', "she's", 'they', "mightn't", 'more', 'ourselves', 'it', 'not', 'doesn', 'there', 'other', 'herself', 'he', 'in', "it's", 'doing', "wasn't", 'again', 're', "aren't", 'very', 'needn', 'each', 'aren', 'at', 'if', 'myself', 'you', 'll', "hasn't", 'our', 'or', 'her', 'your', 'yours', 'as', 'him', 'for', 'than', "haven't", 'weren', 'through', 'be', 'into', 'too', 've', "you'd", 'my', 'yourselves', 'having', 'of', 'a', 'once', 'have', "don't", 'ours', 'those', 'shouldn', 'under', 'after', 'are', 'them', 'that', 'is', 'couldn', 'out', 'because', "you're", 'by', 'from', 'only', 'theirs', 'does', 'now', 'when', 'the', 'down', 't', 'on', 'and', 'been', 'whom', 'don', "you've", 'being', 'then', "isn't", 'some', 'didn', 'until', 'themselves', 'mightn', 'no', 'me', 'o', 'isn', 'his', 'same', 'am', "needn't", 'off', 'hers', 'with', 'above', 'but', 'over', 'how', 'most', "shan't", 'who', 'had', 'here', 'both', 'we', 'so', 'm', 'why', 'hadn', "you'll", 'do', 'i', 'any', 'has', 'yourself', 'such', 'during', 'nor', 'wouldn', "should've", 's', 'to', 'just', "doesn't", 'mustn', 'hasn', "that'll", 'own', "won't", 'which', 'these', 'wasn']
def percent_covid_words(str1, str2):

    #---------For 1st string
    tkns1 = str1.split()
    for i in range(len(tkns1)):
        tkns1[i] = tkns1[i].lower()
    temp = []
    for w in tkns1:
        if w not in stop_words:
            temp.append(w)
    tkns1 = temp
    
    #---------For 2nd string
    tkns2 = str2.split()
    for i in range(len(tkns2)):
        tkns2[i] = tkns2[i].lower()
    temp = []
    for w in tkns2:
        if w not in stop_words:
            temp.append(w)
    tkns2 = temp
    
    common_words = list((Counter(tkns1) & Counter(tkns2)).elements())
    count = 0
    for w in common_words:
        if w in covid_words:
            count += 1
    return count/len(common_words)

def top20common(str1,str2,covid= False):
    #---------For 1st string
    tkns1 = str1.split()
    for i in range(len(tkns1)):
        tkns1[i] = tkns1[i].lower()
    temp = []
    for w in tkns1:
        if w not in stop_words:
            temp.append(w)
    tkns1 = temp
    
    #---------For 2nd string
    tkns2 = str2.split()
    for i in range(len(tkns2)):
        tkns2[i] = tkns2[i].lower()
    temp = []
    for w in tkns2:
        if w not in stop_words:
            temp.append(w)
    tkns2 = temp
    
    common_words = list((Counter(tkns1) & Counter(tkns2)).elements())
    if covid:
        common_words = list((Counter(common_words) & Counter(covid_words)).elements())
    
    #-------Counting Frequency of common
    tmp_dict = {}
    for w in common_words:
        try:
            tmp_dict[w] += 1
        except KeyError:
            tmp_dict[w] = 0
    sorted_tuples = sorted(tmp_dict.items(),key = operator.itemgetter(1))
    sorted_dict = OrderedDict()
    for k,v in sorted_tuples:
        sorted_dict[k] = v
    
    txt = ''
    c = 0
    for w,f in sorted_dict.items():
        txt += w
        c += 1
        if c == 20:
            break
        txt += '\n'
    return txt

#---------------Extracting News availability Date Range for each country--------------------
#-------------------------------------------------------------------------------------------


Country_list = [
    'Argentina',
    'Australia',
    'Bangladesh',
    'Brazil',
    'Ghana',
    'India',
    'Indonesia',
    'Ireland',
    'Malaysia',
    'Mexico',
    'New Zealand',
    'Nigeria',
    'Pakistan',
    'Philippines',
    'Singapore',
    'South Africa',
    'Spain',
    'Turkey',
    'England'
]

#-----------Dict to store the range for each country
date_range = dict()
for country in Country_list:
    date_range[country] = [[],[]]

extracting_start_date = True
#----------------------------------------------------------------------------------------------------------

#------------------Exracting Start Date that can be extracted from rangestart-------------------
countries = {
    'Argentina',
    'Bangladesh',
    'Ghana',
    'Ireland',
    'Malaysia',
    'New Zealand',
    'Nigeria',
    'Philippines',
    'Singapore',
    'South Africa',
    'England'
}
for c in countries:
    temp_news = date_range[c]
    #-----Opening File
    file_path = 'StartDateRange1/' + c + '.html'
    f = open(file_path,'r')
    text = f.read()
    try:
        #-------Tokenizing
        lexer = lex.lex()
        lexer.input(str(text))
        #-------Parsing
        parserr = yaac.yacc(start = 'range')
        parserr.parse(text,lexer = lexer)
        f.close()
    except IndexError:
        f.close()
        
#----------------------------------------------------------------------------------------------------------

#-----------------Exracting Start Date that can be extracted from rangestart2-------------------
countries = [
    'Australia',
    'Brazil',
    'India',
    'Indonesia',
    'Mexico',
    'Pakistan',
    'Spain',
    'Turkey'
]
for c in countries:
    temp_news = date_range[c]
    #-----Opening File
    file_path = 'StartDateRange2/' + c + '.html'
    f = open(file_path,'r')
    text = f.read()
    try:
        lexer = lex.lex()
        lexer.input(str(text))
        parserr = yaac.yacc(start = 'range2')
        parserr.parse(text,lexer = lexer)
        f.close()
    except IndexError:
        f.close()
#----------------------------------------------------------------------------------------------------------

#---------------------Extracting End Date that can be extracted from range----------------------------
extracting_start_date = False
countries = [
    'Argentina',
    'Bangladesh',
    'Ghana',
    'Ireland',
    'Malaysia',
    'New Zealand',
    'Nigeria',
    'Philippines',
    'South Africa',
    'England',
    'Singapore'
]
for c in countries:
    temp_news = date_range[c]
    #-----Opening File
    file_path = 'EndDateRange1/' + c + '.html'
    f = open(file_path,'r')
    text = f.read()
    try:
        #-----Tokenizing
        lexer = lex.lex()
        lexer.input(str(text))
        #-----Parsing
        parserr = yaac.yacc(start = 'range')
        parserr.parse(text,lexer = lexer)
        f.close()
    except IndexError:
        f.close()

date_range['Bangladesh'][1] = ['June', '2020']

#----------------------------------------------------------------------------------------------------------

#------------------Exracting End Date that can be extracted from range2-------------------
countries = {
    'Australia',
    'Brazil',
    'India',
    'Indonesia',
    'Mexico',
    'Pakistan',
    'Spain',
    'Turkey'
}
for c in countries:
    temp_news = date_range[c]
    #-----Opening File
    file_path = 'EndDateRange2/' + c + '.html'
    f = open(file_path,'r')
    text = f.read()
    try:
        lexer = lex.lex()
        lexer.input(str(text))
        parserr = yaac.yacc(start = 'range2')
        parserr.parse(text,lexer = lexer)
        f.close()
    except IndexError:
        f.close()
#----------------------------------------------------------------------------------------------------------

#date_range[country] = [['Start month', 'Start year'],['End month', 'End year']]

#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------

#----------------------------------Extracting Covid News for given countries-----------------------------
#--------------------------------------------------------------------------------------------------------

#-----------------Data structure to store news of given country
country_news = {}
for country in Country_list:
    country_news[country] = {}

#----------Extracting Argentina News
file_path = 'country_Page/Argentina.html'
f = open(file_path,'r')
text = f.read()
lexer = lex.lex()
lexer.input(str(text))
parserr = yaac.yacc(start = 'countrynews')
parserr.parse(text,lexer = lexer)
f.close()
#---------Extracting Australia News
for i in range(1,5):
    file_path = 'country_Page/Australia' + str(i) + '.html'
    f = open(file_path,'r') 
    text = f.read()
    lexer = lex.lex()
    lexer.input(str(text))
    parserr = yaac.yacc(start = 'countrynews2')
    parserr.parse(text,lexer = lexer)
    f.close()
#----------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------

#---------------------------------For Assignment1 Tasks--------------------------------------
#--------------------------------------------------------------------------------------------
import Task2 as ts

#-----------------------------------------GUI-----------------------------------------------
#--------------------------------------------------------------------------------------------

LARGEFONT =("Times New Roman", 20)
class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
		
		# continer creation
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
        
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        #Frames 
        self.frames = {}

        for F in (MainPage, ContinentPage, CountryPage, Time_Range_Page, News_response, Date_range_Page, wordC, country_news_page, Jaccard_similarity_page):
            
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row = 0, column = 0, sticky ="nsew")

        self.show_frame(MainPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

#MainPage
class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
		
        label = ttk.Label(self, text ="MainPage", font = LARGEFONT)
		
        label.grid(row = 0, column = 1, padx = 10, pady = 10)
        label.place(relx = 0.4, rely = 0.02,anchor=NW)
        
        button1 = ttk.Button(self, text ="Country Covid status",
        command = lambda : controller.show_frame(CountryPage))
	

        button1.grid(row = 1, column = 1,padx = 10, pady = 10)
        button1.place(relx = 0.15, rely = 0.2,anchor=NW)

        button2 = ttk.Button(self, text ="Continent/World Covid status",
		command = lambda : controller.show_frame(ContinentPage))
	
        button2.grid(row = 1, column = 90,columnspan=10, padx = 20, pady = 10)
        button2.place(relx = 0.37, rely = 0.2,anchor=NW)

        button3 = ttk.Button(self, text ="Time Range Query",
		command = lambda : controller.show_frame(Time_Range_Page))
	
        button3.grid(row = 1, column = 90,columnspan=10, padx = 20, pady = 10)
        button3.place(relx = 0.62, rely = 0.2,anchor=NW)

        newsRespBTN = ttk.Button(self, text = 'News/Response Page', 
        command = lambda : controller.show_frame(News_response))
        newsRespBTN.grid(row = 1, column = 90,columnspan=10, padx = 20, pady = 10)
        newsRespBTN.place(relx = 0.15, rely = 0.35,anchor=NW)

        DateRangeBTN = ttk.Button(self,text='Date Range Page',
        command = lambda : controller.show_frame(Date_range_Page))
        DateRangeBTN.grid(row = 1, column = 90,columnspan=10, padx = 20, pady = 10)
        DateRangeBTN.place(relx = 0.4, rely = 0.35,anchor=NW)

        DateRangeBTN = ttk.Button(self,text='Word Cloud Page',
        command = lambda : controller.show_frame(wordC))
        DateRangeBTN.grid(row = 1, column = 90,columnspan=10, padx = 20, pady = 10)
        DateRangeBTN.place(relx = 0.625, rely = 0.35,anchor=NW)

        CountryNewsBTN = ttk.Button(self,text='Country News Page',
        command = lambda : controller.show_frame(country_news_page))
        CountryNewsBTN.grid(row = 1, column = 90,columnspan=10, padx = 20, pady = 10)
        CountryNewsBTN.place(relx = 0.27, rely = 0.5,anchor=NW)

        JC_simBTN = ttk.Button(self,text='Jaccard Similarity Page',
        command = lambda : controller.show_frame(Jaccard_similarity_page))
        JC_simBTN.grid(row = 1, column = 90,columnspan=10, padx = 20, pady = 10)
        JC_simBTN.place(relx = 0.52, rely = 0.5,anchor=NW)
	
# ContinentPage
class ContinentPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.data_label = ttk.Label(self, text ="",font=("Times New Roman", 15))
        self.data_label.grid(row = 0, column = 1, padx = 10, pady = 10)
        self.data_label.place(relx = 0.1, rely = 0.45,anchor=NW)


        label = ttk.Label(self, text ="Continent/World Page", font = LARGEFONT)
        label.grid(row = 0, column = 1, padx = 10, pady = 10)
        label.place(relx = 0.35, rely = 0.02,anchor=NW)

        #select continent
        conlabel = ttk.Label(self, text ="Select Continent:")
        conlabel.grid(row = 0, column = 1, padx = 10, pady = 10)
        conlabel.place(relx = 0.15, rely = 0.22,anchor=NW)

        #Drop down menu of continent list
        continent_list = ['World', 'Asia', 'Europe', 'North America', 'South America', 'Africa', 'Oceania']
        self.clicked = StringVar()
        self.clicked.set('Asia')
        drop = OptionMenu(self, self.clicked , *continent_list)
        drop.grid(row = 0, column = 1, padx = 10, pady = 10)
        drop.place(relx = 0.27, rely = 0.205,anchor=NW)

        #select field
        field = ['Total Cases', 'New Cases', 'Total Deaths', 'New Deaths', 'Total Recovered', 'New Recovered', 'Active Cases', 'Death Cases/Mil pop', 'Total Tests', 'Tests/Mil pop']
        conlabel2 = ttk.Label(self, text ="Select Field:")
        conlabel2.grid(row = 0, column = 1, padx = 10, pady = 10)
        conlabel2.place(relx = 0.45, rely = 0.22,anchor=NW)

        #Drop down menu of field list
        self.clicked2 = StringVar()
        self.clicked2.set('Total Cases')
        drop2 = OptionMenu(self, self.clicked2 , *field)
        drop2.grid(row = 0, column = 1, padx = 10, pady = 10)
        drop2.place(relx = 0.55, rely = 0.205,anchor=NW)

        button1 = ttk.Button(self, text ="View Details", command = lambda : self.show_covid_data())
        
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)
        button1.place(relx = 0.4, rely = 0.32,anchor=NW)

        button2 = ttk.Button(self, text ="Go Back to Main Page", command = lambda : controller.show_frame(MainPage))
	
        button2.grid(row = 2, column = 1, padx = 10, pady = 10)
        button2.place(relx = 0.65, rely = 0.03,anchor=NW)

    def show_covid_data(self):
        c = self.clicked.get()
        f = self.clicked2.get()
        data_ = ts.Covid_data[c][f]
        string_data = f
        append_ = c + '\t' + f + ': '
        if data_ is None:
            string_data += ': Not Available'
            append_ += 'NA'
        else:
            string_data += ': ' + str(data_)
            append_ += str(data_)
            if c == 'World':
                self.data_label.config(text=string_data)
                return

            world_data = ts.Covid_data['World'][f]
            if world_data is not None:
                #finding % of world
                world_percent = (data_/world_data)*100
                world_percent = round(world_percent,3)
                string_data += '\t\tTotal World\'s % = ' + str(world_percent) + '%'
                append_ += '\tWorld\'s % = ' + str(world_percent)
            else:
                string_data += '\t\tTotal World\'s % = Not Available'
                append_ += '\tWorld\'s % = NA'

        self.data_label.config(text=string_data)

#CountryPage
class CountryPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.data_label = ttk.Label(self, text ="",font=("Times New Roman", 15))
        self.data_label.grid(row = 0, column = 1, padx = 10, pady = 10)
        self.data_label.place(relx = 0.1, rely = 0.45,anchor=NW)

        label = ttk.Label(self, text ="Country Page", font = LARGEFONT)
        label.grid(row = 0, column = 4, padx = 10, pady = 10)
        label.place(relx = 0.4, rely = 0.02,anchor=NW)

        #select Country
        colabel = ttk.Label(self, text ="Select Country:")
        colabel.grid(row = 0, column = 1, padx = 10, pady = 10)
        colabel.place(relx = 0.08, rely = 0.22,anchor=NW)

        #Drop down menu of continent list
        country_list = [
            'France',
            'UK',
            'Russia',
            'Italy',
            'Germany',
            'Spain',
            'Poland',
            'Netherlands',
            'Ukraine',
            'Belgium',
            'USA',
            'Mexico',
            'Canada',
            'Cuba',
            'Costa Rica',
            'Panama',
            'India',
            'Turkey',
            'Iran',
            'Indonesia',
            'Philippines',
            'Japan',
            'Israel',
            'Malaysia',
            'Thailand',
            'Vietnam',
            'Iraq',
            'Bangladesh',
            'Pakistan',
            'Brazil',
            'Argentina',
            'Colombia',
            'Peru',
            'Chile',
            'Bolivia',
            'Uruguay',
            'Paraguay',
            'Venezuela',
            'South Africa',
            'Morocco',
            'Tunisia',
            'Ethiopia',
            'Libya',
            'Egypt',
            'Kenya',
            'Zambia',
            'Algeria',
            'Botswana',
            'Nigeria',
            'Zimbabwe',
            'Australia',
            'Fiji',
            'Papua New Guinea',
            'New Caledonia',
            'New Zealand'
        ]
        
        self.clicked = StringVar()
        self.clicked.set('India')
        drop = ttk.Combobox(self, textvariable= self.clicked, values=country_list,state='readonly')
        drop.grid(row = 0, column = 1, padx = 10, pady = 10)
        drop.place(relx = 0.2, rely = 0.22,anchor=NW)

        #Drop down menu for field
        field = ['Total Cases', 'New Cases', 'Total Deaths', 'New Deaths', 'Total Recovered', 'New Recovered', 'Active Cases', 'Death Cases/Mil pop', 'Total Tests', 'Tests/Mil pop']

        colabel2 = ttk.Label(self, text ="Select Field:")
        colabel2.grid(row = 0, column = 1, padx = 10, pady = 10)
        colabel2.place(relx = 0.5, rely = 0.22,anchor=NW)

        self.clicked2 = StringVar()
        self.clicked2.set('Total Cases')
        drop2 = ttk.Combobox(self, textvariable= self.clicked2, values=field,state='readonly')
        drop2.grid(row = 0, column = 1, padx = 10, pady = 10)
        drop2.place(relx = 0.6, rely = 0.22,anchor=NW)

        button1 = ttk.Button(self, text ="View Details", command = lambda : self.show_covid_data())
	

        button1.grid(row = 1, column = 1, padx = 10, pady = 10)
        button1.place(relx = 0.45, rely = 0.305,anchor=NW)
	

        button2 = ttk.Button(self, text ="Go Back to Main Page", command = lambda : controller.show_frame(MainPage))
	

        button2.grid(row = 2, column = 1, padx = 10, pady = 10)
        button2.place(relx = 0.65, rely = 0.03,anchor=NW)
    
    def show_covid_data(self):
        c = self.clicked.get()
        f = self.clicked2.get()
        data_ = ts.Covid_data[c][f]
        string_data = f
        append_ = c + '\t' + f + ': '
        if data_ is None:
            string_data += ': Not Available'
            append_ += 'Not Available'
        else:
            string_data += ': ' + str(data_)
            append_ += str(data_)

            world_data = ts.Covid_data['World'][f]
            if world_data is not None:
                #finding % of world
                world_percent = (data_/world_data)*100
                world_percent = round(world_percent,3)
                string_data += '\t\tTotal World\'s % = ' + str(world_percent) + '%'
                append_ += '\tWorld\'s % = ' + str(world_percent)
            else:
                string_data += '\t\tTotal World\'s % = Not Available'
                append_ += '\tWorld\'s % = Not Available'

        self.data_label.config(text=string_data)
    
class Time_Range_Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.datalabel = ttk.Label(self,text="", font = ("Times New Roman", 15))
        self.datalabel.grid(row = 0, column = 1, padx = 10, pady = 10)
        self.datalabel.place(relx = 0.1, rely = 0.65,anchor=NW)

        label = ttk.Label(self, text ="Time Range Query Page", font = LARGEFONT)
        label.grid(row = 0, column = 4, padx = 10, pady = 10)
        label.place(relx = 0.4, rely = 0.02,anchor=NW)

        #select Country
        colabel = ttk.Label(self, text ="Select Country:")
        colabel.grid(row = 0, column = 1, padx = 10, pady = 10)
        colabel.place(relx = 0.1, rely = 0.15,anchor=NW)
        self.country_list = [
            'France',
            'UK',
            'Russia',
            'Italy',
            'Germany',
            'Spain',
            'Poland',
            'Netherlands',
            'Ukraine',
            'Belgium',
            'USA',
            'Mexico',
            'Canada',
            'Cuba',
            'Costa Rica',
            'Panama',
            'India',
            'Turkey',
            'Iran',
            'Indonesia',
            'Philippines',
            'Japan',
            'Israel',
            'Malaysia',
            'Thailand',
            'Vietnam',
            'Iraq',
            'Bangladesh',
            'Pakistan',
            'Brazil',
            'Argentina',
            'Colombia',
            'Peru',
            'Chile',
            'Bolivia',
            'Uruguay',
            'Paraguay',
            'Venezuela',
            'South Africa',
            'Morocco',
            'Tunisia',
            'Ethiopia',
            'Libya',
            'Egypt',
            'Kenya',
            'Zambia',
            'Algeria',
            'Botswana',
            'Nigeria',
            'Zimbabwe',
            'Australia',
            'Fiji',
            'Papua New Guinea',
            'New Caledonia',
            'New Zealand'
        ]

        self.clicked = StringVar()
        self.clicked.set('India')
        drop = ttk.Combobox(self, textvariable = self.clicked, values=self.country_list, state='readonly')
        drop.grid(row = 0, column = 1, padx = 10, pady = 10)
        drop.place(relx = 0.22, rely = 0.15,anchor=NW)

        #select the field
        colabel2 = ttk.Label(self, text ="Select Field:")
        colabel2.grid(row = 0, column = 1, padx = 10, pady = 10)
        colabel2.place(relx = 0.5, rely = 0.15,anchor=NW)
        self.fields = ['Change in Active Cases', 'Change in Daily Deaths', 'Change in New Recoveries', 'Change in New Cases']
        self.clicked2 = StringVar()
        self.clicked2.set('Change in Active Cases')
        drop2 = ttk.Combobox(self,textvariable=self.clicked2,values= self.fields, state='readonly')
        drop2.grid(row = 0, column = 1, padx = 10, pady = 10)
        drop2.place(relx = 0.6, rely = 0.15,anchor=NW)


        #select the start date
        datelabel = ttk.Label(self, text ="Select start Date:")
        datelabel.grid(row = 0, column = 1, padx = 10, pady = 10)
        datelabel.place(relx = 0.08, rely = 0.23,anchor=NW)
        self.cal = Calendar(self, selectmode = 'day',year = 2022, month = 1, day = 21, date_pattern = 'dd-mm-yyy')
        self.cal.grid(row = 0, column = 1, padx = 10, pady = 10)
        self.cal.place(relx = 0.15, rely = 0.28,anchor=NW)

        #select the end date
        datelabel2 = ttk.Label(self, text ="Select End Date:")
        datelabel2.grid(row = 0, column = 1, padx = 10, pady = 10)
        datelabel2.place(relx = 0.5, rely = 0.23,anchor=NW)
        self.cal2 = Calendar(self, selectmode = 'day',year = 2022, month = 1, day = 21, date_pattern = 'dd-mm-yyy')
        self.cal2.grid(row = 0, column = 1, padx = 10, pady = 10)
        self.cal2.place(relx = 0.55, rely = 0.28,anchor=NW)

        button1 = ttk.Button(self, text ="Go Back to Main Page", command = lambda : controller.show_frame(MainPage))

        button1.grid(row = 2, column = 1, padx = 10, pady = 10)
        button1.place(relx = 0.7, rely = 0.03,anchor=NW)


        button2 = ttk.Button(self, text ="View Change",command = lambda : self.show_date())
	

        button2.grid(row = 1, column = 1, padx = 10, pady = 10)
        button2.place(relx = 0.82, rely = 0.32,anchor=NW)


        button3 = ttk.Button(self, text ="Most Similar Country",command = lambda : self.most_similar())
	

        button3.grid(row = 1, column = 1, padx = 10, pady = 10)
        button3.place(relx = 0.82, rely = 0.45,anchor=NW)
    
    def most_similar(self):
        start_date = self.cal.get_date()
        end_date = self.cal2.get_date()
        month_dict = {'01' : 'Jan', '02' : 'Feb', '03' : 'Mar', '04' : 'Apr', '05' : 'May', '06' : 'Jun', '07' : 'Jul', '08' : 'Aug', '09' : 'Sep', '10' : 'Oct', '11' : 'Nov', '12' : 'Dec'}
        
        #converting start date to the relevant form for dictionary query
        start_datestr = start_date.split(sep = '-')
        sd = datetime.datetime(int(start_datestr[2]),int(start_datestr[1]),int(start_datestr[0]))
        start_datestr = month_dict[start_datestr[1]] + ' ' + start_datestr[0] + ' ' +  start_datestr[2]
        
        
        #converting end date to the relevant form for dictionary query
        end_datestr = end_date.split(sep = '-')
        ed = datetime.datetime(int(end_datestr[2]),int(end_datestr[1]),int(end_datestr[0]))
        end_datestr = month_dict[end_datestr[1]] + ' ' + end_datestr[0] + ' ' +  end_datestr[2]
        

        #get start date data from the dictionary
        append_ = self.clicked.get() + ' ' + start_datestr + '-' + end_datestr + ' '

        
        #check if sd > ed
        if sd > ed:
            change_percent_str = 'Start date is greater than end date'
            self.datalabel.config(text = change_percent_str)
            return

        msc = None
        min_change = 99999999
        fi = self.clicked2.get().split(sep=' ')
        fi = ' '.join(fi[2:])

        try:
            start_data = ts.date_wise_data[self.clicked.get()][fi][start_datestr]
            end_data = ts.date_wise_data[self.clicked.get()][fi][end_datestr]
                
            if start_data is None or end_data is None:
                pri = 'Data not Available'
                append_ += 'Data Not Available'
                self.datalabel.config(text = pri)
                return
        except KeyError:
            pri = 'Data not Available'
            append_ += 'Data Not Available'
            self.datalabel.config(text = pri)
            return
        except TypeError:
            pri = 'Data not Available'
            append_ += 'Data Not Available'
            self.datalabel.config(text = pri)
            return
        change_percent = self.change_(start_data,end_data)

        for coun in self.country_list:
            if coun == self.clicked.get():
                continue;
            try:
                country_start_date_data = ts.date_wise_data[coun][fi][start_datestr]
                country_end_date_data = ts.date_wise_data[coun][fi][end_datestr]
            except KeyError:
                continue
            except TypeError:
                continue
            if country_start_date_data is not None and country_end_date_data is not None:
                temp = abs(self.change_(country_start_date_data,country_end_date_data) - change_percent)
                if temp < min_change:
                    min_change = temp
                    msc = coun
        pri = ""
        if msc is not None:
            # pri = msc + ' is closests to ' + self.clicked.get() + ' in terms of ' + fi
            pri = 'In terms of ' + fi +', '+ msc + ' is closests to ' + self.clicked.get()
            append_ += pri
        else:
            pri = 'Data not Available'
            append_ += 'Data Not Available'
        self.datalabel.config(text = pri)

    
    def change_(self,start_data, end_data):
        return (end_data - start_data + 0.001)/(start_data + 0.001)
    
    def show_date(self):
        start_date = self.cal.get_date()
        end_date = self.cal2.get_date()
        month_dict = {'01' : 'Jan', '02' : 'Feb', '03' : 'Mar', '04' : 'Apr', '05' : 'May', '06' : 'Jun', '07' : 'Jul', '08' : 'Aug', '09' : 'Sep', '10' : 'Oct', '11' : 'Nov', '12' : 'Dec'}
        
        #converting start date to the relevant form for dictionary query
        start_datestr = start_date.split(sep = '-')
        sd = datetime.datetime(int(start_datestr[2]),int(start_datestr[1]),int(start_datestr[0]))
        start_datestr = month_dict[start_datestr[1]] + ' ' + start_datestr[0] + ' ' +  start_datestr[2]
        
        
        #converting end date to the relevant form for dictionary query
        end_datestr = end_date.split(sep = '-')
        ed = datetime.datetime(int(end_datestr[2]),int(end_datestr[1]),int(end_datestr[0]))
        end_datestr = month_dict[end_datestr[1]] + ' ' + end_datestr[0] + ' ' +  end_datestr[2]
        

        #get start date data from the dictionary
        field_ = self.clicked2.get().split(sep=' ')
        field_ = ' '.join(field_[2:])
        change_percent = 0
        append_ = self.clicked.get() + '\t' + start_datestr + '-' + end_datestr + '\t' + field_
        #get start date data
        try:
            start_data = ts.date_wise_data[self.clicked.get()][field_][start_datestr]
            if start_data is None:
                raise KeyError
        except KeyError:
            change_percent_str = 'Data Not available for ' + start_datestr
            self.datalabel.config(text = change_percent_str)
            append_ += '\t' + change_percent_str
            return
        except TypeError:
            change_percent_str = 'Data Not available for ' + start_datestr
            self.datalabel.config(text = change_percent_str)
            append_ += '\t' + change_percent_str
            return
        
        #get end date data
        try:
            end_data = ts.date_wise_data[self.clicked.get()][field_][end_datestr]
            if end_data is None:
                raise KeyError
        except KeyError:
            change_percent_str = 'Data Not available for ' + end_datestr
            self.datalabel.config(text = change_percent_str)
            append_ += '\t' + change_percent_str
            return
        except TypeError:
            change_percent_str = 'Data Not available for ' + start_datestr
            self.datalabel.config(text = change_percent_str)
            append_ += '\t' + change_percent_str
            return
        
        #check if sd > ed
        if sd > ed:
            change_percent_str = 'Start date is greater than end date'
            self.datalabel.config(text = change_percent_str)
            append_ += '\t' + change_percent_str
            return

        change_percent = self.change_(start_data,end_data)
        change_percent = round(change_percent,3)
        
        
        if change_percent >= 0:
            change_percent_str = str(change_percent)
            change_percent_str = change_percent_str + '% Increase'
             
        else:
            change_percent = -change_percent
            change_percent_str = str(change_percent)
            change_percent_str = change_percent_str + '% Decrease'

        self.datalabel.config(text = change_percent_str)
        append_ += '\t' + change_percent_str

#News/Response Page
class News_response(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.canvas = 0
        self.datalabel = ttk.Label(self,text="", font = ("Times New Roman", 15))
        self.datalabel.grid(row = 0, column = 1, padx = 10, pady = 10)
        self.datalabel.place(relx = 0.1, rely = 0.5,anchor=NW)

        label = ttk.Label(self, text ="Worldwide News-Response Page", font = LARGEFONT)
        label.grid(row = 0, column = 4, padx = 10, pady = 10)
        label.place(relx = 0.35, rely = 0.02,anchor=NW)

        #select the start date
        datelabel = ttk.Label(self, text ="Select start Date:")
        datelabel.grid(row = 0, column = 1, padx = 10, pady = 10)
        datelabel.place(relx = 0.08, rely = 0.17,anchor=NW)
        self.cal = Calendar(self, selectmode = 'day',year = 2022, month = 1, day = 21, date_pattern = 'dd-mm-yyy')
        self.cal.grid(row = 0, column = 1, padx = 10, pady = 10)
        self.cal.place(relx = 0.15, rely = 0.22,anchor=NW)

        #select the end date
        datelabel2 = ttk.Label(self, text ="Select End Date:")
        datelabel2.grid(row = 0, column = 1, padx = 10, pady = 10)
        datelabel2.place(relx = 0.35, rely = 0.17,anchor=NW)
        self.cal2 = Calendar(self, selectmode = 'day',year = 2022, month = 1, day = 21, date_pattern = 'dd-mm-yyy')
        self.cal2.grid(row = 0, column = 1, padx = 10, pady = 10)
        self.cal2.place(relx = 0.4, rely = 0.22,anchor=NW)

        button1 = ttk.Button(self, text ="Go Back to Main Page", command = lambda : controller.show_frame(MainPage))
        button1.grid(row = 2, column = 1, padx = 10, pady = 10)
        button1.place(relx = 0.7, rely = 0.03,anchor=NW)

        button2 = ttk.Button(self, text ="Display News",command = lambda : self.show_news())
        button2.grid(row = 1, column = 1, padx = 10, pady = 10)
        button2.place(relx = 0.82, rely = 0.22,anchor=NW)


        button3 = ttk.Button(self, text ="Display Response",command = lambda : self.show_resp())
        button3.grid(row = 1, column = 1, padx = 10, pady = 10)
        button3.place(relx = 0.82, rely = 0.34,anchor=NW)

        self.text_wid = scrolledtext.ScrolledText(self,undo = True,height=16,width=150)
        self.text_wid.grid(row = 1, column = 1, padx = 10, pady = 10)
        self.text_wid.place(relx = 0.07, rely = 0.56,anchor=NW)
    
    def compare_month_ony(self, m1, m2):
        month_list = list(calendar.month_name[1:])
        try:
            m1_idx = int(m1)
            m2_idx = month_list.index(m2) + 1

            if m1_idx > m2_idx:
                return -1
            elif m1_idx == m2_idx:
                return 0
            else:
                return 1
        except ValueError:
            return None
    
    def compare_date(self, yr1, m1, d1, date2):
        m1 = list(calendar.month_name[1:]).index(m1) + 1
        date1 = datetime.datetime(yr1,m1,int(d1))

        if date1 > date2:
            return -1
        elif date1 == date2:
            return 0
        else:
            return 1

    def show_news(self):
        start_date = self.cal.get_date()
        end_date = self.cal2.get_date()

        #-------------------converting start date to the relevant form for dictionary query
        start_datestr = start_date.split(sep = '-')             #['DD', 'MM', 'YYYY']
        sd = datetime.datetime(int(start_datestr[2]),int(start_datestr[1]),int(start_datestr[0]))
        #-------------------converting end date to the relevant form for dictionary query
        end_datestr = end_date.split(sep = '-')                 #['DD', 'MM', 'YYYY']
        ed = datetime.datetime(int(end_datestr[2]),int(end_datestr[1]),int(end_datestr[0]))
        #---------check if sd > ed
        if sd > ed:
            self.text_wid.configure(state='normal')
            self.text_wid.delete(1.0,END)
            self.text_wid.config(state='disabled')
            self.datalabel.config(text = 'Start date is greater than end date')
            if self.canvas != 0:
                self.canvas.get_tk_widget().destroy()
                self.canvas = 0
            return
        
        #--------extract all news between two given dates
        try:
            start_yr = int(start_datestr[-1])

            end_yr = int(end_datestr[-1])

            #---- News{yr: {month: {date: []}}} or News{yr: {month: []}}
            All_news = ''
            All_news_for_wc = ''
            for yr,year_news in news.items():
                for month,month_news in year_news.items():
                    if isinstance(month_news,list):
                        if self.compare_month_ony(start_datestr[1],month) is not None and self.compare_month_ony(end_datestr[1],month) is not None:
                            if start_yr == end_yr and start_yr == yr:
                                if self.compare_month_ony(start_datestr[1],month) >= 0 and self.compare_month_ony(end_datestr[1],month) <= 0:
                                    All_news += month + '/' + str(yr) + '-----------------------------------------------------------\n\n'
                                    for para in month_news:
                                        All_news_for_wc += para
                                        All_news += para + '\n'
                                    All_news += '------------------------------------------------------------------------------------------\n'
                                    All_news += '------------------------------------------------------------------------------------------\n\n'
                            elif start_yr >= yr and end_yr <= yr:
                                All_news += month + '/' + str(yr) + '-----------------------------------------------------------\n\n'
                                for para in month_news:
                                    All_news_for_wc += para
                                    All_news += para + '\n'
                                All_news += '------------------------------------------------------------------------------------------\n'
                                All_news += '------------------------------------------------------------------------------------------\n\n'
                            
                    else:
                        for date,date_news in month_news.items():
                            if self.compare_date(yr, month, date, sd) <= 0 and self.compare_date(yr, month, date, ed) >= 0:
                                All_news += date + '/' + month + '/'+  str(yr) + '-----------------------------------------------------------\n\n'
                                for para in date_news:
                                    All_news_for_wc += para
                                    All_news += para + '\n'
                                All_news += '------------------------------------------------------------------------------------------\n'
                                All_news += '------------------------------------------------------------------------------------------\n\n'
            if len(All_news) == 0:
                self.datalabel.config(text = 'Data Not Available')
                self.text_wid.configure(state='normal')
                self.text_wid.delete(1.0,END)
                self.text_wid.config(state='disabled')
                if self.canvas != 0:
                    self.canvas.get_tk_widget().destroy()
                    self.canvas = 0
            else:
                self.text_wid.configure(state='normal')
                self.text_wid.delete(1.0,END)
                self.text_wid.insert(tk.END,All_news)
                self.text_wid.config(state='disabled')
                self.datalabel.config(text='News: ')
                #--------Plot Word Cloud
                tkns1 = All_news_for_wc.split()
                for i in range(len(tkns1)):
                    tkns1[i] = tkns1[i].lower()
                    
                common_words = ' '.join(tkns1)
                #---------STOPWORDS
                stopwords = set(STOPWORDS)

                #---------Plotting WordCloud with only common words
                wordcloud = WordCloud(width = 800, height = 800, background_color ='white', stopwords = stopwords, min_font_size = 10).generate(common_words)

                fig = Figure(figsize = (4, 4), facecolor = None)
                a = fig.add_subplot(111)
                a.imshow(wordcloud)
                if self.canvas != 0:
                    self.canvas.get_tk_widget().destroy()
                    self.canvas = 0
                self.canvas = FigureCanvasTkAgg(fig, master = self)  
                self.canvas.draw()
                self.canvas.get_tk_widget().grid(column=1, row=0, padx = 10, pady = 10)
                self.canvas.get_tk_widget().place(relx = 0.6, rely = 0.17,anchor=NW)

        except KeyError:
            self.datalabel.config(text = 'Data Not Available')
            self.text_wid.configure(state='normal')
            self.text_wid.delete(1.0,END)
            self.text_wid.insert(tk.END,All_news)
            self.text_wid.config(state='disabled')
            if self.canvas != 0:
                self.canvas.get_tk_widget().destroy()
                self.canvas = 0
    
    def show_resp(self):
        start_date = self.cal.get_date()
        end_date = self.cal2.get_date()

        #-------------------converting start date to the relevant form for dictionary query
        start_datestr = start_date.split(sep = '-')             #['DD', 'MM', 'YYYY']
        sd = datetime.datetime(int(start_datestr[2]),int(start_datestr[1]),int(start_datestr[0]))
        #-------------------converting end date to the relevant form for dictionary query
        end_datestr = end_date.split(sep = '-')                 #['DD', 'MM', 'YYYY']
        ed = datetime.datetime(int(end_datestr[2]),int(end_datestr[1]),int(end_datestr[0]))
        #---------check if sd > ed
        if sd > ed:
            self.text_wid.configure(state='normal')
            self.text_wid.delete(1.0,END)
            self.text_wid.config(state='disabled')
            self.datalabel.config(text = 'Start date is greater than end date')
            if self.canvas != 0:
                self.canvas.get_tk_widget().destroy()
                self.canvas = 0
            return
        
        #--------extract all news between two given dates
        try:
            start_yr = int(start_datestr[-1])

            end_yr = int(end_datestr[-1])

            #---- News{yr: {month: {date: []}}} or News{yr: {month: []}}
            All_news = ''
            All_news_for_wc = ''
            for yr,year_news in resp.items():
                for month,month_news in year_news.items():
                    if isinstance(month_news,list):
                        if self.compare_month_ony(start_datestr[1],month) is not None and self.compare_month_ony(end_datestr[1],month) is not None:
                            if start_yr == end_yr:
                                if self.compare_month_ony(start_datestr[1],month) >= 0 and self.compare_month_ony(end_datestr[1],month) <= 0:
                                    All_news += month + '/' + str(yr) + '-----------------------------------------------------------\n\n'
                                    for para in month_news:
                                        All_news_for_wc += para
                                        All_news += para + '\n'
                                    All_news += '------------------------------------------------------------------------------------------\n'
                                    All_news += '------------------------------------------------------------------------------------------\n\n'
                            elif start_yr >= yr and end_yr <= yr:
                                All_news += month + '/' + str(yr) + '-----------------------------------------------------------\n\n'
                                for para in month_news:
                                    All_news_for_wc += para
                                    All_news += para + '\n'
                                All_news += '------------------------------------------------------------------------------------------\n'
                                All_news += '------------------------------------------------------------------------------------------\n\n'
                            
                    else:
                        for date,date_news in month_news.items():
                            if self.compare_date(yr, month, date, sd) <= 0 and self.compare_date(yr, month, date, ed) >= 0:
                                All_news += date + '/' + month + '/'+  str(yr) + '-----------------------------------------------------------\n\n'
                                for para in date_news:
                                    All_news_for_wc += para
                                    All_news += para + '\n'
                                All_news += '------------------------------------------------------------------------------------------\n'
                                All_news += '------------------------------------------------------------------------------------------\n\n'
            if len(All_news) == 0:
                self.datalabel.config(text = 'Data Not Available')
                self.text_wid.configure(state='normal')
                self.text_wid.delete(1.0,END)
                self.text_wid.config(state='disabled')
                if self.canvas != 0:
                    self.canvas.get_tk_widget().destroy()
                    self.canvas = 0
            else:
                self.text_wid.configure(state='normal')
                self.text_wid.delete(1.0,END)
                self.text_wid.insert(tk.END,All_news)
                self.text_wid.config(state='disabled')
                self.datalabel.config(text='Response: ')

                #--------Plot Word Cloud
                tkns1 = All_news_for_wc.split()
                for i in range(len(tkns1)):
                    tkns1[i] = tkns1[i].lower()
                    
                common_words = ' '.join(tkns1)
                #---------STOPWORDS
                stopwords = set(STOPWORDS)

                #---------Plotting WordCloud with only common words
                wordcloud = WordCloud(width = 800, height = 800, background_color ='white', stopwords = stopwords, min_font_size = 10).generate(common_words)

                fig = Figure(figsize = (4, 4), facecolor = None)
                a = fig.add_subplot(111)
                a.imshow(wordcloud)
                if self.canvas != 0:
                    self.canvas.get_tk_widget().destroy()
                    self.canvas = 0
                self.canvas = FigureCanvasTkAgg(fig, master = self)  
                self.canvas.draw()
                self.canvas.get_tk_widget().grid(column=1, row=0, padx = 10, pady = 10)
                self.canvas.get_tk_widget().place(relx = 0.6, rely = 0.17,anchor=NW)

        except KeyError:
            self.datalabel.config(text = 'Data Not Available')
            self.text_wid.configure(state='normal')
            self.text_wid.delete(1.0,END)
            self.text_wid.insert(tk.END,All_news)
            self.text_wid.config(state='disabled')
            if self.canvas != 0:
                self.canvas.get_tk_widget().destroy()
                self.canvas = 0

#Date Range Page
class Date_range_Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.data_label = ttk.Label(self, text ="",font=("Times New Roman", 15))
        self.data_label.grid(row = 0, column = 1, padx = 10, pady = 10)
        self.data_label.place(relx = 0.1, rely = 0.45,anchor=NW)


        label = ttk.Label(self, text ="Date Range Page", font = LARGEFONT)
        label.grid(row = 0, column = 1, padx = 10, pady = 10)
        label.place(relx = 0.35, rely = 0.02,anchor=NW)

        #select continent
        conlabel = ttk.Label(self, text ="Select Country:")
        conlabel.grid(row = 0, column = 1, padx = 10, pady = 10)
        conlabel.place(relx = 0.15, rely = 0.22,anchor=NW)

        #Drop down menu of continent list
        Country_list = [
            'Argentina',
            'Australia',
            'Bangladesh',
            'Brazil',
            'Ghana',
            'India',
            'Indonesia',
            'Ireland',
            'Malaysia',
            'Mexico',
            'New Zealand',
            'Nigeria',
            'Pakistan',
            'Philippines',
            'Singapore',
            'South Africa',
            'Spain',
            'Turkey',
            'England'
]
        self.clicked = StringVar()
        self.clicked.set('India')
        drop = OptionMenu(self, self.clicked , *Country_list)
        drop.grid(row = 0, column = 1, padx = 10, pady = 10)
        drop.place(relx = 0.27, rely = 0.205,anchor=NW)

        button1 = ttk.Button(self, text ="View Range", command = lambda : self.show_range())
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)
        button1.place(relx = 0.4, rely = 0.32,anchor=NW)

        button2 = ttk.Button(self, text ="Go Back to Main Page", command = lambda : controller.show_frame(MainPage))
        button2.grid(row = 2, column = 1, padx = 10, pady = 10)
        button2.place(relx = 0.65, rely = 0.03,anchor=NW)

    def show_range(self):
        c = self.clicked.get()
        txt = 'News for '
        txt += c
        txt += ' is available from '
        txt += date_range[c][0][0] + '-' + date_range[c][0][1]
        txt += ' to '
        txt += date_range[c][1][0] + '-' + date_range[c][1][1]
        self.data_label.config(text=txt)

#Word Cloud Page
class wordC(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.canvas = 0
        self.canvas2 = 0
        self.datalabel = ttk.Label(self,text="", font = ("Times New Roman", 15))
        self.datalabel.grid(row = 0, column = 1, padx = 10, pady = 10)
        self.datalabel.place(relx = 0.07, rely = 0.45,anchor=NW)

        self.percentlabel = ttk.Label(self,text="", font = ("Times New Roman", 15))
        self.percentlabel.grid(row = 0, column = 1, padx = 10, pady = 10)
        self.percentlabel.place(relx = 0.25, rely = 0.85,anchor=NW)

        self.common_words = ttk.Label(self,text="", font = ("Times New Roman", 15))
        self.common_words.grid(row = 0, column = 1, padx = 10, pady = 10)
        self.common_words.place(relx = 0.07, rely = 0.37,anchor=NW)

        self.covid_common_words = ttk.Label(self,text="", font = ("Times New Roman", 15))
        self.covid_common_words.grid(row = 0, column = 1, padx = 10, pady = 10)
        self.covid_common_words.place(relx = 0.4, rely = 0.37,anchor=NW)

        label = ttk.Label(self, text ="Word Cloud Page", font = LARGEFONT)  
        label.grid(row = 0, column = 4, padx = 10, pady = 10)
        label.place(relx = 0.4, rely = 0.02,anchor=NW)

        #Range1 Label
        SR_label = ttk.Label(self,text="First Range", font = ("Times New Roman", 15))
        SR_label.grid(row = 0, column = 1, padx = 10, pady = 10)
        SR_label.place(relx = 0.07, rely = 0.15,anchor=NW)

        #Range2 Label
        SR_label2 = ttk.Label(self,text="Second Range", font = ("Times New Roman", 15))
        SR_label2.grid(row = 0, column = 1, padx = 10, pady = 10)
        SR_label2.place(relx = 0.4, rely = 0.15,anchor=NW)
        
        #select the start date of Range
        datelabel = ttk.Label(self, text ="Select start Date:")
        datelabel.grid(row = 0, column = 1, padx = 10, pady = 10)
        datelabel.place(relx = 0.07, rely = 0.22,anchor=NW)
        self.cal = DateEntry(self, selectmode = 'day', year = 2019, month = 1, day = 21, dateformat = 'dd-mm-yyyy', state='readonly')
        self.cal.grid(row = 0, column = 1, padx = 10, pady = 10)
        self.cal.place(relx = 0.18, rely = 0.22,anchor=NW)

        #select the end date of Range1
        datelabel2 = ttk.Label(self, text ="Select End Date:")
        datelabel2.grid(row = 0, column = 1, padx = 10, pady = 10)
        datelabel2.place(relx = 0.07, rely = 0.3,anchor=NW)
        self.cal2 = DateEntry(self, selectmode = 'day', year = 2020, month = 1, day = 22, dateformat = 'dd-mm-yyyy', state='readonly')
        self.cal2.grid(row = 0, column = 1, padx = 10, pady = 10)
        self.cal2.place(relx = 0.18, rely = 0.3,anchor=NW)

        #select the start date of Range2
        datelabel3 = ttk.Label(self, text ="Select start Date:")
        datelabel3.grid(row = 0, column = 1, padx = 10, pady = 10)
        datelabel3.place(relx = 0.4, rely = 0.22,anchor=NW)
        self.cal3 = DateEntry(self, selectmode = 'day', year = 2021, month = 1, day = 23, dateformat = 'dd-mm-yyyy', state='readonly')
        self.cal3.grid(row = 0, column = 1, padx = 10, pady = 10)
        self.cal3.place(relx = 0.51, rely = 0.22,anchor=NW)

        #select the end date of Range2
        datelabel4 = ttk.Label(self, text ="Select End Date:")
        datelabel4.grid(row = 0, column = 1, padx = 10, pady = 10)
        datelabel4.place(relx = 0.4, rely = 0.3,anchor=NW)
        self.cal4 = DateEntry(self, selectmode = 'day', year = 2022, month = 1, day = 24, dateformat = 'dd-mm-yyyy', state='readonly')
        self.cal4.grid(row = 0, column = 1, padx = 10, pady = 10)
        self.cal4.place(relx = 0.51, rely = 0.3,anchor=NW)

        button1 = ttk.Button(self, text ="Go Back to Main Page", command = lambda : controller.show_frame(MainPage))
        button1.grid(row = 2, column = 1, padx = 10, pady = 10)
        button1.place(relx = 0.7, rely = 0.03,anchor=NW)

        button2 = ttk.Button(self, text ="Plot Word Cloud",command = lambda : self.Plot())
        button2.grid(row = 1, column = 1, padx = 10, pady = 10)
        button2.place(relx = 0.82, rely = 0.20,anchor=NW)

        button3 = ttk.Button(self, text ="% Covid Words",command = lambda : self.Covid_word_percentage())
        button3.grid(row = 1, column = 1, padx = 10, pady = 10)
        button3.place(relx = 0.82, rely = 0.3,anchor=NW)

        button4 = ttk.Button(self, text ="Top 20 Common Words",command = lambda : self.top20())
        button4.grid(row = 1, column = 1, padx = 10, pady = 10)
        button4.place(relx = 0.82, rely = 0.4,anchor=NW)

        self.text_wid_common = scrolledtext.ScrolledText(self,undo = True,height=16,width=20,state='disabled')
        self.text_wid_common.grid(row = 1, column = 1, padx = 10, pady = 10)
        self.text_wid_common.place(relx = 0.82, rely = 0.55,anchor=NW)

        self.text_wid_common_covid = scrolledtext.ScrolledText(self,undo = True,height=16,width=20,state='disabled')
        self.text_wid_common_covid.grid(row = 1, column = 1, padx = 10, pady = 10)
        self.text_wid_common_covid.place(relx = 0.65, rely = 0.55,anchor=NW)

        self.labeltop20Common = ttk.Label(self, text ="Top 20 Common Words:")
        self.labeltop20Common.grid(row = 0, column = 1, padx = 10, pady = 10)
        self.labeltop20Common.place(relx = 0.82, rely = 0.50,anchor=NW)

        self.labeltop20CovidCommon = ttk.Label(self, text ="Top 20 Common covid words:")
        self.labeltop20CovidCommon.grid(row = 0, column = 1, padx = 10, pady = 10)
        self.labeltop20CovidCommon.place(relx = 0.65, rely = 0.50,anchor=NW)

    def compare_month_ony(self, m1, m2):
        month_list = list(calendar.month_name[1:])
        try:
            m1_idx = int(m1)
            m2_idx = month_list.index(m2) + 1

            if m1_idx > m2_idx:
                return -1
            elif m1_idx == m2_idx:
                return 0
            else:
                return 1
        except ValueError:
            return None
    
    def compare_date(self, yr1, m1, d1, date2):
        m1 = list(calendar.month_name[1:]).index(m1) + 1
        date1 = datetime.date(yr1,m1,int(d1))

        if date1 > date2:
            return -1
        elif date1 == date2:
            return 0
        else:
            return 1

    def get_news(self, start_date, end_date):
        
        #--------extract all news between two given dates
        try:
            start_yr = int(start_date.year)

            end_yr = int(end_date.year)

            #---- News{yr: {month: {date: []}}} or News{yr: {month: []}}
            All_news = ''
            for yr,year_news in news.items():
                for month,month_news in year_news.items():
                    if isinstance(month_news,list):
                        if self.compare_month_ony(start_date.month,month) is not None and self.compare_month_ony(end_date.month,month) is not None:
                            if start_yr == end_yr and start_yr == yr:
                                if self.compare_month_ony(start_date.month,month) >= 0 and self.compare_month_ony(end_date.month,month) <= 0:
                                    for para in month_news:
                                        All_news += para
                            elif start_yr >= yr and end_yr <= yr:
                                for para in month_news:
                                    All_news += para
                            
                    else:
                        for date,date_news in month_news.items():
                            if self.compare_date(yr, month, date, start_date) <= 0 and self.compare_date(yr, month, date, end_date) >= 0:
                                for para in date_news:
                                    All_news += para
            if len(All_news) == 0:
                return ''
            else:
                return All_news

        except KeyError:
            return ''
    
    def Covid_word_percentage(self):
        R1S = self.cal.get_date()
        R1E = self.cal2.get_date()

        R2S = self.cal3.get_date()
        R2E = self.cal4.get_date()

        if R1S > R1E:
            #-----check for valid 1st Range
            self.percentlabel.config(text='Start Date is greater than End Date for 1st Range')
            return
        elif R2S > R2E:
            #-----check for valid 1st Range
            self.percentlabel.config(text='Start Date is greater than End Date for 2nd Range')
            return
        
        #----check for overlapping Date Range
        if max(R1S,R2S) < min(R1E,R2E):
            self.percentlabel.config(text='Overlapping Time Range')
            return

        #-----get all news
        News_R1 = self.get_news(R1S, R1E)
        News_R2 = self.get_news(R2S, R2E)

        pr = round(percent_covid_words(News_R1,News_R2),5)*100
        txt = str(pr) + '% common covid words'
        self.percentlabel.config(text = txt)

    def top20(self):
        R1S = self.cal.get_date()
        R1E = self.cal2.get_date()

        R2S = self.cal3.get_date()
        R2E = self.cal4.get_date()

        if R1S > R1E:
            #-----check for valid 1st Range
            self.text_wid_common.config(state = 'normal')
            self.text_wid_common.delete(1.0,END)
            self.text_wid_common.config(state='disabled')
            self.text_wid_common_covid.config(state = 'normal')
            self.text_wid_common_covid.delete(1.0,END)
            self.text_wid_common_covid.config(state='disabled')
            self.percentlabel.config(text='Start Date is greater than End Date for 1st Range')
            return
        elif R2S > R2E:
            #-----check for valid 1st Range
            self.text_wid_common.config(state = 'normal')
            self.text_wid_common.delete(1.0,END)
            self.text_wid_common.config(state='disabled')
            self.text_wid_common_covid.config(state = 'normal')
            self.text_wid_common_covid.delete(1.0,END)
            self.text_wid_common_covid.config(state='disabled')
            self.percentlabel.config(text='Start Date is greater than End Date for 2nd Range')
            return
        
        #----check for overlapping Date Range
        if max(R1S,R2S) < min(R1E,R2E):
            self.text_wid_common.config(state = 'normal')
            self.text_wid_common.delete(1.0,END)
            self.text_wid_common.config(state='disabled')
            self.text_wid_common_covid.config(state = 'normal')
            self.text_wid_common_covid.delete(1.0,END)
            self.text_wid_common_covid.config(state='disabled')
            self.percentlabel.config(text='Overlapping Time Range')
            return
        
        self.percentlabel.config(text='')

        #-----get all news
        News_R1 = self.get_news(R1S, R1E)
        News_R2 = self.get_news(R2S, R2E)

        t1 = top20common(News_R1,News_R2)
        self.text_wid_common.config(state = 'normal')
        self.text_wid_common.delete(1.0,END)
        self.text_wid_common.insert(tk.END,t1)
        self.text_wid_common.config(state='disabled')

        t1 = top20common(News_R1,News_R2,True)
        self.text_wid_common_covid.config(state = 'normal')
        self.text_wid_common_covid.delete(1.0,END)
        self.text_wid_common_covid.insert(tk.END,t1)
        self.text_wid_common_covid.config(state='disabled')

    def Plot(self):
        R1S = self.cal.get_date()
        R1E = self.cal2.get_date()

        R2S = self.cal3.get_date()
        R2E = self.cal4.get_date()

        if R1S > R1E:
            #-----check for valid 1st Range
            self.common_words.config(text='')
            self.covid_common_words.config(text='')
            if self.canvas != 0:
                self.canvas.get_tk_widget().destroy()
                self.canvas = 0
            if self.canvas2 != 0:
                self.canvas2.get_tk_widget().destroy()
                self.canvas2 = 0
            self.percentlabel.config(text='')
            self.datalabel.config(text='Start Date is greater than End Date for 1st Range')
            return
        elif R2S > R2E:
            self.common_words.config(text='')
            self.covid_common_words.config(text='')
            if self.canvas != 0:
                self.canvas.get_tk_widget().destroy()
                self.canvas = 0
            if self.canvas2 != 0:
                self.canvas2.get_tk_widget().destroy()
                self.canvas2 = 0
            #-----check for valid 1st Range
            self.datalabel.config(text='Start Date is greater than End Date for 2nd Range')
            self.percentlabel.config(text='')
            return
        
        #----check for overlapping Date Range
        if max(R1S,R2S) < min(R1E,R2E):
            self.common_words.config(text='')
            self.covid_common_words.config(text='')
            if self.canvas != 0:
                self.canvas.get_tk_widget().destroy()
                self.canvas = 0
            if self.canvas2 != 0:
                self.canvas2.get_tk_widget().destroy()
                self.canvas2 = 0
            self.datalabel.config(text='Overlapping Time Range')
            self.percentlabel.config(text='')
            return


        #-----get all news
        News_R1 = self.get_news(R1S, R1E)
        News_R2 = self.get_news(R2S, R2E)
        try:
            #-------Plotting WordCloud with only common words
            self.datalabel.config(text='')
            self.common_words.config(text='Word Cloud with Common Words')
            Wordcloud = generate_word_cloud(News_R1,News_R2,False)
            fig = Figure(figsize = (4, 4), facecolor = None)
            a = fig.add_subplot(111)
            a.imshow(Wordcloud)
            if self.canvas != 0:
                self.canvas.get_tk_widget().destroy()
                self.canvas = 0
            self.canvas = FigureCanvasTkAgg(fig, master = self)  
            self.canvas.draw()
            self.canvas.get_tk_widget().grid(column=1, row=0, padx = 10, pady = 10)
            self.canvas.get_tk_widget().place(relx = 0.07, rely = 0.42,anchor=NW)

            #-------Plotting WordCloud with Covid common words
            self.datalabel.config(text='')
            self.covid_common_words.config(text='Word Cloud with Covid Common Words')
            Wordcloud = generate_word_cloud(News_R1,News_R2,True)
            fig = Figure(figsize = (4, 4), facecolor = None)
            a = fig.add_subplot(111)
            a.imshow(Wordcloud)
            if self.canvas2 != 0:
                self.canvas2.get_tk_widget().destroy()
                self.canvas2 = 0
            self.canvas2 = FigureCanvasTkAgg(fig, master = self)  
            self.canvas2.draw()
            self.canvas2.get_tk_widget().grid(column=1, row=0, padx = 10, pady = 10)
            self.canvas2.get_tk_widget().place(relx = 0.4, rely = 0.42,anchor=NW)
        except:
            self.common_words.config(text='')
            self.covid_common_words.config(text='')
            if self.canvas != 0:
                self.canvas.get_tk_widget().destroy()
                self.canvas = 0
            if self.canvas2 != 0:
                self.canvas2.get_tk_widget().destroy()
                self.canvas2 = 0
            self.datalabel.config(text='No Common Word found while forming one/both of the Word Cloud')
            self.percentlabel.config(text='')

#Country News Page
class country_news_page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.canvas = 0

        self.datalabel = ttk.Label(self,text="", font = ("Times New Roman", 15))
        self.datalabel.grid(row = 0, column = 1, padx = 10, pady = 10)
        self.datalabel.place(relx = 0.1, rely = 0.5,anchor=NW)

        label = ttk.Label(self, text ="Country News Page", font = LARGEFONT)
        label.grid(row = 0, column = 4, padx = 10, pady = 10)
        label.place(relx = 0.35, rely = 0.02,anchor=NW)

        #select Country
        conlabel = ttk.Label(self, text ="Select Country:")
        conlabel.grid(row = 0, column = 1, padx = 10, pady = 10)
        conlabel.place(relx = 0.12, rely = 0.17,anchor=NW)

        #Drop down menu of continent list
        Country_list = [
            'Argentina',
            'Australia',
            'Bangladesh',
            'Brazil',
            'Ghana',
            'India',
            'Indonesia',
            'Ireland',
            'Malaysia',
            'Mexico',
            'New Zealand',
            'Nigeria',
            'Pakistan',
            'Philippines',
            'Singapore',
            'South Africa',
            'Spain',
            'Turkey',
            'England'
        ]
        self.clicked = StringVar()
        self.clicked.set('Argentina')
        drop = OptionMenu(self, self.clicked , *Country_list)
        drop.grid(row = 0, column = 1, padx = 10, pady = 10)
        drop.place(relx = 0.2, rely = 0.16,anchor=NW)

        #select the start date
        datelabel = ttk.Label(self, text ="Select start Date:")
        datelabel.grid(row = 0, column = 1, padx = 10, pady = 10)
        datelabel.place(relx = 0.32, rely = 0.17,anchor=NW)
        self.cal = Calendar(self, selectmode = 'day',year = 2020, month = 7, day = 21, date_pattern = 'dd-mm-yyy')
        self.cal.grid(row = 0, column = 1, padx = 10, pady = 10)
        self.cal.place(relx = 0.32, rely = 0.22,anchor=NW)

        #select the end date
        datelabel2 = ttk.Label(self, text ="Select End Date:")
        datelabel2.grid(row = 0, column = 1, padx = 10, pady = 10)
        datelabel2.place(relx = 0.52, rely = 0.17,anchor=NW)
        self.cal2 = Calendar(self, selectmode = 'day',year = 2020, month = 8, day = 6, date_pattern = 'dd-mm-yyy')
        self.cal2.grid(row = 0, column = 1, padx = 10, pady = 10)
        self.cal2.place(relx = 0.52, rely = 0.22,anchor=NW)

        button1 = ttk.Button(self, text ="Go Back to Main Page", command = lambda : controller.show_frame(MainPage))
        button1.grid(row = 2, column = 1, padx = 10, pady = 10)
        button1.place(relx = 0.7, rely = 0.03,anchor=NW)

        button2 = ttk.Button(self, text ="Display News and Plot Word Cloud",command = lambda : self.show_news())
        button2.grid(row = 1, column = 1, padx = 10, pady = 10)
        button2.place(relx = 0.12, rely = 0.3,anchor=NW)

        self.text_wid = scrolledtext.ScrolledText(self,undo = True,height=16,width=150)
        self.text_wid.grid(row = 1, column = 1, padx = 10, pady = 10)
        self.text_wid.place(relx = 0.07, rely = 0.56,anchor=NW)
            

        
    def compare_month_ony(self, m1, m2):
        month_list = list(calendar.month_name[1:])
        try:
            m1_idx = int(m1)
            m2_idx = month_list.index(m2) + 1

            if m1_idx > m2_idx:
                return -1
            elif m1_idx == m2_idx:
                return 0
            else:
                return 1
        except ValueError:
            return None
    
    def compare_date(self, yr1, m1, d1, date2):
        try:
            m1 = list(calendar.month_name[1:]).index(m1) + 1
            date1 = datetime.datetime(yr1,m1,int(d1))

            if date1 > date2:
                return -1
            elif date1 == date2:
                return 0
            else:
                return 1
        except:
            return -1

    def show_news(self):
        start_date = self.cal.get_date()
        end_date = self.cal2.get_date()

        c_news = country_news[self.clicked.get()]

        #-------------------converting start date to the relevant form for dictionary query
        start_datestr = start_date.split(sep = '-')             #['DD', 'MM', 'YYYY']
        sd = datetime.datetime(int(start_datestr[2]),int(start_datestr[1]),int(start_datestr[0]))
        #-------------------converting end date to the relevant form for dictionary query
        end_datestr = end_date.split(sep = '-')                 #['DD', 'MM', 'YYYY']
        ed = datetime.datetime(int(end_datestr[2]),int(end_datestr[1]),int(end_datestr[0]))
        #---------check if sd > ed
        if sd > ed:
            self.text_wid.configure(state='normal')
            self.text_wid.delete(1.0,END)
            self.text_wid.config(state='disabled')
            self.datalabel.config(text = 'Start date is greater than end date')
            if self.canvas != 0:
                self.canvas.get_tk_widget().destroy()
                self.canvas = 0
            return
        
        #--------extract all news between two given dates
        try:
            start_yr = int(start_datestr[-1])

            end_yr = int(end_datestr[-1])

            #---- News{yr: {month: {date: []}}} or News{yr: {month: []}}
            All_news = ''
            All_news_for_wc = ''
            for yr,year_news in c_news.items():
                for month,month_news in year_news.items():
                    if isinstance(month_news,list):
                        if self.compare_month_ony(start_datestr[1],month) is not None and self.compare_month_ony(end_datestr[1],month) is not None:
                            if start_yr == end_yr and start_yr == yr:
                                if self.compare_month_ony(start_datestr[1],month) >= 0 and self.compare_month_ony(end_datestr[1],month) <= 0:
                                    All_news += month + '/' + str(yr) + '-----------------------------------------------------------\n\n'
                                    for para in month_news:
                                        All_news_for_wc += para
                                        All_news += para + '\n'
                                    All_news += '------------------------------------------------------------------------------------------\n'
                                    All_news += '------------------------------------------------------------------------------------------\n\n'
                            elif start_yr >= yr and end_yr <= yr:
                                All_news += month + '/' + str(yr) + '-----------------------------------------------------------\n\n'
                                for para in month_news:
                                    All_news_for_wc += para
                                    All_news += para + '\n'
                                All_news += '------------------------------------------------------------------------------------------\n'
                                All_news += '------------------------------------------------------------------------------------------\n\n'
                            
                    else:
                        for date,date_news in month_news.items():
                            if self.compare_date(yr, month, date, sd) <= 0 and self.compare_date(yr, month, date, ed) >= 0:
                                All_news += date + '/' + month + '/'+  str(yr) + '-----------------------------------------------------------\n\n'
                                for para in date_news:
                                    All_news_for_wc += para
                                    All_news += para + '\n'
                                All_news += '------------------------------------------------------------------------------------------\n'
                                All_news += '------------------------------------------------------------------------------------------\n\n'
            if len(All_news) == 0:
                self.datalabel.config(text = 'Data Not Available')
                self.text_wid.configure(state='normal')
                self.text_wid.delete(1.0,END)
                self.text_wid.config(state='disabled')
                if self.canvas != 0:
                    self.canvas.get_tk_widget().destroy()
                    self.canvas = 0
            else:
                self.text_wid.configure(state='normal')
                self.text_wid.delete(1.0,END)
                self.text_wid.insert(tk.END,All_news)
                self.text_wid.config(state='disabled')
                self.datalabel.config(text='News: ')

                #--------Plot Word Cloud
                tkns1 = All_news_for_wc.split()
                for i in range(len(tkns1)):
                    tkns1[i] = tkns1[i].lower()
                    
                common_words = ' '.join(tkns1)
                #---------STOPWORDS
                stopwords = set(STOPWORDS)

                #---------Plotting WordCloud with only common words
                wordcloud = WordCloud(width = 800, height = 800, background_color ='white', stopwords = stopwords, min_font_size = 10).generate(common_words)

                fig = Figure(figsize = (4, 4), facecolor = None)
                a = fig.add_subplot(111)
                a.imshow(wordcloud)
                if self.canvas != 0:
                    self.canvas.get_tk_widget().destroy()
                    self.canvas = 0
                self.canvas = FigureCanvasTkAgg(fig, master = self)  
                self.canvas.draw()
                self.canvas.get_tk_widget().grid(column=1, row=0, padx = 10, pady = 10)
                self.canvas.get_tk_widget().place(relx = 0.75, rely = 0.17,anchor=NW)

        except KeyError:
            self.datalabel.config(text = 'Data Not Available')
            self.text_wid.configure(state='normal')
            self.text_wid.delete(1.0,END)
            self.text_wid.insert(tk.END,All_news)
            self.text_wid.config(state='disabled')
            if self.canvas != 0:
                self.canvas.get_tk_widget().destroy()
                self.canvas = 0

class Jaccard_similarity_page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.datalabel = ttk.Label(self,text="", font = ("Times New Roman", 15))
        self.datalabel.grid(row = 0, column = 1, padx = 10, pady = 10)
        self.datalabel.place(relx = 0.4, rely = 0.63,anchor=NW)

        label = ttk.Label(self, text ="Jaccard Similarity Page", font = LARGEFONT)
        label.grid(row = 0, column = 4, padx = 10, pady = 10)
        label.place(relx = 0.35, rely = 0.02,anchor=NW)

        #select Country
        conlabel = ttk.Label(self, text ="Select Country:")
        conlabel.grid(row = 0, column = 1, padx = 10, pady = 10)
        conlabel.place(relx = 0.12, rely = 0.17,anchor=NW)

        #Drop down menu of continent list
        self.Country_list = [
            'Argentina',
            'Australia',
            'Bangladesh',
            'Brazil',
            'Ghana',
            'India',
            'Indonesia',
            'Ireland',
            'Malaysia',
            'Mexico',
            'New Zealand',
            'Nigeria',
            'Pakistan',
            'Philippines',
            'Singapore',
            'South Africa',
            'Spain',
            'Turkey',
            'England'
        ]
        self.clicked = StringVar()
        self.clicked.set('Argentina')
        drop = OptionMenu(self, self.clicked , *self.Country_list)
        drop.grid(row = 0, column = 1, padx = 10, pady = 10)
        drop.place(relx = 0.2, rely = 0.16,anchor=NW)

        #select the start date
        datelabel = ttk.Label(self, text ="Select start Date:")
        datelabel.grid(row = 0, column = 1, padx = 10, pady = 10)
        datelabel.place(relx = 0.35, rely = 0.17,anchor=NW)
        self.cal = Calendar(self, selectmode = 'day',year = 2020, month = 7, day = 21, date_pattern = 'dd-mm-yyy')
        self.cal.grid(row = 0, column = 1, padx = 10, pady = 10)
        self.cal.place(relx = 0.35, rely = 0.22,anchor=NW)

        #select the end date
        datelabel2 = ttk.Label(self, text ="Select End Date:")
        datelabel2.grid(row = 0, column = 1, padx = 10, pady = 10)
        datelabel2.place(relx = 0.6, rely = 0.17,anchor=NW)
        self.cal2 = Calendar(self, selectmode = 'day',year = 2020, month = 8, day = 6, date_pattern = 'dd-mm-yyy')
        self.cal2.grid(row = 0, column = 1, padx = 10, pady = 10)
        self.cal2.place(relx = 0.6, rely = 0.22,anchor=NW)

        button1 = ttk.Button(self, text ="Go Back to Main Page", command = lambda : controller.show_frame(MainPage))
        button1.grid(row = 2, column = 1, padx = 10, pady = 10)
        button1.place(relx = 0.7, rely = 0.03,anchor=NW)

        button2 = ttk.Button(self, text ="3 Most Similar Countries",command = lambda : self.similarity())
        button2.grid(row = 1, column = 1, padx = 10, pady = 10)
        button2.place(relx = 0.1, rely = 0.6,anchor=NW)

        button3 = ttk.Button(self, text ="3 Most Similar Countries(only common covid words)",command = lambda : self.similarity(True))
        button3.grid(row = 1, column = 1, padx = 10, pady = 10)
        button3.place(relx = 0.1, rely = 0.7,anchor=NW)
    
    def compare_month_ony(self, m1, m2):
        month_list = list(calendar.month_name[1:])
        try:
            m1_idx = int(m1)
            m2_idx = month_list.index(m2) + 1

            if m1_idx > m2_idx:
                return -1
            elif m1_idx == m2_idx:
                return 0
            else:
                return 1
        except ValueError:
            return None
    
    def compare_date(self, yr1, m1, d1, date2):
        m1 = list(calendar.month_name[1:]).index(m1) + 1
        date1 = datetime.datetime(yr1,m1,int(d1))

        if date1 > date2:
            return -1
        elif date1 == date2:
            return 0
        else:
            return 1
    
    def get_news(self, start_date, end_date, c):
        
        #--------extract all news between two given dates
        try:
            start_yr = int(start_date.year)

            end_yr = int(end_date.year)

            #---- News{yr: {month: {date: []}}} or News{yr: {month: []}}
            c_news = country_news[c]
            All_news = ''
            for yr,year_news in c_news.items():
                for month,month_news in year_news.items():
                    if isinstance(month_news,list):
                        if self.compare_month_ony(start_date.month,month) is not None and self.compare_month_ony(end_date.month,month) is not None:
                            if start_yr == end_yr and start_yr == yr:
                                if self.compare_month_ony(start_date.month,month) >= 0 and self.compare_month_ony(end_date.month,month) <= 0:
                                    for para in month_news:
                                        All_news += para
                            elif start_yr >= yr and end_yr <= yr:
                                for para in month_news:
                                    All_news += para
                            
                    else:
                        for date,date_news in month_news.items():
                            if self.compare_date(yr, month, date, start_date) <= 0 and self.compare_date(yr, month, date, end_date) >= 0:
                                for para in date_news:
                                    All_news += para
            if len(All_news) == 0:
                return ''
            else:
                return All_news

        except KeyError:
            return ''
    
    def jaccard_sim(self,str1,str2,covid):
        #---------For 1st string
        tkns1 = str1.split()
        for i in range(len(tkns1)):
            tkns1[i] = tkns1[i].lower()
        temp = []
        for w in tkns1:
            if w not in stop_words:
                temp.append(w)
        tkns1 = temp
        
        #---------For 2nd string
        tkns2 = str2.split()
        for i in range(len(tkns2)):
            tkns2[i] = tkns2[i].lower()
        temp = []
        for w in tkns2:
            if w not in stop_words:
                temp.append(w)
        tkns2 = temp
        
        numerator = list(set(tkns1) & set(tkns2))
        denominator = list(set(tkns1) | set(tkns2))
        if covid:
            numerator = list(set(numerator) & set(covid_words))
            denominator =list(set(denominator) & set(covid_words))

        return len(numerator)/len(denominator)

    def similarity(self,covid = False):
        start_date = self.cal.get_date()
        end_date = self.cal2.get_date()

        #-------------------converting start date to the relevant form for dictionary query
        start_datestr = start_date.split(sep = '-')             #['DD', 'MM', 'YYYY']
        sd = datetime.datetime(int(start_datestr[2]),int(start_datestr[1]),int(start_datestr[0]))
        #-------------------converting end date to the relevant form for dictionary query
        end_datestr = end_date.split(sep = '-')                 #['DD', 'MM', 'YYYY']
        ed = datetime.datetime(int(end_datestr[2]),int(end_datestr[1]),int(end_datestr[0]))
        #---------check if sd > ed
        if sd > ed:
            self.datalabel.config(text = 'Start date is greater than end date')
            return
        
        #------extract all news between two given dates for the given country
        All_news_country = self.get_news(sd, ed, self.clicked.get())
        if All_news_country == '':
            self.datalabel.config(text='Data not available')
            return
        jaccard_dict = {}

        for countr in self.Country_list:
            All_news = self.get_news(sd, ed, countr)
            jaccard_dict[countr] = self.jaccard_sim(All_news_country,All_news,covid)
        
        sorted_tuple = sorted(jaccard_dict.items(),key = operator.itemgetter(1))
        txt = str(sorted_tuple[0][0]) + ', ' + str(sorted_tuple[1][0]) + ' and ' + str(sorted_tuple[2][0]) + ' are the most similar countries.'
        self.datalabel.config(text = txt)

# Driver Code
app = tkinterApp()
app.geometry("1400x850")
app.mainloop()
app.quit()
#--------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
#%%
