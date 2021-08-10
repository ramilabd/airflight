import operator
from .parser_xml import get_xml_tree


def get_all_flights():
    root = get_xml_tree('./airflight/data/RS_Via-3.xml')().getroot()
    all_flights = []

    for Flights in root.xpath('//OnwardPricedItinerary/Flights'):
        routs = {}
        order = 0

        for Flight in Flights.iter('Flight'):
            flight = {}
            order += 1

            for elem in Flight.iter('*'):
                if elem.tag in {'Flight', 'WarningText', 'FareBasis', 'NumberOfStops', 'Class', 'TicketType'}:
                    continue
                tag = elem.tag
                text = elem.text
                flight[tag] = text

            routs['flight_{}'.format(order)] = flight

        currency = Flights.find('../../Pricing').attrib['currency']
        price = Flights.find('../../Pricing/ServiceCharges[@ChargeType="TotalAmount"]').text
        routs['Price'] = dict(TicketPrice=price, Currency=currency)

        all_flights.append(routs)

    return all_flights


def get_flights_sorted_price(compare=''):
    all_flights = get_all_flights()
    operation = {
        'min': operator.lt,
        'max': operator.gt,
    }

    list_price = []
    max_price = float(all_flights[0]['Price']['TicketPrice'])

    for flight in all_flights:
        price = float(flight['Price']['TicketPrice'])
        index = all_flights.index(flight)
        if operation[compare](price, max_price):
            max_price = price
            list_price = []
            list_price.append(all_flights[index])
        elif price == max_price:
            list_price.append(all_flights[index])

    return list_price
