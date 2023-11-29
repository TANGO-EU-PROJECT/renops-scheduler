class ipinfo:
    url = "https://ipinfo.io/json"


class geocoder:
    url = "https://nominatim.openstreetmap.org"


class renopsapi:
    # Test endpoint
    # renewable_potential = "http://127.0.0.1:8000/v1/forecast/renewable_potential"
    renewable_potential = "https://renops-api-tango.xlab.si/v1/forecast/renewable_potential"
    key = "V2_DEV_BASIC_ACCESS_KEY"


class runtime:
    verbose = False
    sleep_seconds = 10

    @classmethod
    def set_verbose(cls, value):
        cls.verbose = value
