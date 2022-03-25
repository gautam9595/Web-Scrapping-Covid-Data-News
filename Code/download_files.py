#%%
import os
import os.path
import requests

#----------------------------saving all the html pages in a folder ''--------------------------
#------------------------------------------------------------------------------------------

#-------------------------URLS of 2020 Feb-Dec, 2021 and 2022 News Pages------------------------
urls = {
    'February2020' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_February_2020',
    'March2020' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_March_2020',
    'April2020' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_April_2020',
    'May2020' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_May_2020',
    'June2020' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_June_2020',
    'July2020' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_July_2020',
    'August2020' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_August_2020',
    'September2020' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_September_2020',
    'October2020' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_October_2020',
    'November2020' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_November_2020',
    'December2020' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_December_2020',
    'January2021' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_January_2021',
    'February2021' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_February_2021',
    'March2021' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_March_2021',
    'April2021' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_April_2021',
    'May2021' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_May_2021',
    'June2021' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_June_2021',
    'July2021' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_July_2021',
    'August2021' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_August_2021',
    'September2021' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_September_2021',
    'October2021' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_October_2021',
    'November2021' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_November_2021',
    'December2021' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_December_2021',
    'January2022' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_January_2022',
    'February2022' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_February_2022',
    'March2022' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_March_2022',
}

#----------------create directory
if not os.path.isdir('News20-22'):
    os.mkdir('News20-22')

#----------------downloading html pages
for country,url in urls.items():
    r = requests.get(url)
    file_path = 'News20-22/' + country + '.html'
    f = open(file_path,'w')
    f.write(r.text)
    f.close()
#-------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------

#-------------------------URLS of 2020 Feb-Dec, 2021 and 2022 response Pages-----------------
urls = {
    'January2020' : 'https://en.wikipedia.org/wiki/Responses_to_the_COVID-19_pandemic_in_January_2020',
    'February2020' : 'https://en.wikipedia.org/wiki/Responses_to_the_COVID-19_pandemic_in_February_2020',
    'March2020' : 'https://en.wikipedia.org/wiki/Responses_to_the_COVID-19_pandemic_in_March_2020',
    'April2020' : 'https://en.wikipedia.org/wiki/Responses_to_the_COVID-19_pandemic_in_April_2020',
    'May2020' : 'https://en.wikipedia.org/wiki/Responses_to_the_COVID-19_pandemic_in_May_2020',
    'June2020' : 'https://en.wikipedia.org/wiki/Responses_to_the_COVID-19_pandemic_in_June_2020',
    'July2020' : 'https://en.wikipedia.org/wiki/Responses_to_the_COVID-19_pandemic_in_July_2020',
    'August2020' : 'https://en.wikipedia.org/wiki/Responses_to_the_COVID-19_pandemic_in_August_2020',
    'September2020' : 'https://en.wikipedia.org/wiki/Responses_to_the_COVID-19_pandemic_in_September_2020',
    'October2020' : 'https://en.wikipedia.org/wiki/Responses_to_the_COVID-19_pandemic_in_October_2020',
    'November2020' : 'https://en.wikipedia.org/wiki/Responses_to_the_COVID-19_pandemic_in_November_2020',
    'December2020' : 'https://en.wikipedia.org/wiki/Responses_to_the_COVID-19_pandemic_in_December_2020',
    'January2021' : 'https://en.wikipedia.org/wiki/Responses_to_the_COVID-19_pandemic_in_January_2021',
    'February2021' : 'https://en.wikipedia.org/wiki/Responses_to_the_COVID-19_pandemic_in_February_2021',
    'March2021' : 'https://en.wikipedia.org/wiki/Responses_to_the_COVID-19_pandemic_in_March_2021',
    'April2021' : 'https://en.wikipedia.org/wiki/Responses_to_the_COVID-19_pandemic_in_April_2021',
    'May2021' : 'https://en.wikipedia.org/wiki/Responses_to_the_COVID-19_pandemic_in_May_2021',
    'June2021' : 'https://en.wikipedia.org/wiki/Responses_to_the_COVID-19_pandemic_in_June_2021',
    'July2021' : 'https://en.wikipedia.org/wiki/Responses_to_the_COVID-19_pandemic_in_July_2021',
    'August2021' : 'https://en.wikipedia.org/wiki/Responses_to_the_COVID-19_pandemic_in_August_2021',
    'September2021' : 'https://en.wikipedia.org/wiki/Responses_to_the_COVID-19_pandemic_in_September_2021',
    'October2021' : 'https://en.wikipedia.org/wiki/Responses_to_the_COVID-19_pandemic_in_October_2021',
    'November2021' : 'https://en.wikipedia.org/wiki/Responses_to_the_COVID-19_pandemic_in_November_2021',
    'December2021' : 'https://en.wikipedia.org/wiki/Responses_to_the_COVID-19_pandemic_in_December_2021',
    'January2022' : 'https://en.wikipedia.org/wiki/Responses_to_the_COVID-19_pandemic_in_January_2022',
    'February2022' : 'https://en.wikipedia.org/wiki/Responses_to_the_COVID-19_pandemic_in_February_2022',
    'March2022' : 'https://en.wikipedia.org/wiki/Responses_to_the_COVID-19_pandemic_in_March_2022'
}

