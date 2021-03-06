import scrapy
import re

# Spider to crawl and extract resort data


class wynSpider(scrapy.Spider):
    name = "wynSpider"
    start_urls = ['https://clubwyndham.wyndhamdestinations.com/us/en/resorts/wyndham-hotels-resorts/united-states-of-america/florida/orlando/club-wyndham-bonnet-creek']

    def parse(self, response):
        # This for loop gets the resort data; name, address, telephone, quote, amenities,
        # and images(not yet implemented)
        header = '//*[@* = "column is-8"]'
        for wyndham in response.xpath(header):

            nameSELECTOR = './/h1[@class = "wyn-headline__title"]/text()'
            addressSELECTOR = './/h2[@class = "wyn-headline__subtitle"]/text()'
            telephoneSELECTOR = './/a[@class = "wyn-resort-phoneNumber"]/text()'
            highlightSELECTOR = './/div[@class = "wyn-js-expand-disabled wyn-expandable-card "]/p/text()'
            resort_amenitiesSELECTOR = './/ul/li/span/span[@class = "wyn-icon__label "]/text()'

            yield {
                'name': wyndham.xpath(nameSELECTOR).get().strip(),
                'address': wyndham.xpath(addressSELECTOR).get().strip(),
                'telephone': wyndham.xpath(telephoneSELECTOR).get().strip(),
                'highlight': wyndham.xpath(highlightSELECTOR).get().strip(),
                'resort_amenities': wyndham.xpath(resort_amenitiesSELECTOR).getall()
            }

        # This for loop gets the room data; name, square feet, bed types, max guests,, number of bathrooms,
        # type of kitchen, Washer/Dryer (if applicable), amenities, and images(not yet implemented)
        unit = '//*[@* = "wyn-bedroom-card"]'
        for bedroom in response.xpath(unit):

            room_type_1SELECTOR = './/div[@class = "wyn-type-title-2 wyn-color-black"]/text()'
            # for presidential, presidential reserve, and other 'unique' units with second name
            # room_type_2SELECTOR = './/d[@class ="wyn-bedroom-card__detail__row"]/div[@class = "wyn-type-title-2 wyn-color-black"][2]/text()'
            sqft_guestCountSELECTOR = './/div[@class = "wyn-color-grey wyn-type-body-2 wyn-color-grey"]/text()'
            bed_typeSELECTOR = 'normalize-space(.//div[@class = "wyn-bedroom-card__detail__row"]/div[@class = "wyn-color-grey wyn-type-body-2 wyn-color-grey wyn-bedroom-card__detail__row__icons"]/text())'
            num_bathsSELECTOR = './/div[@class = "wyn-bedroom-card__detail__row"]/div[@class = "wyn-color-grey wyn-type-body-2 wyn-color-grey"]/text()'
            room_amenitiesSELECTOR = './/li[@class = "wyn-color-grey wyn-type-body-2"]/text()'
            # this is for the second room name
            #room_exists = bedroom.xpath(room_type_2SELECTOR)

            ############################################################################
            # Attempt to figure out how to print both names for room if it exists and print out the one name
            # if it does not have a second name
            # second name for rooms exist in a separate div as a sibling
            # to the first div with the room's first name
            # room = []
            # for room in room_exists:
            #     if room_exists is not None:
            #         room_name_1 = bedroom.xpath(
            #             room_type_1SELECTOR).get().strip()
            #         room_name_2 = bedroom.xpath(
            #             room_type_2SELECTOR).get().strip()
            #         room_name = room_name_1 + " " + room_name_2
            #         room.append(str(room_name))
            #     else:
            #         room_name = bedroom.xpath(
            #             room_type_1SELECTOR).get().strip()
            #         room.append(str(room_name))

            ##############################################################################

            # strips the room amenities list of all extra spaces and \n
            ls = bedroom.xpath(room_amenitiesSELECTOR).getall()
            room_amenities = [amenity.strip() for amenity in ls]

            # This contains both the square feet and guest count per room
            sqft_guest = bedroom.xpath(sqft_guestCountSELECTOR).get().strip()
            # pulls just the square feet for each room with RegEx
            sqft_pattern = re.compile(r'\d*,?\d+\s?\-?\s?\d*,?\d+')
            sqft = re.findall(sqft_pattern, sqft_guest)
            # grabs square feet and max_guest count per room and puts them into an array
            # to pull max_guest
            max_guest = []
            for guest in sqft_guest.split():
                if guest.isdigit():
                    max_guest.append(int(guest))

            # Pulls type of kitchen; Full, Mini, Partial, None, Varies
            kitchen_varieties = 'Kitchen:'
            kitchen = list(
                filter(lambda x: kitchen_varieties in x, room_amenities))

            # Pulls Washer/Dryer amenity if available
            washer_amenity = 'Washer'
            washer_dryer = list(
                filter(lambda x: washer_amenity in x, room_amenities))

            # Extracts the washer/dryer and kitchen type from the room_amenities list
            room_amenities = [
                x for x in room_amenities if not x.startswith('Kitchen:')]
            room_amenities = [
                x for x in room_amenities if not x.startswith('Washer')]

            # Strips all but the number for bathrooms
            bathrooms = bedroom.xpath(num_bathsSELECTOR).get().strip()
            bathroom = []
            for bath in bathrooms.split():
                if bath.isdigit():
                    bathroom.append(int(bath))

            yield {
                'room_type': bedroom.xpath(room_type_1SELECTOR).get().strip(),
                #Testing for second name of room
                #'room_label': bedroom.xpath(room_type_2SELECTOR).get().strip(),
                'bed_type': bedroom.xpath(bed_typeSELECTOR).get().strip(),
                # [-1] pulls the last number from the array containing square feet and max_guests
                # in which the last number [-1] is the max_guest number
                'sleeps': max_guest[-1],
                'num_baths': bathroom,
                'sqft': sqft[0],
                'kitchen': kitchen,
                'washer_dryer': washer_dryer,
                'amenities': room_amenities
            }
