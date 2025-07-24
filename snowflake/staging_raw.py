# The Snowpark package is required for Python Worksheets. 
# You can add more packages by selecting them using the Packages control and then importing them.

import snowflake.snowpark as snowpark
from snowflake.snowpark.functions import length, col
#from snowflake.snowpark.functions import col

def main(session: snowpark.Session): 

    session.sql('USE SCHEMA SNOWFLAKE_LEARNING_DB.STAGGING').collect()


    session.sql('TRUNCATE TABLE SNOWFLAKE_LEARNING_DB.STAGGING.COVID_STATS_2022').collect()
    session.sql('TRUNCATE TABLE SNOWFLAKE_LEARNING_DB.STAGGING.ISO_COUNTRY_CODE').collect()

    # Load the files data to stagging table

    session.sql('''COPY INTO SNOWFLAKE_LEARNING_DB.STAGGING.COVID_STATS_2022
                FROM @SNOWFLAKE_LEARNING_DB.STAGGING.SNOWPARK_STAGE/monthly_summary_2025-07-11_22-05-27.csv
                FILE_FORMAT = (TYPE = CSV SKIP_HEADER = 1 FIELD_OPTIONALLY_ENCLOSED_BY = '"')''').collect()
    
    session.sql('''COPY INTO SNOWFLAKE_LEARNING_DB.STAGGING.ISO_COUNTRY_CODE
                FROM @SNOWFLAKE_LEARNING_DB.STAGGING.REGIONS_STAGE/iso_country_code_2025-07-16_01-13-26.csv
                FILE_FORMAT = (TYPE = CSV SKIP_HEADER = 1 FIELD_OPTIONALLY_ENCLOSED_BY = '"')''').collect()


    # Load the data from staging area to raw area
    # Creating Raw table Dataframe
    df_covid_stats_2022_read = session.sql('''SELECT 
                                            DATE_UPDATED,  
                                            LAST_UPDATE_TIMESTAMP,  
                                            CONFIRMED,  
                                            CONFIRMED_DIFF,  
                                            DEATHS,  
                                            DEATHS_DIFF,  
                                            RECOVERED,  
                                            RECOVERED_DIFF,  
                                            ACTIVE,  
                                            ACTIVE_DIFF,  
                                            FATALITY_RATE,  
                                            COUNTRY_ISO_CODE FROM SNOWFLAKE_LEARNING_DB.STAGGING.COVID_STATS_2022''')

    df_covid_stats_2022_read.write.mode('overwrite').save_as_table('SNOWFLAKE_LEARNING_DB.RAW.COVID_STATS_2022')

    df_covid_stats_2022_read.show()


    
    df_iso_country_code_read = session.sql('''SELECT 
                                            COUNTRY_ISO_CODE,  
                                            COUNTRY_NAME FROM SNOWFLAKE_LEARNING_DB.STAGGING.ISO_COUNTRY_CODE''')
    df_iso_country_code_read.show()
    
    # Step 3: Filter rows where ISO_COUNTRY_CODE is exactly 3 characters long
    df_iso_country_code_read = df_iso_country_code_read.filter(length(col("COUNTRY_ISO_CODE")) == 3)

    
    df_iso_country_code_read.write.mode('overwrite').save_as_table('SNOWFLAKE_LEARNING_DB.RAW.ISO_COUNTRY_CODE')
    
    df_iso_country_code_read.show()
    #return dataframe