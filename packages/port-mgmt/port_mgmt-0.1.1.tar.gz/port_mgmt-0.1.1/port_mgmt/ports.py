import threading
import pandas as pd
import numpy as np
from scipy.spatial import cKDTree
from geopandas import GeoDataFrame
from shapely.geometry import Point
from shapely.ops import nearest_points
__EXCEL_DATA__='port_mgmt/data/port_data.xlsx'

class Port:
    __instance = None
    __lock = threading.Lock()
    __geodataframe = None
    __btree = None
    __use_BTREE = False

    def __new__(cls, *args, **kwargs):
        """ override ___new__ to make this class a singltone class so that only one instance of the class will be created.
        In case of not using multi-threading you can comment the related code to increase performance.

        Returns:
            Port: The only instance of the Port class will be returned.
        """
        if not cls.__instance:
            with cls.__lock:
                if not cls.__instance:
                    cls.__instance = super(Port, cls).__new__(cls)
        return cls.__instance

    def get_geodataframe(self):
        return self.__geodataframe

    @staticmethod
    def getInstance():
        if Port.__instance == None:
            Port()
        return Port.__instance

    def __init__(self, use_BTREE=False) -> None:
        self.__use_BTREE = use_BTREE
        if Port.__instance == None:
            Port.__instance = self
        if self.__geodataframe == None:
            self.__geodataframe = self.load_data()

    def load_data(self):
        """This function loads excel data prepared by Bailey Lab team and generate geometry for geopandas to work with the locations

        Returns:
            geoDataframe: a geodataframe generated from excel file that contains geomentry column
        """

        xls_file = pd.ExcelFile(
            __EXCEL_DATA__)
        ports_dataframe = pd.read_excel(xls_file, 'portdataSep2019')
        geometry = [Point(xy) for xy in zip(
            ports_dataframe.Longitude, ports_dataframe.Latitude)]
        ports_geodataframe = GeoDataFrame(
            ports_dataframe, crs="EPSG:4326", geometry=geometry)
        if self.__use_BTREE:
            nB = np.array(
                list(ports_geodataframe.geometry.apply(lambda x: (x.x, x.y))))
            self.__btree = cKDTree(nB)
        return ports_geodataframe

    def nearest_port(self, lat, lon):
        """ This function find the nearest port to (lat,lon) in the provided data

        Args:
            lat (int): Latitude of the point
            lon (int): longitude of the point

        Returns:
            array: the record of the nearest port
        """
        location = Point(lat, lon)
        nearest = nearest_points(
            location, self.__geodataframe.geometry.unary_union)
        return self.__geodataframe.loc[self.__geodataframe.geometry == nearest[1]]

    def nearest_port2(self, lat, lon):
        if self.__use_BTREE:
            location = Point(lat, lon)
            nearest = self.nearest_point_faster(
                location, self.__geodataframe)
            return self.__geodataframe.loc[self.__geodataframe.geometry == nearest]
        else:
            # print("use shapely nearest point function")
            return self.nearest_port( lat, lon)
        

    def nearest_point_faster(self, location, gdf1):
        """using clustering to improve speed; experiment does not show a big difference

        Args:
            location (Point): the point searching
            gdf1 (GeoDataFrame): dataframe of all ports

        Returns:
            [port]: nearest port
        """
        gpd2 = GeoDataFrame([['Current Port', location]],
                            columns=['location', 'geometry'])
        x = self.ckdnearest(gpd2, gdf1)

        # print('x:',Point(x.iloc[0].Latitude,x.iloc[0].Longitude))
        return Point(x.iloc[0].Longitude, x.iloc[0].Latitude)

    def ckdnearest(self, gdA, gdB):
        assert self.__use_BTREE,"set use_BTREE to True"

        nA = np.array(list(gdA.geometry.apply(lambda x: (x.x, x.y))))
        # # print("nA:",nA)
        # nB = np.array(list(gdB.geometry.apply(lambda x: (x.x, x.y))))
        # # print("nB:",nB)
        #  = cKDTree(nB)
        dist, idx = self.__btree.query(nA, k=1)
        print(dist, idx, gdB.iloc[idx])
        # gdB_nearest = gdB.iloc[idx].drop(columns="geometry").reset_index(drop=True)
        # gdf = pd.concat(
        #     [
        #         gdA.reset_index(drop=True),
        #         gdB_nearest,
        #         pd.Series(dist, name='dist')
        #     ],
        #     axis=1)

        return gdB.iloc[idx]  # gdf

    def env_factors(self, lat, lon):
        """ This function returns the environmental factors of the nearest port to (lat,lon) 

        Args:
            lat (int): Latitude of the point
            lon (int): longitude of the point

        Returns:
            array: an array with environmental variables [Minimum Tempreature, Max Temperature, Annual Temperature, Salinity]
        """
        yp = self.nearest_port(lat, lon)
        yp = np.ravel(
            np.array([yp['Min Temp'], yp['Max Temp'], yp['Annual Temp'], yp['Salinity']]))
        return yp

    def env_distance(self, p1, p2):
        """ Returns the environmental distance between two point p1 and p2

        Args:
            p1 (tuple): point with (lat, lon)
            p2 (tuple): point with (lat, lon)

        Returns:
            float: returns the environmental distance between the nearest port to p1 and the nearest port to p2
        """
        (lat1, lon1) = p1
        (lat2, lon2) = p2
        point1 = self.env_factors(lat1, lon1)
        point2 = self.env_factors(lat2, lon2)
        return np.round(np.sqrt(np.sum(np.power(point1-point2, 2))), 3)
