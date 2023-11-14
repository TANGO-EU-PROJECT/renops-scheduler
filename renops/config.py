class endpoint:
    renops = "https://renops-api-tango.xlab.si/forecast/renewable_potential"
    geocoder = "https://ipinfo.io/json"


class runtime:
    verbose = False
    sleep_seconds = 10

    @classmethod
    def set_verbose(cls, value):
        cls.verbose = value
