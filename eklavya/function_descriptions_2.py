functions_2 = [{
    "name":
        "query_photoobj",
    "description":
        "Queries the service and returns a table object, At least one of run, camcol or field parameters must be specified. Returns:table A Table object.",
    "parameters": {
        "type": "object",
        "properties": {
            "run": {
                "type": "integer",
                "description": "Length of a strip observed in a single continuous image observing scan.",
            },
            "rerun": {
                "type": "integer",
                "description": "Reprocessing of an imaging run. Defaults to 301 which is the most recent rerun.",
            },
            "camcol": {
                "type": "integer",
                "description": "Output of one camera column of CCDs.",
            },
            "field": {
                "type": "integer",
                "description": "Part of a camcol of size 2048 by 1489 pixels.",
            },
            "fields": {
                "type": ["array", "null"],
                "items": {
                    "type": "string"
                },
                "description":
                    "SDSS PhotoObj or SpecObj quantities to return. If None, defaults to quantities required to find corresponding spectra and images of matched objects (e.g. plate, fiberID, mjd, etc.)."
            },
            "timeout": {
                "type": ["number", "null"],
                "description":
                    "Time limit (in seconds) for establishing a successful connection with the remote server. Defaults to SDSSClass.TIMEOUT."
            },
            "field_help": {
                "type": ["boolean", "string", "null"],
                "description":
                    "Field name to check whether a valid PhotoObjAll or SpecObjAll field name. If True or it is an invalid field name, all the valid field names are returned as a dict."
            },
            "get_query_payload": {
                "type": ["boolean", "null"],
                "description": "If True, this will return the data the query would have sent out, but does not actually do the query."
            },
            "data_release": {
                "type": ["integer", "null"],
                "description": "The data release of the SDSS to use."
            },
            "cache": {
                "type": ["boolean", "null"],
                "description": "If True, use the request caching mechanism."
            }
        },
        "anyOf": [{
            "required": ["run"]
        }, {
            "required": ["camcol"]
        }, {
            "required": ["field"]
        }]
    },
}, {
    "name":
        "query_photoobj_async",
    "description":
        "Used to query the PhotoObjAll table with run, rerun, camcol, and field values. At least one of run, camcol, or field parameters must be specified.",
    "parameters": {
        "type": "object",
        "properties": {
            "run": {
                "type": ["integer", "null"],
                "description": "Length of a strip observed in a single continuous image observing scan."
            },
            "rerun": {
                "type": ["integer", "null"],
                "description": "Reprocessing of an imaging run. Defaults to 301 which is the most recent rerun."
            },
            "camcol": {
                "type": ["integer", "null"],
                "description": "Output of one camera column of CCDs."
            },
            "field": {
                "type": ["integer", "null"],
                "description": "Part of a camcol of size 2048 by 1489 pixels."
            },
            "fields": {
                "type": ["array", "null"],
                "items": {
                    "type": "string"
                },
                "description":
                    "SDSS PhotoObj or SpecObj quantities to return. If None, defaults to quantities required to find corresponding spectra and images of matched objects (e.g. plate, fiberID, mjd, etc.)."
            },
            "timeout": {
                "type": ["number", "null"],
                "description":
                    "Time limit (in seconds) for establishing a successful connection with the remote server. Defaults to SDSSClass.TIMEOUT."
            },
            "field_help": {
                "type": ["boolean", "string", "null"],
                "description":
                    "Field name to check whether a valid PhotoObjAll or SpecObjAll field name. If True or it is an invalid field name, all the valid field names are returned as a dict."
            },
            "get_query_payload": {
                "type": ["boolean", "null"],
                "description": "If True, this will return the data the query would have sent out, but does not actually do the query."
            },
            "data_release": {
                "type": ["integer", "null"],
                "description": "The data release of the SDSS to use."
            },
            "cache": {
                "type": ["boolean", "null"],
                "description": "If True, use the request caching mechanism."
            }
        },
        "anyOf": [{
            "required": ["run"]
        }, {
            "required": ["camcol"]
        }, {
            "required": ["field"]
        }]
    }
}, {
    "name":
        "get_images",
    "description":
        "Download an image from SDSS.Querying SDSS for images will return the entire plate. For subsequent analyses of individual objects. Function is used when the user asks for an image",
    "parameters": {
        "type": "object",
        "properties": {
            "coordinates": {
                "type": ["string", "null"],
                "description":
                    "The target around which to search.These will be provided in the form of celestial coordinate system, for example 0h8m05.63s +14d50m23.3s or some variant of an input that can be converted to the elestial coordinate system, specifically in the format used for specifying positions in the sky. This format is known as the sexagesimal system, which uses hours, minutes, and seconds to represent angles."
            },
            "radius": {
                "type": ["string", "null"],
                "description":
                    "The string must be parsable by Angle. The appropriate Quantity object from astropy.units may also be used. Defaults to 2 arcsec."
            },
            "matches": {
                "type": ["object", "null"],
                "description": "Result of query_region."
            },
            "run": {
                "type": ["integer", "null"],
                "description": "Length of a strip observed in a single continuous image observing scan."
            },
            "rerun": {
                "type": ["integer", "null"],
                "description": "Reprocessing of an imaging run. Defaults to 301 which is the most recent rerun."
            },
            "camcol": {
                "type": ["integer", "null"],
                "description": "Output of one camera column of CCDs."
            },
            "field": {
                "type": ["integer", "null"],
                "description": "Part of a camcol of size 2048 by 1489 pixels."
            },
            "band": {
                "type": ["string", "array"],
                "description": "Could be individual band or list of bands. Options: 'u', 'g', 'r', 'i', or 'z'."
            },
            "timeout": {
                "type": ["number", "null"],
                "description":
                    "Time limit (in seconds) for establishing a successful connection with the remote server. Defaults to SDSSClass.TIMEOUT."
            },
            "get_query_payload": {
                "type": ["boolean", "null"],
                "description": "If True, this will return the data the query would have sent out, but does not actually do the query."
            },
            "cache": {
                "type": ["boolean", "null"],
                "description": "Cache the images using astropy’s caching system."
            },
            "data_release": {
                "type": ["integer", "null"],
                "description": "The data release of the SDSS to use."
            },
            "show_progress": {
                "type": ["boolean", "null"],
                "description": "If False, do not display download progress."
            }
        },
        "anyOf": [{
            "required": ["matches"]
        }, {
            "required": ["coordinates", "radius"]
        }, {
            "required": ["run", "rerun", "camcol", "field"]
        }],
    }
}, {
    "name": "query_crossid",
    "description": "Query using the cross-identification web interface. This query returns the nearest primary object.",
    "parameters": {
        "type": "object",
        "properties": {
            "coordinates": {
                "type":
                    "string",
                "description":
                    "The target(s) around which to search. These will be provided in the form of celestial coordinate system, for example 0h8m05.63s +14d50m23.3s or some variant of an input that can be converted to the elestial coordinate system, specifically in the format used for specifying positions in the sky. This format is known as the sexagesimal system, which uses hours, minutes, and seconds to represent angles.",
            },
            "radius": {
                "type": ["string", "null"],
                "description": "The string must be parsable by Angle. Defaults to 2 arcsec.",
            },
            "timeout": {
                "type": ["number", "null"],
                "description":
                    "Time limit (in seconds) for establishing successful connection with remote server. Defaults to SDSSClass.TIMEOUT.",
            },
            "fields": {
                "type": ["array", "null"],
                "items": {
                    "type": "number"
                },
                "description":
                    "SDSS PhotoObj or SpecObj quantities to return. If None, defaults to quantities required to find corresponding spectra and images of matched objects (e.g. plate, fiberID, mjd, etc.).",
            },
            "photoobj_fields": {
                "type": ["array", "null"],
                "items": {
                    "type": "number"
                },
                "description":
                    "PhotoObj quantities to return. If photoobj_fields is None and specobj_fields is None then the value of fields is used",
            }
        },
    },
}, {
    "name": "query_crossid_async",
    "description": "Query using the cross-identification web interface. This query returns the nearest primary object.",
    "parameters": {
        "type": "object",
        "properties": {
            "coordinates": {
                "type":
                    "string",
                "description":
                    "The target(s) around which to search. These will be provided in the form of celestial coordinate system, for example 0h8m05.63s +14d50m23.3s or some variant of an input that can be converted to the elestial coordinate system, specifically in the format used for specifying positions in the sky. This format is known as the sexagesimal system, which uses hours, minutes, and seconds to represent angles.",
            },
            "radius": {
                "type": ["string", "null"],
                "description": "The string must be parsable by Angle. Defaults to 2 arcsec.",
            },
            "timeout": {
                "type": ["number", "null"],
                "description":
                    "Time limit (in seconds) for establishing successful connection with remote server. Defaults to SDSSClass.TIMEOUT.",
            },
            "fields": {
                "type": ["array", "null"],
                "items": {
                    "type": "number"
                },
                "description":
                    "SDSS PhotoObj or SpecObj quantities to return. If None, defaults to quantities required to find corresponding spectra and images of matched objects (e.g. plate, fiberID, mjd, etc.).",
            },
            "photoobj_fields": {
                "type": ["array", "null"],
                "items": {
                    "type": "number"
                },
                "description":
                    "PhotoObj quantities to return. If photoobj_fields is None and specobj_fields is None then the value of fields is used",
            }
        },
    },
}, {
    "name": "query_region",
    "description": "Queries the service and returns a table object",
    "parameters": {
        "type": "object",
        "properties": {
            "coordinates": {
                "type": ["string", "null"],
                "description":
                    "The target(s) around which to search. These will be provided in the form of celestial coordinate system, for example 0h8m05.63s +14d50m23.3s or some variant of an input that can be converted to the elestial coordinate system, specifically in the format used for specifying positions in the sky. This format is known as the sexagesimal system, which uses hours, minutes, and seconds to represent angles.",
            },
            "radius": {
                "type": ["string", "null"],
                "description":
                    "The string must be parsable by Angle. The appropriate Quantity object from astropy.units may also be used. The maximum allowed value is 3 arcmin",
            },
            "width": {
                "type": ["string", "null"],
                "description": "The string must be parsable by Angle. The appropriate Quantity object from astropy.units may also be used.",
            },
            "height": {
                "type": ["string", "null"],
                "description": "The string must be parsable by Angle.",
            },
            "timeout": {
                "type": ["integer", "null"],
                "description": "Time limit (in seconds) for establishing successful connection with remote server."
            }
        },
        "anyOf": [{
            "required": ["coordinates", "radius"]
        }, {
            "required": ["coordinates", "radius"]
        }]
    },
}, {
    "name": "get_spectra",
    "description": "Download spectrum from SDSS.",
    "parameters": {
        "type": "object",
        "properties": {
            "coordinates": {
                "type": ["string", "null"],
                "description":
                    "The target around which to search. These will be provided in the form of celestial coordinate system, for example 0h8m05.63s +14d50m23.3s or some variant of an input that can be converted to the elestial coordinate system, specifically in the format used for specifying positions in the sky. This format is known as the sexagesimal system, which uses hours, minutes, and seconds to represent angles."
            },
            "radius": {
                "type": ["string", "null"],
                "description":
                    "The string must be parsable by Angle. The appropriate Quantity object from astropy.units may also be used. Defaults to 2 arcsec."
            },
            "matches": {
                "type": ["object", "null"],
                "description": "Result of query_region."
            },
            "plate": {
                "type": ["integer", "null"],
                "description": "Plate number."
            },
            "fiberID": {
                "type": ["integer", "null"],
                "description": "Fiber number."
            },
            "mjd": {
                "type": ["integer", "null"],
                "description": "Modified Julian Date indicating the date a given piece of SDSS data was taken."
            },
            "timeout": {
                "type": ["number", "null"],
                "description":
                    "Time limit (in seconds) for establishing a successful connection with the remote server. Defaults to SDSSClass.TIMEOUT."
            },
            "get_query_payload": {
                "type": ["boolean", "null"],
                "description": "If True, this will return the data the query would have sent out, but does not actually do the query."
            },
            "data_release": {
                "type": ["integer", "null"],
                "description": "The data release of the SDSS to use. With the default server, this only supports DR8 or later."
            },
            "cache": {
                "type": ["boolean", "null"],
                "description": "Cache the spectra using astropy’s caching system."
            },
            "show_progress": {
                "type": ["boolean", "null"],
                "description": "If False, do not display download progress."
            }
        },
        "anyOf": [{
            "required": ["matches"]
        }, {
            "required": ["coordinates", "radius"]
        }, {
            "required": ["plate", "fiberID", "mjd"]
        }],
    }
}, {
    "name": "query_specobj",
    "description": "Queries the service and returns a table object. Used to query the SpecObjAll table with plate, mjd and fiberID values.",
    "parameters": {
        "type": "object",
        "properties": {
            "plate": {
                "type": ["integer", "null"],
                "description": "Plate number."
            },
            "mjd": {
                "type": ["integer", "null"],
                "description": "Modified Julian Date indicating the date a given piece of SDSS data was taken."
            },
            "fiberID": {
                "type": ["integer", "null"],
                "description": "Fiber number."
            },
            "fields": {
                "type": ["array", "null"],
                "description":
                    "SDSS PhotoObj or SpecObj quantities to return. If None, defaults to quantities required to find corresponding spectra and images of matched objects (e.g. plate, fiberID, mjd, etc.)."
            }
        },
        "anyOf": [
            {
                "required": ["plate"]
            },
            {
                "required": ["mjd"]
            },
            {
                "required": ["fiberID"]
            },
        ],
    }
}, {
    "name": "query_specobj_async",
    "description": "Queries the service and returns a table object. Used to query the SpecObjAll table with plate, mjd and fiberID values.",
    "parameters": {
        "type": "object",
        "properties": {
            "plate": {
                "type": ["integer", "null"],
                "description": "Plate number."
            },
            "mjd": {
                "type": ["integer", "null"],
                "description": "Modified Julian Date indicating the date a given piece of SDSS data was taken."
            },
            "fiberID": {
                "type": ["integer", "null"],
                "description": "Fiber number."
            },
            "fields": {
                "type": ["array", "null"],
                "description":
                    "SDSS PhotoObj or SpecObj quantities to return. If None, defaults to quantities required to find corresponding spectra and images of matched objects (e.g. plate, fiberID, mjd, etc.)."
            }
        },
        "anyOf": [
            {
                "required": ["plate"]
            },
            {
                "required": ["mjd"]
            },
            {
                "required": ["fiberID"]
            },
        ],
    }
}, {
    "name": "get_spectral_template",
    "description": "Download spectral templates from SDSS DR-2.",
    "parameters": {
        "type": "object",
        "properties": {
            "kind": {
                "type": ["string", "array"],
                "description":
                    "Which spectral template to download? Options are stored in the dictionary astroquery.sdss.SDSS.AVAILABLE_TEMPLATES."
            },
            "timeout": {
                "type": ["number", "null"],
                "description":
                    "Time limit (in seconds) for establishing a successful connection with the remote server. Defaults to SDSSClass.TIMEOUT."
            },
            "show_progress": {
                "type": ["boolean", "null"],
                "description": "If False, do not display download progress."
            }
        },
        "required": ["kind"],
    }
}]
