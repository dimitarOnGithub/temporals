
class TimeAmbiguityError(Exception):
    pass


class NonexistentTimeError(TimeAmbiguityError):

    def __init__(self, dt_value, timezone):
        super().__init__(f"Time={dt_value} is nonexistent in the {timezone} timezone due to daylight savings shift")