#----------------create directory
if not os.path.isdir('Resp20-22'):
    os.mkdir('Resp20-22')

#----------------downloading html pages
for country,url in urls.items():
    r = requests.get(url)
    file_path = 'Resp20-22/' + country + '.html'
    f = open(file_path,'w')
    f.write(r.text)
    f.close()
#-------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------

#---------------------------------------Extract start Date Part1--------------------------------
urls = {
    'Argentina' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Argentina',
    'Bangladesh' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Bangladesh',
    'Ghana' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Ghana_(March–July_2020)',
    'Ireland' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_the_Republic_of_Ireland_(January%E2%80%93June_2020)',
    'Malaysia' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Malaysia_(2020)',
    'New Zealand' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_New_Zealand_(2020)',
    'Nigeria' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Nigeria_(February–June_2020)',
    'Philippines' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_the_Philippines_(2020)',
    'Singapore' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Singapore_(2020)',
    'South Africa' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_South_Africa',
    'England' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_England_(January%E2%80%93June_2020)'
}

#----------------create directory
if not os.path.isdir('StartDateRange1'):
    os.mkdir('StartDateRange1')

#----------------downloading html pages
for country,url in urls.items():
    r = requests.get(url)
    file_path = 'StartDateRange1/' + country + '.html'
    f = open(file_path,'w')
    f.write(r.text)
    f.close()
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------

#---------------------------------------Extract start Date Part2--------------------------------
urls = {
    'Australia' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Australia_(2020)',
    'Brazil' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Brazil',
    'India' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_India_(January–May_2020)',
    'Indonesia' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Indonesia_(2020)',
    'Mexico' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Mexico',
    'Pakistan' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Pakistan',
    'Spain' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Spain',
    'Turkey' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Turkey'
}

#----------------create directory
if not os.path.isdir('StartDateRange2'):
    os.mkdir('StartDateRange2')

#----------------downloading html pages
for country,url in urls.items():
    r = requests.get(url)
    file_path = 'StartDateRange2/' + country + '.html'
    f = open(file_path,'w')
    f.write(r.text)
    f.close()
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------

#---------------------------------------Extract End Date Part1--------------------------------
urls = {
    'Argentina' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Argentina',
    'Bangladesh' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Bangladesh',
    'Ghana' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Ghana_(March–July_2020)',
    'Ireland' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_the_Republic_of_Ireland_(January%E2%80%93June_2020)',
    'Malaysia' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Malaysia_(2020)',
    'New Zealand' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_New_Zealand_(2020)',
    'Nigeria' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Nigeria_(February–June_2020)',
    'Philippines' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_the_Philippines_(2020)',
    'Singapore' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Singapore_(2020)',
    'South Africa' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_South_Africa',
    'England' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_England_(January%E2%80%93June_2020)'
}

#----------------create directory
if not os.path.isdir('EndDateRange1'):
    os.mkdir('EndDateRange1')

#----------------downloading html pages
for country,url in urls.items():
    r = requests.get(url)
    file_path = 'EndDateRange1/' + country + '.html'
    f = open(file_path,'w')
    f.write(r.text)
    f.close()
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------

#---------------------------------------Extract End Date Part2--------------------------------
urls = {
    'Australia' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Australia_(2020)',
    'Brazil' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Brazil',
    'India' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_India_(January–May_2020)',
    'Indonesia' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Indonesia_(2020)',
    'Mexico' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Mexico',
    'Pakistan' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Pakistan',
    'Spain' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Spain',
    'Turkey' : 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Turkey'
}

#----------------create directory
if not os.path.isdir('EndDateRange2'):
    os.mkdir('EndDateRange2')

#----------------downloading html pages
for country,url in urls.items():
    r = requests.get(url)
    file_path = 'EndDateRange2/' + country + '.html'
    f = open(file_path,'w')
    f.write(r.text)
    f.close()
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------

#%%