class wynSpider(scrapy.Spider):
    name = "wynSpider"
    start_urls = ['https://clubwyndham.wyndhamdestinations.com/us/en/resorts/wyndham-hotels-resorts/united-states-of-america/florida/orlando/worldmark-orlando-kingstown-reef']

    def parse(self, response):
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

        unit = '//*[@* = "wyn-bedroom-card"]'
        for bedroom in response.xpath(unit):

            room_typeSELECTOR = './/div[@class = "wyn-type-title-2 wyn-color-black"]/text()'
            sqft_guestCountSELECTOR = './/div[@class = "wyn-color-grey wyn-type-body-2 wyn-color-grey"]/text()'
            bed_typeSELECTOR = 'normalize-space(.//div[@class = "wyn-bedroom-card__detail__row"]/div[@class = "wyn-color-grey wyn-type-body-2 wyn-color-grey wyn-bedroom-card__detail__row__icons"]/text())'
            num_bathsSELECTOR = './/div[@class = "wyn-bedroom-card__detail__row"]/div[@class = "wyn-color-grey wyn-type-body-2 wyn-color-grey"]/text()'
            room_amenitiesSELECTOR = './/li[@class = "wyn-color-grey wyn-type-body-2"]/text()'

            yield {
                'room_type': bedroom.xpath(room_typeSELECTOR).get().strip(),
                'sqft_guestCount': bedroom.xpath(sqft_guestCountSELECTOR).get().strip(),
                'bed_type': bedroom.xpath(bed_typeSELECTOR).get().strip(),
                'num_baths': bedroom.xpath(num_bathsSELECTOR).get().strip(),
                'amenities': bedroom.xpath(room_amenitiesSELECTOR).getall()
            }

