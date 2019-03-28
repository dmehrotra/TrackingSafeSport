CREATE TABLE coach(
	fullName varchar unique,
	regionLong varchar,
	city varchar,
	region varchar,
	sport varchar,
	hearingDate date,
	charge1 varchar,
	charge2 varchar,
	charge3 varchar,
	charge4 varchar,
	charge5 varchar,
	charge6 varchar,
	finding1 varchar,
	finding2 varchar,
	finding3 varchar,
	finding4 varchar,
	finding5 varchar,
	finding6 varchar,
	actions varchar,
 	created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  	updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
	adjudicatingBody varchar,
	checked bool default false

);


CREATE SCHEMA logging;

CREATE TABLE logging.t_history (
        id serial,
        tstamp timestamp DEFAULT now(),
        schemaname text,
        tabname text,
        operation text,
        who text DEFAULT current_user,
        new_val json,
        old_val json,
        checked bool default false
);
CREATE TABLE common_name(
	name varchar unique,
	checked bool default false
);

CREATE FUNCTION change_trigger() RETURNS trigger AS $$
        BEGIN
                IF TG_OP = 'INSERT'
                THEN
                    INSERT INTO logging.t_history (tabname, schemaname, operation, new_val)
                                VALUES (TG_RELNAME, TG_TABLE_SCHEMA, TG_OP, row_to_json(NEW));
                        RETURN NEW;
                ELSIF   TG_OP = 'UPDATE'
                THEN
                    INSERT INTO logging.t_history (tabname, schemaname, operation, new_val, old_val)
                            VALUES (TG_RELNAME, TG_TABLE_SCHEMA, TG_OP, row_to_json(NEW), row_to_json(OLD));

                        RETURN NEW;

                END IF;

        END;

$$ LANGUAGE 'plpgsql' SECURITY DEFINER;

CREATE OR REPLACE FUNCTION trigger_set_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER t BEFORE INSERT OR UPDATE OR DELETE ON coach
        FOR EACH ROW EXECUTE PROCEDURE change_trigger();