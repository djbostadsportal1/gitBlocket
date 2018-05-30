# -*- coding: utf-8 -*-
"""
Created 17-01-2018
Last-edit: 09-04-2018
@author: Dennis
"""

import scrapy
import scrapy_splash
import sys
import time
import re
import Blocket_module as bm

class BlocketAlvsborg(scrapy.Spider):

    #Name of scraper
    name = 'BlocketAlvsborg'

    #Start page you start scraping from
    start_urls = ['https://www.blocket.se/bostad/uthyres/lagenheter/alvsborg']

    #The domain you are allowed to scrape on
    allowed_domains = ['https://www.blocket.se/bostad/']

    #Scraping the first page
    def parse(self, response):
        AdType = 'RENTAL'
        counter = 0

        # Wrapping all the content i want to scrape
        ads = response.xpath(bm.Xp_Wrapper)

        # Starts scraping and yielding to meta
        for ad in ads:
            PropertyType = ad.xpath(bm.Xp_PropertyType).re_first(bm.Reg_PropertyType)
            response.meta[bm.fieldname_Title] = bm.NoneToString(ad.xpath(bm.Xp_Title).re_first(bm.Reg_Title))
            response.meta[bm.fieldname_Rooms] = bm.NoneToString(ad.xpath(bm.Xp_Rooms).re_first(bm.Reg_Rooms))
            response.meta[bm.fieldname_LivingSpace] = bm.NoneToString(ad.xpath(bm.Xp_LivingSpace).re_first(bm.Reg_LivingSpace))
            absolute_url = ad.xpath(bm.Xp_absolute_url).re_first(bm.Reg_absolute_url)
            counter = counter + 1
            TitleInfo = ad.xpath(bm.Xp_TitleInfo).re_first(bm.Reg_TitleInfo)
            response.meta['AdType'] = AdType
            response.meta[bm.fieldname_ExternalReference] = bm.NoneToString(absolute_url)
            response.meta['counter'] = counter

            # Tjekker om det kun er for studerende boligen er for.
            response.meta[bm.fieldname_StudentsOnly] = bm.student(TitleInfo)

            # Starter med at tjekke om titlen indeholder info om propertytype
            response.meta[bm.fieldname_PropertyType] = bm.propertyType(TitleInfo, PropertyType)
            response.meta['PropertTypeInfo'] = ad.xpath(bm.Xp_PropertyType).re_first(bm.Reg_PropertyType)
            response.meta['TitleInfo'] = TitleInfo


            # The rent is sometimes monthly and sometimes weekly but only gets the data from monthly on purpose
            response.meta[bm.fieldname_Rent] = bm.NoneToString(ad.xpath(bm.Xp_Rent).re_first(bm.Reg_Rent))

            yield scrapy.Request(absolute_url, callback=self.parse_details, meta=response.meta, dont_filter=True)

        # Next page button:
        absolute_next_url = response.xpath(bm.Xp_absolute_url_next_page).re_first(bm.Reg_absolute_url_next_page)
        yield scrapy.Request(absolute_next_url, callback=self.parse, dont_filter=True)

    #Scraping the link from each add, where you read more about the specific appartment (Detail Page)
    def parse_details(self, response):
        Description = " ".join(response.xpath(bm.Xp_Description).re(bm.Reg_Description))
        StreetName = response.xpath(bm.Xp_StreetName).re_first(bm.Reg_StreetName)
        StreetNumber = response.xpath(bm.Xp_StreetNumber).re_first(bm.Reg_StreetNumber)
        Name = response.xpath(bm.Xp_Name).re_first(bm.Reg_Name)
        Municipality = response.xpath(bm.Xp_Municipality).re_first(bm.Reg_Municipality)
        Addinfo = " ".join(response.xpath(bm.Xp_Addinfo).re(bm.Reg_Addinfo))

        #Extracts Picutres from blocket if you want.
        if bm.get_Images == 1:
            response.meta[bm.fieldname_Images] = "|".join(response.xpath(bm.Xp_Images).re(bm.Reg_Images))


        # Collects the total info to search for RentalPeriod Furnishing.
        RentalInfo = bm.collectTotalInfo(Description, Addinfo)

        # Bruger funktioner til at finde rentalPeriod
        response.meta[bm.fieldname_RentalPeriod] = bm.rentalPeriodSearch(RentalInfo)
        response.meta[bm.fieldname_RentalPeriodFrom] = bm.rentalPeriodFromSearch(RentalInfo)

        # Checks if there is Furnishing with the apartment.
        response.meta[bm.fieldname_Furnishing] = bm.furnishing(RentalInfo)

        # Replacing the adress in all descriptions with "Adress".
        response.meta[bm.fieldname_Description] = bm.replaceStreetNameInDescription(StreetName, Description, StreetNumber)

        response.meta[bm.fieldname_StreetName] = bm.NoneToString(StreetName)
        response.meta[bm.fieldname_StreetNumber] = bm.NoneToString(StreetNumber)
        response.meta[bm.fieldname_Name] = bm.NoneToString(Name)
        response.meta[bm.fieldname_Municipality] = bm.NoneToString(Municipality)

        yield response.meta
