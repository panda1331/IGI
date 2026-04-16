"""
Task 6. Module for Library service.
"""
import pandas as pd
from IPython.core.display_functions import display

class LibService:
    """Service for weather dataset analysis."""
    def __init__(self):
        """Initialize and load weather dataset."""
        self.__data = self._read_file()

    @staticmethod
    def _read_file():
        """
        Read weather dataset from CSV file.

        Returns:
            pd.DataFrame: Loaded weather data
        """
        data = pd.read_csv("task6/weatherHistory.csv")
        return data

    def select_first_records(self, num_of_records: int):
        """
        Select first N records at 12:00 PM showing temperature and humidity.

        Args:
            num_of_records: Number of records to display
        """
        data = self.__data.copy()
        data["Formatted Date"] = pd.to_datetime(data["Formatted Date"], utc=True)
        data.index = data["Formatted Date"].dt.day_name()
        mask = data["Formatted Date"].dt.hour == 12
        filtered_data = data[mask].head(num_of_records)
        display(filtered_data[["Temperature (C)", "Humidity"]])

    def statistical_analysis(self):
        """
        Perform decile analysis: compare average temperature of hottest days
        (above 90th percentile) vs coldest days (below 10th percentile).

        Prints ratio of hot mean to cold mean.
        """
        temperatures = self.__data["Temperature (C)"]
        quant_10 = temperatures.quantile(0.1)
        quant_90 = temperatures.quantile(0.9)

        cold_temps = temperatures[temperatures <= quant_10]
        cold_mean = cold_temps.mean()
        hot_temps = temperatures[temperatures >= quant_90]
        hot_mean = hot_temps.mean()
        display(f"Average temperature on hottest days is higher than on coldest days (quantile_90 / quantile_10) in: {round(hot_mean / abs(cold_mean), 2)}")