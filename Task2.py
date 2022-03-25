#%%
#----------------------Program to extract the covid data from the website using ply lexer and yaac parser----------------
#download the file and save it
from cmath import log, nan
from curses.ascii import isdigit
from datetime import date, datetime
import os
import os.path
import requests

Covid_data = {}
Active_cases = [[],[]]
Daily_deaths = [[],[]]
New_Recoveries = [[],[]]
New_Cases = [[],[]]

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

country_list = {
    'France' : 'https://www.worldometers.info/coronavirus/country/france/',
    'UK' : 'https://www.worldometers.info/coronavirus/country/uk/',
    'Russia' : 'https://www.worldometers.info/coronavirus/country/russia/',
    'Italy' : 'https://www.worldometers.info/coronavirus/country/italy/',
    'Germany' : 'https://www.worldometers.info/coronavirus/country/germany/',
    'Spain': 'https://www.worldometers.info/coronavirus/country/spain/',
    'Poland': 'https://www.worldometers.info/coronavirus/country/poland/',
    'Netherlands' : 'https://www.worldometers.info/coronavirus/country/netherlands/',
    'Ukraine' : 'https://www.worldometers.info/coronavirus/country/ukraine/',
    'Belgium' : 'https://www.worldometers.info/coronavirus/country/belgium/',
    'USA' : 'https://www.worldometers.info/coronavirus/country/us/',
    'Mexico' : 'https://www.worldometers.info/coronavirus/country/mexico/',
    'Canada' : 'https://www.worldometers.info/coronavirus/country/canada/',
    'Cuba' : 'https://www.worldometers.info/coronavirus/country/cuba/',
    'Costa Rica' : 'https://www.worldometers.info/coronavirus/country/costa-rica/',
    'Panama' : 'https://www.worldometers.info/coronavirus/country/panama/',
    'India' : 'https://www.worldometers.info/coronavirus/country/india/',
    'Turkey' : 'https://www.worldometers.info/coronavirus/country/turkey/',
    'Iran' : 'https://www.worldometers.info/coronavirus/country/iran/',
    'Indonesia' : 'https://www.worldometers.info/coronavirus/country/indonesia/',
    'Philippines' : 'https://www.worldometers.info/coronavirus/country/philippines/',
    'Japan' : 'https://www.worldometers.info/coronavirus/country/japan/',
    'Israel' : 'https://www.worldometers.info/coronavirus/country/israel/',
    'Malaysia' : 'https://www.worldometers.info/coronavirus/country/malaysia/',
    'Thailand' : 'https://www.worldometers.info/coronavirus/country/thailand/',
    'Vietnam' : 'https://www.worldometers.info/coronavirus/country/viet-nam/',
    'Iraq' : 'https://www.worldometers.info/coronavirus/country/iraq/',
    'Bangladesh' : 'https://www.worldometers.info/coronavirus/country/bangladesh/',
    'Pakistan' : 'https://www.worldometers.info/coronavirus/country/pakistan/',
    'Brazil' : 'https://www.worldometers.info/coronavirus/country/brazil/',
    'Argentina' : 'https://www.worldometers.info/coronavirus/country/argentina/',
    'Colombia' : 'https://www.worldometers.info/coronavirus/country/colombia/',
    'Peru' : 'https://www.worldometers.info/coronavirus/country/peru/',
    'Chile' : 'https://www.worldometers.info/coronavirus/country/chile/',
    'Bolivia' : 'https://www.worldometers.info/coronavirus/country/bolivia/',
    'Uruguay' : 'https://www.worldometers.info/coronavirus/country/uruguay/',
    'Paraguay' : 'https://www.worldometers.info/coronavirus/country/paraguay/',
    'Venezuela' : 'https://www.worldometers.info/coronavirus/country/venezuela/',
    'South Africa' : 'https://www.worldometers.info/coronavirus/country/south-africa/',
    'Morocco' : 'https://www.worldometers.info/coronavirus/country/morocco/',
    'Tunisia' : 'https://www.worldometers.info/coronavirus/country/tunisia/',
    'Ethiopia' : 'https://www.worldometers.info/coronavirus/country/ethiopia/',
    'Libya' : 'https://www.worldometers.info/coronavirus/country/libya/',
    'Egypt' : 'https://www.worldometers.info/coronavirus/country/egypt/',
    'Kenya' : 'https://www.worldometers.info/coronavirus/country/kenya/',
    'Zambia' : 'https://www.worldometers.info/coronavirus/country/zambia/',
    'Algeria' : 'https://www.worldometers.info/coronavirus/country/algeria/',
    'Botswana' : 'https://www.worldometers.info/coronavirus/country/botswana/',
    'Nigeria' : 'https://www.worldometers.info/coronavirus/country/nigeria/',
    'Zimbabwe' : 'https://www.worldometers.info/coronavirus/country/zimbabwe/',
    'Australia' : 'https://www.worldometers.info/coronavirus/country/australia/',
    'Fiji' : 'https://www.worldometers.info/coronavirus/country/fiji/',
    'Papua New Guinea' : 'https://www.worldometers.info/coronavirus/country/papua-new-guinea/',
    'New Caledonia' : 'https://www.worldometers.info/coronavirus/country/new-caledonia/',
    'New Zealand' : 'https://www.worldometers.info/coronavirus/country/new-zealand/'
}

