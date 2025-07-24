USE DATABASE SNOWFLAKE_LEARNING_DB;



CREATE OR REPLACE SCHEMA STAGGING;
CREATE OR REPLACE SCHEMA RAW;
CREATE OR REPLACE SCHEMA TRANSFORMED;
CREATE OR REPLACE SCHEMA CURATED;


USE SCHEMA SNOWFLAKE_LEARNING_DB.STAGGING;
SHOW SCHEMAS IN DATABASE SNOWFLAKE_LEARNING_DB;


CREATE OR REPLACE TABLE SNOWFLAKE_LEARNING_DB.STAGGING.COVID_STATS_2022(
date_updated date,
last_update_timestamp timestamp_LTZ,
confirmed number,
confirmed_diff number,
deaths number,
deaths_diff number,
recovered number,
recovered_diff number,
active number,
active_diff number,
fatality_rate float,
country_iso_code varchar
);


CREATE OR REPLACE TABLE SNOWFLAKE_LEARNING_DB.STAGGING.ISO_COUNTRY_CODE(
country_iso_code varchar,
country_name varchar
);


CREATE OR REPLACE TABLE SNOWFLAKE_LEARNING_DB.RAW._COUNTRY_CODE(
country_iso_code varchar(3),
country_name varchar(25)
);


--Create Storage Integration
CREATE OR REPLACE STORAGE INTEGRATION SNOWPARK_INT
TYPE = EXTERNAL_STAGE
STORAGE_PROVIDER = 'S3'
ENABLED = TRUE
STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::442426867609:role/snowfalke_snowpark_role'
--STORAGE_ALLOWED_LOCATIONS = ('s3://covid-19-api-data/covid-data/','s3://covid-19-api-data/regions/');
STORAGE_ALLOWED_LOCATIONS = ('s3://covid-19-api-data/');


DESC INTEGRATION SNOWPARK_INT;



--Create a stage in Snowflake
CREATE OR REPLACE STAGE SNOWFLAKE_LEARNING_DB.STAGGING.SNOWPARK_STAGE
STORAGE_INTEGRATION = SNOWPARK_INT
URL = 's3://covid-19-api-data/covid-data/';

--To verify Stage Integration is set up successfully
ls @SNOWFLAKE_LEARNING_DB.STAGGING.SNOWPARK_STAGE;

CREATE OR REPLACE STAGE SNOWFLAKE_LEARNING_DB.STAGGING.REGIONS_STAGE
STORAGE_INTEGRATION = SNOWPARK_INT
URL = 's3://covid-19-api-data/regions/';

--To verify Stage Integration is set up successfully
ls @SNOWFLAKE_LEARNING_DB.STAGGING.REGIONS_STAGE;

