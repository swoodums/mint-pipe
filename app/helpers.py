from .models import TwoLineElementRecord, TwoLineElementRecordParsed, SourcePayload, ModifiedPayload
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_robust_session():
    session = requests.Session()
    
    # Configure retry strategy
    retry_strategy = Retry(
        total=3,  # number of retries
        backoff_factor=1,  # wait 1, 2, 4 seconds between retries
        status_forcelist=[500, 502, 503, 504],  # retry on these status codes
        allowed_methods=["GET"]  # only retry on GET requests
    )
    
    # Mount the adapter to the session
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    
    return session

def fetch_tle_data(url='https://tle.ivanstanojevic.me/api/tle/'):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "DNT": "1",
        "Host": "tle.ivanstanojevic.me",
        "Priority":	"u=0, i",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Sec-GPC": "1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.0"
    }
    
    session = create_robust_session()
    
    try:
        #Using session with stream=True
        with session.get(url, headers=headers, stream=True) as response:
            print(f"Status Code: {response.status_code}")
            print(f"Response Headers: {dict(response.headers)}")
            return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"Request failed. Error: {str(e)}")
        raise SystemExit(e)

def parse_tle(tle: TwoLineElementRecord) -> TwoLineElementRecordParsed:

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