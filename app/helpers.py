import json

def parse_tle(tle):
    line1 = tle["line1"]
    line2 = tle["line2"]
    
    # Extract information from line1
    line_number = int(line1[0])
    satellite_catalog_number = int(line1[2:7])
    classification = line1[7]
    international_designator = line1[9:17]
    epoch_year = int(line1[18:20])
    epoch_day = float(line1[20:32])
    first_derivative_mean_motion = float(line1[33:43])
    #Extract second derivative mean motion
    sdmm_raw = line1[44:52]
    sdmm_sign = 1 if sdmm_raw[6] == '+' else -1
    second_derivative_mean_motion = float(sdmm_raw[:6]) * 10 ** (sdmm_sign * int(sdmm_raw[7]))
    # Extract BSTAR
    bstar_raw = line1[53:61]
    bstar_sign = 1 if bstar_raw[6] == '+' else -1
    bstar = float(bstar_raw[:6]) * 10 ** (bstar_sign * int(bstar_raw[7]))
    ephemeris_type = int(line1[62])
    element_set_number = int(line1[64:68])
    line1_check_sum = int(line1[68])
    
    # Extract information from line2
    inclination = float(line2[8:16])
    right_ascension = float(line2[17:25])
    eccentricity = float(line2[26:33]) / 1e7
    argument_of_perigee = float(line2[34:42])
    mean_anomaly = float(line2[43:51])
    mean_motion = float(line2[52:63])
    revolution_number = int(line2[63:68])
    line2_check_sum = int(line2[68])
    
    # Create the new JSON structure
    transformed_tle = {
        "@id": tle["@id"],
        "@type": tle["@type"],
        "satelliteId": tle["satelliteId"],
        "name": tle["name"],
        "date": tle["date"],
        "line_number": line_number,
        "satellite_catalog_number": satellite_catalog_number,
        "classification": classification,
        "international_designator": international_designator,
        "epoch_year": epoch_year,
        "epoch_day": epoch_day,
        "first_derivative_mean_motion": first_derivative_mean_motion,
        "second_derivative_mean_motion": second_derivative_mean_motion,
        "bstar": bstar,
        "ephemeris_type": ephemeris_type,
        "element_set_number": element_set_number,
        "line1_check_sum": line1_check_sum,
        "inclination": inclination,
        "right_ascension": right_ascension,
        "eccentricity": eccentricity,
        "argument_of_perigee": argument_of_perigee,
        "mean_anomaly": mean_anomaly,
        "mean_motion": mean_motion,
        "revolution_number": revolution_number,
        "line2_check_sum": line2_check_sum
    }
    
    return transformed_tle

def parse_mutliple_tles(tles):
    return [parse_tle(tle) for tle in tles]