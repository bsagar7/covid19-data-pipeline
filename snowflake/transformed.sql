--Dropped difference columns as they are calculated on daily basis, we are analysing monthly data.
CREATE OR REPLACE TABLE SNOWFLAKE_LEARNING_DB.TRANSFORMED.COVID_STATS_2022_FINAL (
	COUNTRY_ISO_CODE VARCHAR(3),
	COUNTRY_NAME VARCHAR(35),
	CONFIRMED NUMBER(38,0),
	DEATHS NUMBER(38,0),
	RECOVERED NUMBER(38,0),
	ACTIVE NUMBER(38,0),
	FATALITY_RATE FLOAT,
    DATE_UPDATED DATE,
	LAST_UPDATE_TIMESTAMP TIMESTAMP_LTZ(9)
);


TRUNCATE TABLE SNOWFLAKE_LEARNING_DB.TRANSFORMED.COVID_STATS_2022_FINAL;



INSERT INTO SNOWFLAKE_LEARNING_DB.TRANSFORMED.COVID_STATS_2022_FINAL
SELECT 
    cs.COUNTRY_ISO_CODE,
    iso.COUNTRY_NAME,
    cs.CONFIRMED,
    cs.DEATHS,
    cs.RECOVERED, 
    cs.ACTIVE,
    cs.FATALITY_RATE, 
    cs.DATE_UPDATED,
    cs.LAST_UPDATE_TIMESTAMP
    FROM SNOWFLAKE_LEARNING_DB.RAW.COVID_STATS_2022 cs
         LEFT JOIN SNOWFLAKE_LEARNING_DB.RAW.ISO_COUNTRY_CODE iso
           ON cs.country_iso_code = iso.country_iso_code;


SELECT * FROM SNOWFLAKE_LEARNING_DB.TRANSFORMED.COVID_STATS_2022_FINAL LIMIT 5;