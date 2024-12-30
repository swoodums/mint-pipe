This is a learning project.  I will be using FastAPI to build some endpoints that consume data, transform it, and output it to a JSON.

The end objective is to have a whole data pipeline built out to learn a slew of data engineering skills.

The data is coming from a public API found on https://api.nasa.gov/.  The actual API is https://tle.ivan.stanojevic.me/api/.
It is data for earth-orbiting objects at a given point in time.  It provides two-line element set records, updated daily from
CelesTrak and served as a JSON.  A two-line element is a data format encoding a lsit of orbital elements of an earth-orbiting
object for a given point in time.

We will be extracting the data for each element and flattening the data, so we have one row per object, with the data types
defined.  This ensures we have a predicatable schema, and the API will perform data validation.