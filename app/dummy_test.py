from models import TwoLineElementRecord, TwoLineElementRecordParsed
from helpers import parse_tle

print(f"Imported models and helpers")

test_tle = {
    "@id": "https://tle.ivanstanojevic.me/api/tle/694",
    "@type": "Tle",
    "satelliteId": 694,
    "name": "ATLAS CENTAUR 2",
    "date": "2024-12-30T16:44:23+00:00",
    "line1": "1 00694U 63047A   24365.69749068  .00009556  00000+0  11813-2 0  9998",
    "line2": "2 00694  30.3575  96.7654 0557567 222.2164 133.4191 14.09575246 70287"
}
print("Created test JSON")
print(test_tle)

test_tle_from_class = TwoLineElementRecord(
    id=test_tle["@id"],
    type=test_tle["@type"],
    satelliteId=test_tle["satelliteId"],
    name=test_tle["name"],
    date=test_tle["date"],
    line1=test_tle["line1"],
    line2=test_tle["line2"]
)
print(f"Created tle object from class TwoLineElementRecord")
print(test_tle_from_class)
print("..")
print("..")
print("Starting Parse!")


parsed_tle = parse_tle(test_tle_from_class)
print("Parsed TLE!")
print(parsed_tle)