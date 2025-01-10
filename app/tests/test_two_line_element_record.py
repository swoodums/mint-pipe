from app.models import TwoLineElementRecord

def test_two_line_element_record() -> None:
    two_line_element_record = TwoLineElementRecord(
        **{
            "@id": "test_id",
            "@type": "test_tle",
            "satelliteId": 42069,
            "name": "BLOODGULCH",
            "date": "2024-12-30",
            "line1": "digimon digital monsters",
            "line2": "digimon are the champions"
        }
    )

    assert two_line_element_record.id == "test_id"
    assert two_line_element_record.type == "test_tle"
    assert two_line_element_record.satelliteId == 42069
    assert two_line_element_record.name == "BLOODGULCH"
    assert two_line_element_record.date == "2024-12-30"
    assert two_line_element_record.line1 == "digimon digital monsters"
    assert two_line_element_record.line2 == "digimon are the champions"