if not os.path.isdir('Pages'):
    os.mkdir('Pages')

#downloading main web page
world_url = 'https://www.worldometers.info/coronavirus/'
r = requests.get(world_url)
f = open("Pages/World.html","w")
f.write(r.text)
f.close()

#downloading country html pages
for country,url in country_list.items():
    r = requests.get(url)
    file_path = 'Pages/' + country + '.html'
    f = open(file_path,'w')
    f.write(r.text)
    f.close()
#Make tokens

#country list provided
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

#YESTERDAY token to start with
def t_YESTERDAY(t):
    r'<table\sid="main_table_countries_yesterday"\sclass="table\stable-bordered\stable-hover\smain_table_countries"\sstyle="width:100%;margin-top:\s0px\s!important;display:none;">'
    return t
#Head Start token
def t_HEADSTART(t):
    r'<thead>'
    return t
#Head End token
def t_HEADEND(t):
    r'</thead>'
    return t
#Row start token
def t_ROWSTART(t):
    r'<tr[^>]*>'
    return t
#Row End token
def t_ROWEND(t):
    r'</tr>'
    return t
#Table header token
def t_TABLEHEADERSTART(t):
    r'<th[^>]*>'
    return t
#Table header end token
def t_TABLEHEADEREND(t):
    r'</th>'
    return t
#Body header start token
def t_BODYSTART(t):
    r'<tbody>'
    return t
#Body header end token
def t_BODYEND(t):
    r'</tbody>'
    return t
#Open table data token
def t_OPENTD(t):
    r'<td[^>]*>'
    return t
#close table data token
def t_CLOSETD(t):
    r'</td>'
    return t
#Breakline token
def t_BREAKLINES(t):
    r'<br\s/>'
    return t

def t_NOBRSTART(t):
    r'<nobr>'
    return t
def t_NOBREND(t):
    r'</nobr>'
    return t
def t_NBSP(t):
    r'&nbsp;'
    return t
#Close href token
def t_CLOSEHREF(t):
    r'</a>'
    return t
#Open href token
def t_OPENHREF(t):
    r'<a[^>]*>'
    return t

#Tokens to extract date-wise data from the country webpage 
def t_ACTIVECASESTITLE(t):
    r'text:\s\'Active\sCases\''
    return t
def t_SUBTITLE(t):
    r'subtitle[^}]*}'
    return t
def t_XAXIS(t):
    r'xAxis[^\[]*\['
    return t
def t_YAXIS(t):
    r'yAxis[^,]*,'
    return t
def t_LEGEND(t):
    r'legend[^}]*}'
    return t
def t_CREDITS(t):
    r'credits[^}]*}'
    return t
def t_SERIES(t):
    r'series:\s\[{[^\[]*\['
    return t
def t_RESPONSIVE(t):
    r'responsive[^;]*;'
    return t
def t_DAILYDEATHTITLE(t):
    r'text:\s\'Daily\sDeaths\''
    return t
def t_PLOTOPTION(t):
    r'plotOptions[^}]*}'
    return t
def t_SPLINE(t):
    r'spline[^}]*}'
    return t
def t_SHOWINLEGEND(t):
    r'showInLegend[^}]*}'
    return t
def t_NEWRECOVEREDTITLE(t):
    r'text:\s\'New\sCases\svs.\sNew\sRecoveries\''
    return t
def t_NAMESKIP(t):
    r'name[^\[]*\['
    return t
def t_NEWCASESTITLE(t):
    r'text:\s\'Daily\sNew\sCases\''
    return t

#Token for name and number
def t_NAME(t):
    r'[A-Za-z0-9+/.]+'
    return t

def t_error(t):
    t.lexer.skip(1)

t_ignore = " \t"

