import re
import random
import urllib
import urllib2 as urllib
import urlparse
import json
from datetime import datetime
from PIL import Image
from cStringIO import StringIO

VERSION_NO = '2.2018.09.08.1'

def any(s):
    for v in s:
        if v:
            return True
    return False

def Start():
    #HTTP.ClearCache()
    HTTP.CacheTime = CACHE_1WEEK
    HTTP.Headers['User-agent'] = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.2; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)'
    HTTP.Headers['Accept-Encoding'] = 'gzip'

def capitalize(line):
    return ' '.join([s[0].upper() + s[1:] for s in line.split(' ')])

def tagAleadyExists(tag,metadata):
    for t in metadata.genres:
        if t.lower() == tag.lower():
            return True
    return False

def posterAlreadyExists(posterUrl,metadata):
    for p in metadata.posters.keys():
        Log(p.lower())
        if p.lower() == posterUrl.lower():
            Log("Found " + posterUrl + " in posters collection")
            return True

    for p in metadata.art.keys():
        if p.lower() == posterUrl.lower():
            return True
    return False

class Data18PhoenixAgent(Agent.Movies):
    name = 'Data18-Phoenix'
    languages = [Locale.Language.English]
    accepts_from = ['com.plexapp.agents.localmedia']
    primary_provider = True

    def search(self, results, media, lang):
        
        title = media.name
        if media.primary_metadata is not None:
            title = media.primary_metadata.title

        Log('*******MEDIA TITLE****** ' + str(title))

        # Search for year
        year = media.year
        if media.primary_metadata is not None:
            year = media.primary_metadata.year
            
        encodedTitle = urllib.quote(title)
        Log(encodedTitle)
        searchResults = HTML.ElementFromURL('https://data18.empirestores.co/Search?q=' + encodedTitle)
        isSingleMatch = False
        try:
            singleMatch = searchResults.xpath('//meta[@http-equiv="refresh"]')
            if len(singleMatch) > 0:
                isSingleMatch = True
                Log("Search yields single result & redirects")
        except:
            pass
        if isSingleMatch:
            singleMatchURL = singleMatch[0].get("content")[7:]
            url = 'https://data18.empirestores.co/' + singleMatchURL
            detailsPageElements = HTML.ElementFromURL(url)
            titleNoFormatting = detailsPageElements.xpath('//h1[@class="hidden-md hidden-lg hidden-xl"]')[0].text_content()[6:-11]
            curID = singleMatchURL
            curID = curID.replace('/','_')

            releasedDate = detailsPageElements.xpath('//ul[@class="list-unstyled product-details spacing-bottom"]//li')[1].text_content()[18:30]
            Log(str(curID))
            lowerResultTitle = str(titleNoFormatting).lower()
            score = 100 - Util.LevenshteinDistance(title.lower(), titleNoFormatting.lower()) - Util.LevenshteinDistance(year, releasedDate[6:])
            titleNoFormatting = titleNoFormatting + " [" + releasedDate + "]"
            results.Append(MetadataSearchResult(id = curID, name = titleNoFormatting, score = score, lang = lang))
        else:
            for searchResult in searchResults.xpath('//div[@class=" col-xs-6 col-sm-4 col-md-3 grid-item"]//a'):

                Log(searchResult.text_content())
                titleNoFormatting = searchResult.get("data-original-title")
                curID = searchResult.get("href")
                curID = curID.replace('/','_')
                popOverID = searchResult.get("data-target")
                popOver = searchResults.xpath('//div[@id="'+ popOverID +'"]')[0]
                popOverContents = popOver.text_content()
                releasedPos = popOverContents.find("Released")
                releasedDate = popOverContents[releasedPos+9:releasedPos+19]
                runtimePos = popOverContents.find("Runtime")
                runtimePosEnd = popOverContents.find(" mins.")
                runtimeAmount = popOverContents[runtimePos+7:runtimePosEnd]    
                Log(str(curID))
                lowerResultTitle = str(titleNoFormatting).lower()
                score = 100 - Util.LevenshteinDistance(title.lower(), titleNoFormatting.lower()) - Util.LevenshteinDistance(year, releasedDate[6:])
                titleNoFormatting = titleNoFormatting + " [" + releasedDate + ", " + runtimeAmount + " mins]"
                results.Append(MetadataSearchResult(id = curID, name = titleNoFormatting, score = score, lang = lang))
                    
        results.Sort('score', descending=True)            

    def update(self, metadata, media, lang):

        Log('******UPDATE CALLED*******')
        
        temp = str(metadata.id).replace('_','/')
        url = 'https://data18.empirestores.co/' + temp
        detailsPageElements = HTML.ElementFromURL(url)

        # Summary
        paragraph = detailsPageElements.xpath('//div[@class="spacing-bottom"]')
        paragraph = paragraph[len(paragraph)-1].text_content()
        paragraph = paragraph.replace('&13;', '').strip(' \t\n\r"').replace('\n','').replace('  ','') + "\n\n"
        metadata.summary = paragraph
        metadata.title = detailsPageElements.xpath('//h1[@class="hidden-md hidden-lg hidden-xl"]')[0].text_content()[6:-11]
        metadata.studio = detailsPageElements.xpath('//ul[@class="list-unstyled product-details spacing-bottom"]//li')[0].text_content()[25:]
        date = detailsPageElements.xpath('//ul[@class="list-unstyled product-details spacing-bottom"]//li')[1].text_content()[18:30]
        date_object = datetime.strptime(date, '%b %d, %Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year    
            

        detailsSections = detailsPageElements.xpath('//ul[@class="list-unstyled product-details spacing-bottom"]//li')

        # Genres
        metadata.genres.clear()
        
        for selectedSection in detailsSections:
            if "Categories" in selectedSection.text_content():
                genres = selectedSection.xpath('.//a')
        if len(genres) > 0:
            for genreLink in genres:
                genreName = genreLink.text_content().strip('\n').lower()
                metadata.genres.add(capitalize(genreName))

        # Actors
        metadata.roles.clear()
        for selectedSection in detailsSections:
            if "Performers" in selectedSection.text_content():
                actors = selectedSection.xpath('.//a')
        if len(actors) > 0:
            for actorLink in actors:
                role = metadata.roles.new()
                actorName = actorLink.text_content().strip('\n')[9:]
                role.name = actorName
                actorPage = actorLink.get("href")
                actorPageReduced = actorPage[:-len(actorName)-5-11]
                actorPageParts = actorPageReduced.split("/")
                actorID = actorPageParts[len(actorPageParts)-1]
                role.photo = "https://imgs1cdn.adultempire.com/actors/" + actorID + ".jpg"

        # Posters/Background
        posterURL = detailsPageElements.xpath('//div[@id="Boxcover"]//a//img')[0].get("src")
        try:
            background = detailsPageElements.xpath('//div[@id="previewContainer"]')[0].get("style")[21:-2]
            metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
            Log("BackgroundURL: " + background)
        except: 
            pass
        Log("PosterURL: " + posterURL)
        
        
        metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
                
