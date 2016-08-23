"""Library of miscellaneous charting classes."""

import time


class TimeStamp(object):
    """Calculates the timestamps for predefined chart timeframes."""

    def __init__(self):
        """Instantiate the class.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        self.presets = [1800, 3600, 10800, 18000, 28800, 43200]
        self.descriptions = [
            'Five Minute', 'Thirty Minute', 'One Hour',
            'Three Hours', 'Eight Hours', 'Twelve Hours']
        self.id_labels = ['five-minute', 'thirty-minute', 'one-hour',
            'three-hours', 'eight-hours', 'twelve-hours']
        self._process()

    def _process(self):
        """Process the data.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        now = int(time.time()) - 300
        self.start_times = []
        self.stop_times = []

        # Process data. Create lists of start/stop times and descriptions
        for timestamp in self.presets:
            start = now - timestamp
            self.start_times.append(start)
            self.stop_times.append(now)
        self.times = zip(self.start_times, self.stop_times, self.descriptions, self.id_labels)

    def get_times(self):
        """Return chart duration data.

        Args:
            None

        Returns:
            value: tuple of lists of (start times, stop times, descriptions)
                for each timeframe of chart

        """
        # Return
        value = self.times
        return value
