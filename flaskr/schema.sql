DROP TABLE IF EXISTS iris;
DROP TYPE IF EXISTS iris_species;

CREATE TYPE iris_species AS ENUM (
    'setosa',
    'virginica',
    'versicolor'
);

CREATE TABLE iris (
    id SERIAL PRIMARY KEY,
    sepal_length REAL NOT NULL,
    sepal_width REAL NOT NULL,
    petal_length REAL NOT NULL,
    petal_width REAL NOT NULL,
    species iris_species NOT NULL,
    sepal_ratio REAL NOT NULL,
    petal_ratio REAL NOT NULL
);