#token list
tokens = [
    'YESTERDAY',
    'HEADSTART',
    'HEADEND',
    'BODYSTART',
    'BODYEND',
    'OPENTD',
    'CLOSETD',
    'ROWSTART',
    'ROWEND',
    'NAME',
    'TABLEHEADERSTART',
    'TABLEHEADEREND',
    'BREAKLINES',
    'NOBRSTART',
    'NOBREND',
    'NBSP',
    'OPENHREF',
    'CLOSEHREF',
    'ACTIVECASESTITLE',
    'SUBTITLE',
    'XAXIS',
    'YAXIS',
    'LEGEND',
    'CREDITS',
    'SERIES',
    'RESPONSIVE',
    'DAILYDEATHTITLE',
    'PLOTOPTION',
    'SPLINE',
    'SHOWINLEGEND',
    'NEWRECOVEREDTITLE',
    'NAMESKIP',
    'NEWCASESTITLE'
]

#GRAMMAR production rules to extract data from main web page

def p_start1(t):
    'start1 : YESTERDAY head1 BODYSTART data1 BODYEND'

def p_head1(p):
    'head1 : HEADSTART row1 HEADEND'

def p_row(p):
    '''row1 : ROWSTART rowdata rowdata rowdata rowdata rowdata rowdata rowdata rowdata rowdata rowdata rowdata rowdata rowdata rowdata rowdata rowdata rowdata rowdata rowdata rowdata rowdata rowdata ROWEND'''

def p_name(p):
    '''name : NAME
            | NAME name'''
    
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + ' ' + p[2]

def p_rowdata(p):
    '''rowdata : TABLEHEADERSTART name TABLEHEADEREND
               | TABLEHEADERSTART TABLEHEADEREND
               | TABLEHEADERSTART name BREAKLINES name TABLEHEADEREND
               | TABLEHEADERSTART name NBSP name BREAKLINES name TABLEHEADEREND
               | TABLEHEADERSTART name BREAKLINES nobr TABLEHEADEREND'''

def p_nobr(p):
    '''nobr : NOBRSTART name NOBREND
            | NOBRSTART NOBREND'''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = None

def p_data(p):
    '''data1 : ROWSTART tabledata tabledata tabledata tabledata tabledata tabledata tabledata tabledata tabledata tabledata tabledata tabledata tabledata tabledata tabledata tabledata tabledata tabledata tabledata tabledata tabledata tabledata ROWEND
            | ROWSTART tabledata tabledata tabledata tabledata tabledata tabledata tabledata tabledata tabledata tabledata tabledata tabledata tabledata tabledata tabledata tabledata tabledata tabledata tabledata tabledata tabledata tabledata ROWEND data1'''
    global Covid_data
    Covid_data[p[3]] = {}
    Covid_data[p[3]]['Total Cases'] = convert_string_to_number(p[4])
    Covid_data[p[3]]['New Cases'] = convert_string_to_number(p[5])
    Covid_data[p[3]]['Total Deaths'] = convert_string_to_number(p[6])
    Covid_data[p[3]]['New Deaths'] = convert_string_to_number(p[7])
    Covid_data[p[3]]['Total Recovered'] = convert_string_to_number(p[8])
    Covid_data[p[3]]['New Recovered'] = convert_string_to_number(p[9])
    Covid_data[p[3]]['Active Cases'] = convert_string_to_number(p[10])
    Covid_data[p[3]]['Serious Critical'] = convert_string_to_number(p[11])
    Covid_data[p[3]]['Total Cases/Mil pop'] = convert_string_to_number(p[12])
    Covid_data[p[3]]['Death Cases/Mil pop'] = convert_string_to_number(p[13])
    Covid_data[p[3]]['Total Tests'] = convert_string_to_number(p[14])
    Covid_data[p[3]]['Tests/Mil pop'] = convert_string_to_number(p[15])


def p_tabledata(p):
    '''tabledata : OPENTD CLOSETD
                 | OPENTD nobr CLOSETD
                 | OPENTD name CLOSETD
                 | OPENTD OPENHREF name CLOSEHREF CLOSETD
    '''
    if len(p) == 3:
        p[0] = None
    elif len(p) == 6:
        p[0] = p[3]
    else:
        p[0] = p[2]

#GRAMMAR rule to extract date-wise data from the country pages.

def p_start2(p):
    '''start2 : activecases
              | dailydeaths
              | newrecoveries
              | newcases'''
def p_activecases(p):
    'activecases : ACTIVECASESTITLE SUBTITLE XAXIS acdates YAXIS LEGEND CREDITS SERIES acdata RESPONSIVE'
    global Active_cases
    Active_cases = dict(zip(Active_cases[0],Active_cases[1]))
