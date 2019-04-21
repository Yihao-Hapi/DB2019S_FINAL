DROP TABLE hospital;
DROP TABLE hospital_payment;
DROP TABLE hospital_comp;
DROP TABLE city;
DROP TABLE payment;
DROP TABLE complication;
DROP TABLE time_range;

DROP SCHEMA IF EXISTS hospital_project;
CREATE SCHEMA hospital_project;


CREATE TABLE hospital(
	providerID VARCHAR(255) PRIMARY KEY,
	hospitalName VARCHAR(255),
	address VARCHAR(255),
	zip VARCHAR(5), --refers to city table
	phone VARCHAR(255)
);

CREATE TABLE hospital_payment (
	providerID VARCHAR(255),
	paymentID VARCHAR(255),
	paymentAmount BIGINT, --"payment" column of value of care table
	payLow INT, --low estimate for procedure
	payHigh INT, --high estimate for procedure
	quantity INT, --the "denominator" column, or how many data points/subjects
	compare VARCHAR(255), --higher/neutral/lower than national avg
	UNIQUE (providerID, paymentID)
);


CREATE TABLE hospital_comp(
	providerID VARCHAR(255),
	measureID VARCHAR(255), --same as paymentID above, only 4 types
	compScore NUMERIC(5,2),--percent of patients with complications
	compLow NUMERIC(5,2), --low est
	compHigh NUMERIC(5,2), --high est
	quantity INT, --data points
	compare VARCHAR(255), --worse/neutral/better than national avg
	UNIQUE (providerID, measureID)
);

CREATE TABLE city(
	cityName VARCHAR(255),
	countyName VARCHAR(255),
	zip VARCHAR(5) PRIMARY KEY,
	stateName VARCHAR(2) --abbreviation
);

CREATE TABLE payment(
	paymentID VARCHAR(255) PRIMARY KEY,
	paymentDesc VARCHAR(255)
);

CREATE TABLE complication( --complications or deaths
	measureID VARCHAR(255) PRIMARY KEY,
	measureDesc VARCHAR(255)
);

/*
    The table is for checking hospital information with correct time measured
    so that data in 2 datasets are joined by correct time
*/
CREATE TABLE time_range
(
    dateStart TIMESTAMP,    -- overlapped time start : the later one (HAD TO TEMPORARILY SWITCH THESE
    						   -- PSYCOPG2 DOES NOT LIKE CONVERSIONS, NO SOLID CONVERSION TO SQL DATE TYPE FROM STRING)
    dateEnd TIMESTAMP,      -- overlapped time end: the earlier one
    providerID VARCHAR(255) PRIMARY KEY UNIQUE
);
