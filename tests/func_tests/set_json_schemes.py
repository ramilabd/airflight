# -*- coding: utf8 -*-
"""A set of schemes.

Used for testing (validation) json returned by a web service.
"""

flight1_flight2_scheme = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "Price": {
            "type": "object",
            "properties": {
                "Currency": {
                    "type": "string",
                },
                "TicketPrice": {
                    "type": "string",
                },
            },
            "required": ["Currency", "TicketPrice"],
        },
        "TotalTravelTime": {
            "type": "string",
        },
        "flight1": {
            "type": "object",
            "properties": {
                "ArrivalTimeStamp": {
                    "type": "string",
                },
                "Carrier": {
                    "type": "string",
                },
                "Class": {
                    "type": "string",
                },
                "DepartureTimeStamp": {
                    "type": "string",
                },
                "Destination": {
                    "type": "string",
                },
                "FareBasis": {
                    "type": "string",
                },
                "FlightNumber": {
                    "type": "string",
                },
                "NumberOfStops": {
                    "type": "string",
                },
                "Source": {
                    "type": "string",
                },
                "TicketType": {
                    "type": "string",
                },
            },
            "required": [
                "ArrivalTimeStamp",
                "Carrier",
                "Class",
                "DepartureTimeStamp",
                "Destination",
                "FareBasis",
                "FlightNumber",
                "NumberOfStops",
                "Source",
                "TicketType",
            ],
        },
        "flight2": {
            "type": "object",
            "properties": {
                "ArrivalTimeStamp": {
                    "type": "string",
                },
                "Carrier": {
                    "type": "string",
                },
                "Class": {
                    "type": "string",
                },
                "DepartureTimeStamp": {
                    "type": "string",
                },
                "Destination": {
                    "type": "string",
                },
                "FareBasis": {
                    "type": "string",
                },
                "FlightNumber": {
                    "type": "string",
                },
                "NumberOfStops": {
                    "type": "string",
                },
                "Source": {
                    "type": "string",
                },
                "TicketType": {
                    "type": "string",
                },
            },
            "required": [
                "ArrivalTimeStamp",
                "Carrier",
                "Class",
                "DepartureTimeStamp",
                "Destination",
                "FareBasis",
                "FlightNumber",
                "NumberOfStops",
                "Source",
                "TicketType",
            ],
        },
    },
    "required": ["Price", "TotalTravelTime", "flight1", "flight2"],
}

flight1_scheme = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "Price": {
            "type": "object",
            "properties": {
                "Currency": {
                    "type": "string",
                },
                "TicketPrice": {
                    "type": "string",
                },
            },
            "required": ["Currency", "TicketPrice"],
        },
        "TotalTravelTime": {
            "type": "string",
        },
        "flight1": {
            "type": "object",
            "properties": {
                "ArrivalTimeStamp": {
                    "type": "string",
                },
                "Carrier": {
                    "type": "string",
                },
                "Class": {
                    "type": "string",
                },
                "DepartureTimeStamp": {
                    "type": "string",
                },
                "Destination": {
                    "type": "string",
                },
                "FareBasis": {
                    "type": "string",
                },
                "FlightNumber": {
                    "type": "string",
                },
                "NumberOfStops": {
                    "type": "string",
                },
                "Source": {
                    "type": "string",
                },
                "TicketType": {
                    "type": "string",
                },
            },
            "required": [
                "ArrivalTimeStamp",
                "Carrier",
                "Class",
                "DepartureTimeStamp",
                "Destination",
                "FareBasis",
                "FlightNumber",
                "NumberOfStops",
                "Source",
                "TicketType",
            ],
        },
    },
    "required": ["Price", "TotalTravelTime", "flight1"],
}


route_scheme = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "Destination": {
            "type": "string",
        },
        "Source": {
            "type": "string",
        },
        "Transfer": {
            "type": "string",
        },
    },
    "required": [
        "Destination",
        "Source",
        "Transfer",
    ],
}


min_route_scheme = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "Destination": {
            "type": "string",
        },
        "Source": {
            "type": "string",
        },
    },
    "required": [
        "Destination",
        "Source",
    ],
}