def p_acdates(p):
    '''acdates : NAME NAME NAME
               | NAME NAME NAME acdates'''
    p[0] = p[1] + ' ' + p[2] + ' ' + p[3]
    global Active_cases
    Active_cases[0].append(p[0])
def p_acdata(p):
    '''acdata : NAME
              | NAME acdata'''
    p[0] = p[1]
    global Active_cases
    Active_cases[1].append(convert_string_to_number(p[0]))
def p_dailydeaths(p):
    'dailydeaths : DAILYDEATHTITLE SUBTITLE XAXIS dddates YAXIS LEGEND CREDITS PLOTOPTION SPLINE SHOWINLEGEND SERIES dddata NAMESKIP'
    global Daily_deaths
    Daily_deaths = dict(zip(Daily_deaths[0],Daily_deaths[1]))
def p_dddates(p):
    '''dddates : NAME NAME NAME
               | NAME NAME NAME dddates'''
    p[0] = p[1] + ' ' + p[2] + ' ' + p[3]
    global Daily_deaths
    Daily_deaths[0].append(p[0])
def p_dddata(p):
    '''dddata : NAME
              | NAME dddata'''
    p[0] = p[1]
    global Daily_deaths
    Daily_deaths[1].append(convert_string_to_number(p[0]))
def p_newrecoveries(p):
    'newrecoveries : NEWRECOVEREDTITLE SUBTITLE XAXIS nrdate YAXIS LEGEND CREDITS SERIES nrdata NAMESKIP'
    global New_Recoveries
    New_Recoveries = dict(zip(New_Recoveries[0],New_Recoveries[1]))
def p_nrdate(p):
    '''nrdate : NAME NAME NAME
              | NAME NAME NAME nrdate'''
    p[0] = p[1] + ' ' + p[2] + ' ' + p[3]
    global New_Recoveries
    New_Recoveries[0].append(p[0])
def p_nrdata(p):
    '''nrdata : NAME
              | NAME nrdata'''
    p[0] = p[1]
    global New_Recoveries
    New_Recoveries[1].append(convert_string_to_number(p[0]))
def p_newcases(p):
    'newcases : NEWCASESTITLE SUBTITLE XAXIS ncdate YAXIS LEGEND CREDITS PLOTOPTION SPLINE SHOWINLEGEND SERIES ncdata NAMESKIP'
    global New_Cases
    New_Cases = dict(zip(New_Cases[0],New_Cases[1]))
def p_ncdate(p):
    '''ncdate : NAME NAME NAME
              | NAME NAME NAME ncdate'''
    p[0] = p[1] + ' ' + p[2] + ' ' + p[3]
    global New_Cases
    New_Cases[0].append(p[0])
def p_ncdata(p):
    '''ncdata : NAME
              | NAME ncdata'''
    p[0] = p[1]
    global New_Cases
    New_Cases[1].append(convert_string_to_number(p[0]))

def p_error(t):
    pass

#Load the first HTML page from the file
f = open('Pages/World.html')
text = f.read()

#Tokenize the text
import ply.lex as lex
lexer = lex.lex()
lexer.input(text)

#Parsing the Front WebPage
import ply.yacc as yaac
parser = yaac.yacc(start = 'start1')
parser.parse(text)

#close the file
f.close()

