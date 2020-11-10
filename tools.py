from dd import dd
from dd_store import dd_store
from geocode import geocode
from go import go
from light_week_report import light_week_report
from pc_interpolation import pc_interpolation
from prorate import prorate
from mobile_error_analysis import mobileErrorAnalysis


class Tools:
    geo_tools = {
                "DriveDistance" : dd,
                "DriveDistanceStore" : dd_store,
                "GrandOpening" : go,
                "Geocode": geocode,
                "LightWeekReport" : light_week_report,
                "MobileErrorAnalysis" : mobileErrorAnalysis,
                "PcInterpolation" : pc_interpolation,
                "Prorate" : prorate
                }

    def __init__(self):
        self.toolbox = {
                "DriveDistance" : dd,
                "DriveDistanceStore" : dd_store,
                "GrandOpening" : go,
                "Geocode": geocode,
                "LightWeekReport" : light_week_report,
                "MobileErrorAnalysis" : mobileErrorAnalysis,
                "PcInterpolation" : pc_interpolation,
                "Prorate" : prorate
                }



