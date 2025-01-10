from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer


# Setup SQLite in-memory database and metadata
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
metadata = MetaData()

# Define the Person table
person = Table(
    "person",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50), nullable=False),
    Column("age", Integer),
)

# Create all tables
metadata.create_all(engine)

# Example: Insert data
with engine.connect() as conn:
    conn.execute(
        person.insert(),
        [
            {"name": "Alice", "age": 25},
            {"name": "Bob", "age": 30},
            {"name": "Charlie", "age": 35},
        ],
    )
    conn.commit()

# Example: Query data
with engine.connect() as conn:
    result = conn.execute(person.select()).fetchall()
    for row in result:
        print(row)



from sqlalchemy import text

# Example: Query using raw SQL
with engine.connect() as conn:
    sql = "SELECT * FROM person WHERE age > 30"
    result = conn.execute(text(sql))
    for row in result:
        print(row)
