# -*- coding: utf-8 -*-
"""
Created 17-01-2018
Last-edit: 25-04-2018
@author: Dennis
"""

import re


"""
This script is only for spiders meant for blocket.
We define all the xpaths here in this script to be general for all blocket spiders, fieldnames, regex expression and
also the functions. So if you edit this script you will affect all blocket spiders.
"""

# Wrapper xpath
Xp_Wrapper = '//div[@id="item_list"]/div'



# Fields scraped on first page with xpath and regex
fieldname_Title = 'Title'
Xp_Title = './/h4[@class="media-heading"]/a/text()'
Reg_Title = '[\w\s]+'

fieldname_Rooms = 'Rooms'
Xp_Rooms = './/span[contains(@class,"rooms")]/text()'
Reg_Rooms = '\d*'

fieldname_LivingSpace = 'LivingSpace'
Xp_LivingSpace = './/span[contains(@class,"size")]/text()'
Reg_LivingSpace = '\d*'

fieldname_ExternalReference = 'ExternalReference'
Xp_absolute_url = './/a[contains(@class,"vi-link-overlay")]/@href'
Reg_absolute_url = '.*'

fieldname_Rent = 'Rent'
Xp_Rent = './/span[contains(@class,"monthly_rent")]/text()'
Reg_Rent = '[\d+\s]+'

# Variables scraped for putting inside functions to get a field name
# Titleinfo is used inside propertytype and studentsonly.
Xp_TitleInfo = './/div[contains(@class,"media-body")]/a/@title'
Reg_TitleInfo = '.*'


# PropertyType is used inside propertytype function to determine the field value of propertytype.
fieldname_PropertyType = 'PropertyType'
Xp_PropertyType = './/span[@class="subject-param category"]/text()'
Reg_PropertyType = '\w+'

# Next page xpath
Xp_absolute_url_next_page = '//li[@class="next"]/a[not(@class and @class="disabled")]/@href'
Reg_absolute_url_next_page = '.*'


# Second page xpaths without wrapper
fieldname_Description = 'Description'
Xp_Description = '//p[@class="object-text"]/text()'
Reg_Description = '.*'

fieldname_StreetName = 'StreetName'
Xp_StreetName = '//div[contains(@class,"row")][2]//h3[@class="h5"]/text()'
Reg_StreetName = '[\D\s]+'

fieldname_StreetNumber = 'StreetNumber'
Xp_StreetNumber = '//div[contains(@class,"row")][2]//h3[@class="h5"]/text()'
Reg_StreetNumber = '\d+\s?\w?'

fieldname_Name = 'Name'
Xp_Name = '//div[@id="secondary-content"]//h2[@class="h4"]/text()'
Reg_Name = '.*'

fieldname_Municipality = 'Municipality'
Xp_Municipality = '//span[@class="subject-param address separator"]/text()'
Reg_Municipality = '\w+'

Xp_Addinfo = '//div[@class="col-xs-8 body"]//div[@class="params-extra"]/div/span/text()'
Reg_Addinfo = '.*'

#Images that you can active or deactivate if you write a hashtag, it does not scrape it. If you write nothing it will be
#scraped.
get_Images = 0
fieldname_Images = 'Images'
Xp_Images = '//div[@class="carousel-inner"]/div/img/@src'
Reg_Images = '.*'

#Fieldnames not connected to a specific xpath but instead some of the functions.
fieldname_StudentsOnly = 'StudentsOnly'
fieldname_RentalPeriod = 'RentalPeriod'
fieldname_RentalPeriodFrom = 'RentalPeriodFrom'
fieldname_Furnishing = 'Furnishing'


# Lists for further fields to scrape
list_Fields = ['FieldOne', 'FieldTwo', 'FieldThree']
list_Xpaths = ['XpathOne', 'XpathTwo', 'XpathThree']
list_Extraction_method = ['ExtractOne', 'ExtractTwo', 'ExtractThree']


def student(TitleInfo):
    if 'stud' in TitleInfo.lower():
        StudentsOnly = 'TRUE'
    else:
        StudentsOnly = 'FALSE'

    return StudentsOnly