#parsing given country datewise data
date_wise_data = {
    'France' : 'https://www.worldometers.info/coronavirus/country/france/',
    'UK' : 'https://www.worldometers.info/coronavirus/country/uk/',
    'Russia' : 'https://www.worldometers.info/coronavirus/country/russia/',
    'Italy' : 'https://www.worldometers.info/coronavirus/country/italy/',
    'Germany' : 'https://www.worldometers.info/coronavirus/country/germany/',
    'Spain': 'https://www.worldometers.info/coronavirus/country/spain/',
    'Poland': 'https://www.worldometers.info/coronavirus/country/poland/',
    'Netherlands' : 'https://www.worldometers.info/coronavirus/country/netherlands/',
    'Ukraine' : 'https://www.worldometers.info/coronavirus/country/ukraine/',
    'Belgium' : 'https://www.worldometers.info/coronavirus/country/belgium/',
    'USA' : 'https://www.worldometers.info/coronavirus/country/us/',
    'Mexico' : 'https://www.worldometers.info/coronavirus/country/mexico/',
    'Canada' : 'https://www.worldometers.info/coronavirus/country/canada/',
    'Cuba' : 'https://www.worldometers.info/coronavirus/country/cuba/',
    'Costa Rica' : 'https://www.worldometers.info/coronavirus/country/costa-rica/',
    'Panama' : 'https://www.worldometers.info/coronavirus/country/panama/',
    'India' : 'https://www.worldometers.info/coronavirus/country/india/',
    'Turkey' : 'https://www.worldometers.info/coronavirus/country/turkey/',
    'Iran' : 'https://www.worldometers.info/coronavirus/country/iran/',
    'Indonesia' : 'https://www.worldometers.info/coronavirus/country/indonesia/',
    'Philippines' : 'https://www.worldometers.info/coronavirus/country/philippines/',
    'Japan' : 'https://www.worldometers.info/coronavirus/country/japan/',
    'Israel' : 'https://www.worldometers.info/coronavirus/country/israel/',
    'Malaysia' : 'https://www.worldometers.info/coronavirus/country/malaysia/',
    'Thailand' : 'https://www.worldometers.info/coronavirus/country/thailand/',
    'Vietnam' : 'https://www.worldometers.info/coronavirus/country/viet-nam/',
    'Iraq' : 'https://www.worldometers.info/coronavirus/country/iraq/',
    'Bangladesh' : 'https://www.worldometers.info/coronavirus/country/bangladesh/',
    'Pakistan' : 'https://www.worldometers.info/coronavirus/country/pakistan/',
    'Brazil' : 'https://www.worldometers.info/coronavirus/country/brazil/',
    'Argentina' : 'https://www.worldometers.info/coronavirus/country/argentina/',
    'Colombia' : 'https://www.worldometers.info/coronavirus/country/colombia/',
    'Peru' : 'https://www.worldometers.info/coronavirus/country/peru/',
    'Chile' : 'https://www.worldometers.info/coronavirus/country/chile/',
    'Bolivia' : 'https://www.worldometers.info/coronavirus/country/bolivia/',
    'Uruguay' : 'https://www.worldometers.info/coronavirus/country/uruguay/',
    'Paraguay' : 'https://www.worldometers.info/coronavirus/country/paraguay/',
    'Venezuela' : 'https://www.worldometers.info/coronavirus/country/venezuela/',
    'South Africa' : 'https://www.worldometers.info/coronavirus/country/south-africa/',
    'Morocco' : 'https://www.worldometers.info/coronavirus/country/morocco/',
    'Tunisia' : 'https://www.worldometers.info/coronavirus/country/tunisia/',
    'Ethiopia' : 'https://www.worldometers.info/coronavirus/country/ethiopia/',
    'Libya' : 'https://www.worldometers.info/coronavirus/country/libya/',
    'Egypt' : 'https://www.worldometers.info/coronavirus/country/egypt/',
    'Kenya' : 'https://www.worldometers.info/coronavirus/country/kenya/',
    'Zambia' : 'https://www.worldometers.info/coronavirus/country/zambia/',
    'Algeria' : 'https://www.worldometers.info/coronavirus/country/algeria/',
    'Botswana' : 'https://www.worldometers.info/coronavirus/country/botswana/',
    'Nigeria' : 'https://www.worldometers.info/coronavirus/country/nigeria/',
    'Zimbabwe' : 'https://www.worldometers.info/coronavirus/country/zimbabwe/',
    'Australia' : 'https://www.worldometers.info/coronavirus/country/australia/',
    'Fiji' : 'https://www.worldometers.info/coronavirus/country/fiji/',
    'Papua New Guinea' : 'https://www.worldometers.info/coronavirus/country/papua-new-guinea/',
    'New Caledonia' : 'https://www.worldometers.info/coronavirus/country/new-caledonia/',
    'New Zealand' : 'https://www.worldometers.info/coronavirus/country/new-zealand/'
}
for country_name in country_list:
    Active_cases = [[],[]]
    Daily_deaths = [[],[]]
    New_Recoveries = [[],[]]
    New_Cases = [[],[]]
    
    #Load the country file
    file_path = 'Pages/' + country_name + '.html'
    f = open(file_path,'r')
    text = f.read()

    #lexer for country Page
    lexerr = lex.lex()
    lexerr.input(text)

    #parsing country Page to extract data
    pareserr = yaac.yacc(start='start2')
    pareserr.parse(text,lexer=lexerr)

    date_wise_data[country_name] = {}
    date_wise_data[country_name]['Active Cases'] = Active_cases.copy()
    date_wise_data[country_name]['Daily Deaths'] = Daily_deaths.copy()
    date_wise_data[country_name]['New Recoveries'] = New_Recoveries.copy()
    date_wise_data[country_name]['New Cases'] = New_Cases.copy()

    #close the file
    f.close()
    

# Import the required libraries

#%%