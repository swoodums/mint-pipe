from app.models import TwoLineElementRecord
from app.helpers import parse_tle

def test_parse_tle() -> None:
    two_line_element_record = TwoLineElementRecord(
        **{
            "@id": "https://tle.ivanstanojevic.me/api/tle/694",
            "@type": "Tle",
            "satelliteId": 694,
            "name": "ATLAS CENTAUR 2",
            "date": "2025-01-09T06:11:00+00:00",
            "line1": "1 00694U 63047A   25009.25764709  .00005194  00000+0  63524-3 0  9996",
            "line2": "2 00694  30.3594  43.5454 0557114 306.1368  48.8899 14.09718149 71637"
        }
    )
    two_line_element_record_parsed = parse_tle(two_line_element_record)

    assert two_line_element_record_parsed.id == "https://tle.ivanstanojevic.me/api/tle/694"
    assert two_line_element_record_parsed.type == "Tle"
    assert two_line_element_record_parsed.satelliteId == 694
    assert two_line_element_record_parsed.name == "ATLAS CENTAUR 2"
    assert two_line_element_record_parsed.date == "2025-01-09T06:11:00+00:00"
    assert two_line_element_record_parsed.satellite_catalog_number == 694
    assert two_line_element_record_parsed.classification == "U"
    assert two_line_element_record_parsed.international_designator == "63047A"
    assert two_line_element_record_parsed.epoch_year == 25
    assert two_line_element_record_parsed.epoch_day == 9.25764709
    assert two_line_element_record_parsed.first_derivative_mean_motion == 5.194e-05
    assert two_line_element_record_parsed.second_derivative_mean_motion == 0.0
    assert two_line_element_record_parsed.bstar == 63.524
    assert two_line_element_record_parsed.ephemeris_type == 0
    assert two_line_element_record_parsed.element_set_number == 999
    assert two_line_element_record_parsed.line1_check_sum == 6
    assert two_line_element_record_parsed.inclination == 30.3594
    assert two_line_element_record_parsed.right_ascension == 43.5454
    assert two_line_element_record_parsed.eccentricity == 0.0557114
    assert two_line_element_record_parsed.argument_of_perigee == 306.1368
    assert two_line_element_record_parsed.mean_anomaly == 48.8899
    assert two_line_element_record_parsed.mean_motion == 14.09718149
    assert two_line_element_record_parsed.revolution_number == 7163
    assert two_line_element_record_parsed.line2_check_sum == 7