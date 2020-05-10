import scrapy

# Spider to crawl and extract resort data
class wyn_spider(scrapy.Spider):
    
    #Enter exact resort at clubwyndham.wyndhamdestinations.com between quotes in start_urls 
    #Ex: https://clubwyndham.wyndhamdestinations.com/us/en/resorts/wyndham-hotels-resorts/united-states-of-america/florida/daytona-beach/worldmark-ocean-walk#room0
    name = 'wyn_spider'
    start_urls = [
        'file:///private/var/folders/rs/scr10b_16_j_lrdktb1xx4340000gn/T/tmpd9upcn7o.html']

    #This pulls resort level information such as name, address, description, and other information added in new update
    #No phone number is present anywhere on the webpage to scrape
    def parse(self, response):

        # Name, Address, and a description/highlight quote
        nameSelector = './/section[@id= "description"]//h1[@class = "title-1 margin-0"]/text()'
        addressSelector = './/section[@id= "description"]//p[@class = "body-1 semibold margin-top-1"]/text()'
        descriptionSelector = './/section[@id= "description"]//div[@class="cell small-11"]/p[3]/text()'
        #phoneSelector = 

        # other information/hints/amenities/and nearby activities
        #Some new information was added here in site update
        #littered with unicode
        resort_infoSelector = './/*[@id="resort-information"]/div/div/section/ul/li/span/text()'
        hintsSelector = './/div[@class="contentSlice section"]/div/div/div[2]/ul/li/text()'
        accessibilitySelector = '//*[@id="accessible-features"]/div/div/section/ul/li/span/text()'
        amenitiesSelector = './/*[@id="amenities"]/div/div/section/ul//li/span/text()'
        activitesSelector = '//*[@id="activities"]/div/div/section/ul//li/span/text()'

        # removes unicode from description: '\xa0'
        phrase = response.xpath(descriptionSelector).get().strip()
        clean_description = phrase.replace('\xa0', ' ')
        
        #returns scraped resort data
        yield {
            'resort_name': response.xpath(nameSelector).get(),
            'address': response.xpath(addressSelector).get(),
            'quote': clean_description,
            'resort_info': response.xpath(resort_infoSelector).getall(),
            'hint': response.xpath(hintsSelector).getall(),
            'accessible-feautres': response.xpath(accessibilitySelector).getall(),
            'resort_amenities': response.xpath(amenitiesSelector).getall(),
            'resort_activies': response.xpath(activitesSelector).getall()
        }

        unit = './/div[contains(@id, "unit-details")]'
        for units in response.xpath(unit):
            room_nameSelector = './/div[@class ="unit-details reveal__content"]/div[1]/section[1]/div/h2/text()'
            sqftSelector = './/div[@class = "grid-x padding-2"]/div[3]/div/div/span/text()'
            kitchenSelector = './/div[@class = "grid-x padding-2"]/div[3]/div/div[2]/span/text()'
            bathsSelector = './/div[@class = "grid-x padding-2"]/div[3]/div/div[3]/span/text()'
            max_guestsSelector = './/div[@class = "grid-x padding-2"]/div[4]/div/div/span/text()'
            bedSelector = './/div[@class = "grid-x padding-2"]/div[4]/div/div[2]/ul[@class="text-black margin-0 no-bullet"]/li/text()'
            room_amenitiesSelector = './/div[@class = "unit-details reveal__content"]//section[@class="unit-details__section padding-2"]/ul//li/text()'

            # gets maximum guests per room as string and puts number into a list
            sleeps = units.xpath(max_guestsSelector).get().strip()
            max_guest = []
            for guest in sleeps.split():
                if guest.isdigit():
                    max_guest.append(int(guest))

            # makes a list with all the room amenities to be used to extract washer/dryer
            room_amenities = units.xpath(room_amenitiesSelector).getall()

            # Pulls Washer/Dryer amenity if available
            washer_amenity = 'Washer'
            washer_dryer = list(
                filter(lambda x: washer_amenity in x, room_amenities))

            # Extracts the washer/dryer room_amenities list
            room_amenities = [
                x for x in room_amenities if not x.startswith('Washer')]

            yield {
                'room_title': units.xpath(room_nameSelector).get().strip(),
                'square_feet': units.xpath(sqftSelector).get().strip(),
                'kitchen': units.xpath(kitchenSelector).get().strip(),
                'num_baths': units.xpath(bathsSelector).get().strip(),
                'max_guests': max_guest,
                'beds': units.xpath(bedSelector).getall(),
                'washer_dryer': washer_dryer,
                'room_amenities': room_amenities,
            }