def propertyType(TitleInfo, PropertyType):
    if 'rum uthyres' in TitleInfo.lower():
        PropertyType = 'ROOM'
    elif 'delat boende' in TitleInfo.lower():
        PropertyType = 'ROOM'
    elif 'inneboende' in TitleInfo.lower():
        PropertyType = 'ROOM'
    elif 'lägenhet' in TitleInfo.lower():
        PropertyType = 'APARTMENT'
    elif 'villa' in TitleInfo.lower():
        PropertyType = 'HOUSE'
    elif 'radhus' in TitleInfo.lower():
        PropertyType = 'HOUSE'
    elif 'parhus' in TitleInfo.lower():
        PropertyType = 'HOUSE'
    elif 'tomt' in TitleInfo.lower():
        PropertyType = 'LOT'
    elif 'fritidsboende' in TitleInfo.lower():
        PropertyType = 'CABIN'
    else:
        if 'lägenhet' in PropertyType.lower():
            PropertyType = 'APARTMENT'
        elif 'villa' in PropertyType.lower():
            PropertyType = 'HOUSE'
        elif 'radhus' in PropertyType.lower():
            PropertyType = 'HOUSE'
        elif 'parhus' in PropertyType.lower():
            PropertyType = 'HOUSE'
        elif 'tomt' in PropertyType.lower():
            PropertyType = 'LOT'
        elif 'fritidsboende' in PropertyType.lower():
            PropertyType = 'CABIN'
        else:
            PropertyType = ''

    return PropertyType

#Leder efter RentalPeriod
def rentalPeriodSearch(RentalInfo):
    if 'uthyres korttid' in RentalInfo.lower():
        RentalPeriod = 'LESS_THAN_ONE_YEAR'
    elif 'tillsvidare' in RentalInfo.lower():
        RentalPeriod = 'UNLIMITED'
    elif 'förstahand' in RentalInfo.lower():
        RentalPeriod = 'UNLIMITED'
    elif 'och framåt' in RentalInfo.lower():
        RentalPeriod = 'UNLIMITED'
    elif '1a handskontrakt' in RentalInfo.lower():
        RentalPeriod = 'UNLIMITED'
    elif 'andrahand' in RentalInfo.lower():
        RentalPeriod = 'ONE_TO_TWO_YEARS'
    elif 'andra hand' in RentalInfo.lower():
        RentalPeriod = 'ONE_TO_TWO_YEARS'
    elif 'andrahandskontrakt' in RentalInfo.lower():
        RentalPeriod = 'ONE_TO_TWO_YEARS'
    elif 'termin' in RentalInfo.lower():
        RentalPeriod = 'LESS_THAN_ONE_YEAR'
    elif 'prövetid' in RentalInfo.lower():
        RentalPeriod = 'LESS_THAN_ONE_YEAR'
    elif 'korttidsuthyrning' in RentalInfo.lower():
        RentalPeriod = 'LESS_THAN_ONE_YEAR'
    elif 'period' in RentalInfo.lower():
        RentalPeriod = 'LESS_THAN_ONE_YEAR'
    else:
        RentalPeriod = ''

    return RentalPeriod

#Leder efter RentalPeriodFrom
def rentalPeriodFromSearch(RentalInfo):
    if re.search('\d+-\d+-\d+', RentalInfo.lower()) is not None:
        m = re.search('\d+-\d+-\d+', RentalInfo.lower())
        RentalPeriodFrom = m.group(0)
    elif re.search('\d+/\d+/\d+', RentalInfo.lower()) is not None:
        m = re.search('\d+/\d+/\d+', RentalInfo.lower())
        RentalPeriodFrom = m.group(0)
        RentalPeriodFrom = RentalPeriodFrom.replace('/', '-')
    else:
        RentalPeriodFrom = ''

    return RentalPeriodFrom

def collectTotalInfo(Description, Addinfo):
    if Addinfo != None:
        RentalInfo = Description + Addinfo
    else:
        RentalInfo = Description

    return RentalInfo

# Check if there is furnishing.
def furnishing(RentalInfo):
    if 'uthyres möblerad' in RentalInfo.lower():
        Furnishing = 'PROVIDED'
    else:
        Furnishing = ""

    return Furnishing

# Replaces Streetname in Description with Adress.
def replaceStreetNameInDescription(StreetName, Description, StreetNumber):
    if StreetName != None:
        Adress = StreetName + ' ' + str(StreetNumber)
        Replace = '\"Adress\"'
        Description = Description.replace(Adress, Replace)
    else:
        Description = Description

    return Description

# Makes it an empty string if none else returns the original input.
def NoneToString(variable):
    # The backend can't handle option None.
    if variable == None:
        variable = ''
    else:
        variable = variable

    return variable
