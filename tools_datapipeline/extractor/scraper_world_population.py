
import pandas as pd
import requests
from bs4 import BeautifulSoup
import tools_datapipeline.base.extractor as extractor 
import tools_datapipeline.base.exceptions as exceptions
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame 

class ScrapperWorldPopulation(extractor.Extractor):

    def __init__(self,url:str,sparksession:SparkSession)->None:
        """
        Metodo constructor

        Args:
            url (str): url de la pagina para scrappear
            sparksession (SparkSession): sparksession , 
                                         para construir el dataframe a futuro
        """
        self._url = url
        self._parameter_validation()
        self._perform_to_authentication()
        self._sparksession = sparksession

    def _parameter_validation(self)->None:
        """
        Metodo que permite hace una validacion
        del tipo de dato que se para como parametro 
        en el formato de evitar errores a futuro

        Raises:
            exceptions.ExtractorErrorType
        """
        if not isinstance(self._url,str):
            raise exceptions.ExtractorErrorType("El tipo de dato es incorrecto")
    
    def _perform_to_authentication(self)->None:
        """
        Metodo que permite hace una validacion
        del request a la pagina

        Raises:
            exceptions.ExtractorErrorAuthentication
        """
        self._req = requests.get(self._url)
        
        if self._req.status_code != 200:
            raise exceptions.ExtractorErrorAuthentication("El request a la página no fue exitoso")
    
    def extract_data_from_source(self)->DataFrame:
        """
        Metodo que te permite extraer la informacion
        del request , con la librería BeautifulSoup
        para posteriormente , cargarlo en un dataframe de spark
        para poder llevar a cabo en paso posteriores la limpieza 
        con el framework

        Returns:
            DataFrame: Spark Dataframe
        """
        soup = BeautifulSoup(self._req.text)
        data = soup.find_all("table")[0]
        df_population = pd.read_html(str(data))[0]
        df_spark = self._sparksession.createDataFrame(df_population)

        return df_spark


