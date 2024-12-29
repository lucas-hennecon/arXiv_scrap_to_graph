CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    authors TEXT,
    year INT,
    arxiv_id VARCHAR(20),
    pdf_url TEXT
);

