CREATE TABLE IF NOT EXISTS cities (
    geonameid BIGINT PRIMARY KEY,
    name TEXT NOT NULL,
    name_fr TEXT,
    name_en TEXT,
    country_code TEXT,
    country_name TEXT,
    admin1_code TEXT,
    region TEXT,
    lat DOUBLE PRECISION NOT NULL,
    lon DOUBLE PRECISION NOT NULL,
    tz TEXT,
    feature_class TEXT,
    feature_code TEXT,
    population BIGINT DEFAULT 0,
    display_fr TEXT,
    display_en TEXT,
    search_text TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS city_aliases (
    id BIGSERIAL PRIMARY KEY,
    geonameid BIGINT NOT NULL REFERENCES cities(geonameid) ON DELETE CASCADE,
    alias TEXT NOT NULL,
    alias_norm TEXT NOT NULL,
    lang TEXT
);

CREATE INDEX IF NOT EXISTS idx_cities_search_text ON cities(search_text);
CREATE INDEX IF NOT EXISTS idx_cities_country_name ON cities(country_name);
CREATE INDEX IF NOT EXISTS idx_cities_population ON cities(population DESC);

CREATE INDEX IF NOT EXISTS idx_city_aliases_alias_norm ON city_aliases(alias_norm);
CREATE INDEX IF NOT EXISTS idx_city_aliases_geonameid ON city_aliases(geonameid);
