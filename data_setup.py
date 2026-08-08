import sqlite3

# Connect to SQLite (this automatically creates 'analytics.db' if it doesn't exist)
conn = sqlite3.connect('analytics.db')
cursor = conn.cursor()

# Create a sample sales table
cursor.execute('''
CREATE TABLE IF NOT EXISTS sales (
    order_id INTEGER PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    revenue REAL,
    order_date DATE
)
''')

# Clear old data if re-running
cursor.execute('DELETE FROM sales')

# Insert sample dataset
sample_data = [
    ('Laptop Pro', 'Electronics', 1200.00, '2026-01-15'),
    ('Wireless Mouse', 'Electronics', 25.50, '2026-01-16'),
    ('Office Chair', 'Furniture', 250.00, '2026-01-20'),
    ('Desk Lamp', 'Furniture', 45.00, '2026-02-01'),
    ('Monitor 4K', 'Electronics', 450.00, '2026-02-10'),
    ('Standing Desk', 'Furniture', 550.00, '2026-02-15'),
    ('USB-C Cable', 'Electronics', 15.00, '2026-02-18')
]

cursor.executemany('''
INSERT INTO sales (product_name, category, revenue, order_date) VALUES (?, ?, ?, ?)
''', sample_data)

conn.commit()
conn.close()

print("Database 'analytics.db' created successfully with sample data!")