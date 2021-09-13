from datetime import datetime, timedelta
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

    return list(map(add_total_travel_time, all_flights))


def add_total_travel_time(flight, str_time=False):
    departure_time = flight['flight_1']['DepartureTimeStamp']
    if 'flight_2' in flight:
        arrival_time = flight['flight_2']['ArrivalTimeStamp']
    else:
        arrival_time = flight['flight_1']['ArrivalTimeStamp']
    time_delta = datetime.strptime(arrival_time, '%Y-%m-%dT%H%M') - datetime.strptime(departure_time, '%Y-%m-%dT%H%M')
    flight['TotalTravelTime'] = str(time_delta) if str_time else time_delta
    return flight


def get_flights_sorted_price(flights, reverse=False, number_flights=None):
    return sorted(flights, key=lambda flight: float(flight['Price']['TicketPrice']), reverse=reverse)[:number_flights]


def get_flights_sorted_time(flights, reverse=False, number_flights=None):
    return sorted(flights, key=lambda flight: flight['TotalTravelTime'], reverse=reverse)


def get_flights_sorted_direction(source, destination):
    all_flights = get_all_flights()
    sorted_flights = []

    for flight in all_flights:
        if 'flight_2' not in flight:
            if flight['flight_1']['Source'] == source and flight['flight_1']['Destination'] == destination:
                sorted_flights.append(flight)
        else:
            if flight['flight_1']['Source'] == source and flight['flight_2']['Destination'] == destination:
                sorted_flights.append(flight)

    return sorted_flights
