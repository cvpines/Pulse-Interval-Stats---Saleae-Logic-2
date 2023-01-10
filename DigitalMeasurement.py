import math

from saleae.range_measurements import DigitalMeasurer

MEASUREMENT_COUNT = 'count'
MEASUREMENT_MIN = 'min'
MEASUREMENT_MEAN = 'mean'
MEASUREMENT_MAX = 'max'
MEASUREMENT_STDDEV = 'stddev'
MEASUREMENT_POLARITY = 'polarity'

class IntervalStatsMeasurer(DigitalMeasurer):
    """Calculates stats for pulse intervals."""

    supported_measurements = [MEASUREMENT_COUNT, MEASUREMENT_MIN, MEASUREMENT_MEAN, MEASUREMENT_MAX, MEASUREMENT_STDDEV, MEASUREMENT_POLARITY]

    def __init__(self, requested_measurements):
        super().__init__(requested_measurements)

        self.intervals = []
        self.target_state = None
        self.pulse_start = None

    def process_data(self, data):
        for t, state in data:

            # Determine target state
            if self.target_state is None:
                self.target_state = state

            # A pulse is beginning
            if state == self.target_state:
                self.pulse_start = t
                continue

            # A pulse is ending
            delta = float(t - self.pulse_start)
            self.intervals.append(delta)

    # This method is called after all the relevant data has been passed to `process_data`
    # It returns a dictionary of the request_measurements values
    def measure(self):
        icount = len(self.intervals)
        isum = 0
        imin = None
        imax = None
        imean = None
        istd = None

        for interval in self.intervals:
            isum += interval

            if imin is None or interval < imin:
                imin = interval

            if imax is None or interval > imax:
                imax = interval

    
        if icount > 0:
            imean = isum / icount
            istd = math.sqrt(sum((x - imean) * (x - imean) for x in self.intervals) / icount)


        values = {}
        return {
            MEASUREMENT_COUNT: icount,
            MEASUREMENT_MIN: imin or 0,
            MEASUREMENT_MEAN: imean or 0,
            MEASUREMENT_MAX: imax or 0,
            MEASUREMENT_STDDEV: istd or 0,
            MEASUREMENT_POLARITY: self.target_state or 0
        }
