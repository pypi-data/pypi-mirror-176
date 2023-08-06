
CREATE TABLE IF NOT EXISTS "Subject" (
    "Identifier" VARCHAR(512) PRIMARY KEY,
    "Species" VARCHAR(512),
    "Sex" VARCHAR(512),
    "Birth date" VARCHAR,
    "Death date" VARCHAR,
    "Cause of death" VARCHAR
);

CREATE TABLE IF NOT EXISTS "Diagnosis" (
    "Subject" VARCHAR(512) REFERENCES "Subject"("Identifier"),
    "Condition" VARCHAR,
    "Result" VARCHAR(512),
    "Assessor" VARCHAR(512),
    "Date" VARCHAR
);

CREATE TABLE IF NOT EXISTS "Diagnostic selection criterion" (
    "Identifier" VARCHAR(512) PRIMARY KEY,
    "Condition" VARCHAR(512),
    "Result" VARCHAR(512)
);

CREATE TABLE IF NOT EXISTS "Specimen collection study" (
    "Name" VARCHAR(512) PRIMARY KEY,
    "Extraction method" VARCHAR(512),
    "Preservation method" VARCHAR(512),
    "Storage location" VARCHAR,
    "Inception date" VARCHAR,
    "Conclusion date" VARCHAR
);

CREATE TABLE IF NOT EXISTS "Specimen collection process" (
    "Specimen" VARCHAR PRIMARY KEY,
    "Source" VARCHAR,
    "Source site" VARCHAR,
    "Source age" VARCHAR,
    "Extraction date" VARCHAR(512),
    "Study" VARCHAR(512) REFERENCES "Specimen collection study"("Name")
);

CREATE TABLE IF NOT EXISTS "Histology assessment process" (
    "Slide" VARCHAR(512) REFERENCES "Specimen collection process"("Specimen"),
    "Assay" VARCHAR(512),
    "Result" VARCHAR(512),
    "Assessor" VARCHAR,
    "Assessment date" VARCHAR(512)
);

CREATE TABLE IF NOT EXISTS "Specimen measurement study" (
    "Name" VARCHAR(512) PRIMARY KEY,
    "Assay" VARCHAR(512),
    "Machine" VARCHAR(512),
    "Software" VARCHAR(512),
    "Inception date" VARCHAR,
    "Conclusion date" VARCHAR
);

CREATE TABLE IF NOT EXISTS "Specimen data measurement process" (
    "Identifier" VARCHAR(512) PRIMARY KEY,
    "Specimen" VARCHAR(512) REFERENCES "Specimen collection process"("Specimen"),
    "Specimen age" VARCHAR,
    "Date of measurement" VARCHAR(512),
    "Study" VARCHAR(512) REFERENCES "Specimen measurement study"("Name")
);

CREATE TABLE IF NOT EXISTS "Data file" (
    "SHA256 hash" VARCHAR(512) PRIMARY KEY,
    "File name" VARCHAR(512),
    "File format" VARCHAR(512),
    "Contents format" VARCHAR(512),
    "Size" VARCHAR(512),
    "Source generation process" VARCHAR(512) REFERENCES "Specimen data measurement process"("Identifier")
);

CREATE TABLE IF NOT EXISTS "Histological structure" (
    "Identifier" VARCHAR(512) PRIMARY KEY,
    "Anatomical entity" VARCHAR(512)
);

CREATE TABLE IF NOT EXISTS "Shape file" (
    "Identifier" VARCHAR(512) PRIMARY KEY,
    "Geometry specification file format" VARCHAR(512),
    "Base64 contents" VARCHAR
);

CREATE TABLE IF NOT EXISTS "Plane coordinates reference system" (
    "Name" VARCHAR(512) PRIMARY KEY,
    "Reference point" VARCHAR,
    "Reference point coordinate 1" NUMERIC,
    "Reference point coordinate 2" NUMERIC,
    "Reference orientation" VARCHAR,
    "Length unit" VARCHAR
);

CREATE TABLE IF NOT EXISTS "Histological structure identification" (
    "Histological structure" VARCHAR(512) REFERENCES "Histological structure"("Identifier"),
    "Data source" VARCHAR(512) REFERENCES "Data file"("SHA256 hash"),
    "Shape file" VARCHAR(512) REFERENCES "Shape file"("Identifier"),
    "Plane coordinates reference" VARCHAR(512) REFERENCES "Plane coordinates reference system"("Name"),
    "Identification method" VARCHAR(512),
    "Identification date" VARCHAR(512),
    "Annotator" VARCHAR
);

CREATE TABLE IF NOT EXISTS "Chemical species" (
    "Identifier" VARCHAR(512) PRIMARY KEY,
    "Symbol" VARCHAR,
    "Name" VARCHAR(512),
    "Chemical structure class" VARCHAR(512)
);

CREATE TABLE IF NOT EXISTS "Expression quantification" (
    "Histological structure" VARCHAR(512) REFERENCES "Histological structure"("Identifier"),
    "Target" VARCHAR(512) REFERENCES "Chemical species"("Identifier"),
    "Quantity" NUMERIC,
    "Unit" VARCHAR(512),
    "Quantification method" VARCHAR(512),
    "Discrete value" VARCHAR(512),
    "Discretization method" VARCHAR(512)
);

CREATE TABLE IF NOT EXISTS "Biological marking system" (
    "Identifier" VARCHAR(512) PRIMARY KEY,
    "Target" VARCHAR(512) REFERENCES "Chemical species"("Identifier"),
    "Antibody" VARCHAR,
    "Marking mechanism" VARCHAR(512),
    "Study" VARCHAR(512) REFERENCES "Specimen measurement study"("Name")
);

CREATE TABLE IF NOT EXISTS "Data analysis study" (
    "Name" VARCHAR(512) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS "Cell phenotype" (
    "Identifier" VARCHAR(512) PRIMARY KEY,
    "Symbol" VARCHAR,
    "Name" VARCHAR(512)
);

CREATE TABLE IF NOT EXISTS "Cell phenotype criterion" (
    "Cell phenotype" VARCHAR(512) REFERENCES "Cell phenotype"("Identifier"),
    "Marker" VARCHAR(512) REFERENCES "Chemical species"("Identifier"),
    "Polarity" VARCHAR(512),
    "Study" VARCHAR(512) REFERENCES "Data analysis study"("Name")
);

CREATE TABLE IF NOT EXISTS "Feature specification" (
    "Identifier" VARCHAR(512) PRIMARY KEY,
    "Derivation method" VARCHAR(512),
    "Study" VARCHAR(512) REFERENCES "Data analysis study"("Name")
);

CREATE TABLE IF NOT EXISTS "Feature specifier" (
    "Feature specification" VARCHAR(512) REFERENCES "Feature specification"("Identifier"),
    "Specifier" VARCHAR(512),
    "Ordinality" VARCHAR(512)
);

CREATE TABLE IF NOT EXISTS "Quantitative feature value" (
    "Identifier" VARCHAR(512) PRIMARY KEY,
    "Feature" VARCHAR(512) REFERENCES "Feature specification"("Identifier"),
    "Subject" VARCHAR,
    "Value" NUMERIC
);

CREATE TABLE IF NOT EXISTS "Two-cohort feature association test" (
    "Selection criterion 1" VARCHAR(512) REFERENCES "Diagnostic selection criterion"("Identifier"),
    "Selection criterion 2" VARCHAR(512) REFERENCES "Diagnostic selection criterion"("Identifier"),
    "Test" VARCHAR(512),
    "p-value" NUMERIC,
    "Feature tested" VARCHAR(512) REFERENCES "Feature specification"("Identifier")
);
