import json
from operator import lt, gt
from get_xml_tree import get_xml_tree


def get_all_flights(tree_xml):
    root = tree_xml.getroot()
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


def get_flights_sorted_price(all_flights, compare=''):
    operation = {
        'min': lt,
        'max': gt,
    }

    list_max_price = []
    max_price = float(all_flights[0]['Price']['TicketPrice'])

    for flight in all_flights:
        price = float(flight['Price']['TicketPrice'])
        index = all_flights.index(flight)
        if operation[compare](price, max_price):
            max_price = price
            list_max_price = []
            list_max_price.append(all_flights[index])
        elif price == max_price:
            list_max_price.append(all_flights[index])

    return list_max_price
