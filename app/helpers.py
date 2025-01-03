from app.models import TwoLineElementRecord, TwoLineElementRecordParsed, SourcePayload, ModifiedPayload

# This function takes a single TLE record and parses the line elements into distinct key-value pairs
# Definitions for 
def parse_tle(tle: TwoLineElementRecord) -> TwoLineElementRecordParsed:
    """Parses a single Two-Line Element record

    Takes each record from the member list and parses line1 and line2 into
    distinct key-value pairs.

    Args:
        tle: object created from class TwoLineElementRecord

    Returns:
        An object with the lines parsed created from class TwoLineElementRecordParsed
        Returned as a Pydantic model.

    Reference: https://ensatellite.com/tle/
    """

    #Extract second derivative mean motion
    sdmm_raw = tle.line1[44:52]
    sdmm_sign = 1 if sdmm_raw[6] == '+' else -1
    second_derivative_mean_motion = float(sdmm_raw[:6]) * 10 ** (sdmm_sign * int(sdmm_raw[7]))
    
    # Extract BSTAR
    bstar_raw = tle.line1[53:61]
    bstar_sign = 1 if bstar_raw[6] == '+' else -1
    bstar = float(bstar_raw[:6]) * 10 ** (bstar_sign * int(bstar_raw[7]))
    
    return TwoLineElementRecordParsed(
        id = tle.id,
        type = tle.type,
        satelliteId = tle.satelliteId,
        name = tle.name,
        date = tle.date,
        line_number = tle.line1[0], 
        satellite_catalog_number = tle.line1[2:7],
        classification = tle.line1[7],
        international_designator = tle.line1[9:15],
        epoch_year = tle.line1[18:20],
        epoch_day = tle.line1[20:32],
        first_derivative_mean_motion = tle.line1[33:43],
        second_derivative_mean_motion = second_derivative_mean_motion,
        bstar = bstar,
        ephemeris_type = tle.line1[62],
        element_set_number = tle.line1[64:68],
        line1_check_sum = tle.line1[68],
        inclination = tle.line2[8:16],
        right_ascension = tle.line2[17:25],
        eccentricity = float(tle.line2[26:33]) / 1e7,
        argument_of_perigee = tle.line2[34:42],
        mean_anomaly = tle.line2[43:51],
        mean_motion = tle.line2[52:63],
        revolution_number = tle.line2[63:68],
        line2_check_sum = tle.line2[68]
    )

def modify_payload(source_payload: SourcePayload) -> ModifiedPayload:
    """Modifies a TLE payload

    Uses the same structure as the response payload, but has the TLE records
    parsed into distinct key-value pairs.

    Args:
        source_payload: object created from class SourcePayload

    Returns:
        An response payload with the TLE records parsed into key-value pairs
        Returned as a Pydantic model.
    """

    modified_members = [parse_tle(member) for member in source_payload.member]

    # Create the modified payload
    return ModifiedPayload(
        context=source_payload.context,
        id=source_payload.id,
        type=source_payload.type,
        totalItems=source_payload.totalItems,
        member=modified_members,
        parameters=source_payload.parameters,
        view=source_payload.view
    )