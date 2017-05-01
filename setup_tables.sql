CREATE DATABASE voiceassist;

CREATE TABLE Requests (
    id SERIAL PRIMARY KEY,
    patient_id varchar(50) NOT NULL,
    ts_request timestamp DEFAULT LOCALTIMESTAMP,
    ts_pickup timestamp,
    ts_close timestamp,
    transcription text,
    status varchar(10) CHECK (status = 'OPEN' OR status = 'INPROGRESS' OR status = 'CLOSED'),
    priority_score real
);

CREATE TABLE Patients (
	id varchar(50) NOT NULL PRIMARY KEY,
	name text,
	room_no varchar(10)
);
