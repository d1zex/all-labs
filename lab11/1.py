import psycopg2
import pandas as pd
import json

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="phonebook_db",  # change if you use different db
    user="postgres",
    password="lolpopqwerty",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Create table if not exists
cur.execute("""
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(50),
        phone VARCHAR(15)
    )
""")
conn.commit()

def insert_from_console():
    first_name = input("Enter first name: ")
    phone = input("Enter phone number: ")
    cur.execute("INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)", (first_name, phone))
    conn.commit()
    print("Data inserted successfully!")

def insert_from_csv():
    path = input("Enter CSV file path: ")
    df = pd.read_csv(path)
    for _, row in df.iterrows():
        cur.execute("INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)", (row['first_name'], row['phone']))
    conn.commit()
    print("CSV data inserted successfully!")

def update_entry():
    print("1. Update name\n2. Update phone")
    choice = input("Choose option: ")
    if choice == "1":
        old_name = input("Current name: ")
        new_name = input("New name: ")
        cur.execute("UPDATE phonebook SET first_name = %s WHERE first_name = %s", (new_name, old_name))
    elif choice == "2":
        name = input("Name: ")
        new_phone = input("New phone: ")
        cur.execute("UPDATE phonebook SET phone = %s WHERE first_name = %s", (new_phone, name))
    conn.commit()
    print("Data updated successfully!")

def query_data():
    print("1. Show all\n2. Filter by name")
    choice = input("Choose option: ")
    if choice == "1":
        cur.execute("SELECT * FROM phonebook")
        rows = cur.fetchall()
    elif choice == "2":
        name = input("Enter name: ")
        cur.execute("SELECT * FROM phonebook WHERE first_name = %s", (name,))
        rows = cur.fetchall()
    else:
        print("Invalid option")
        return
    for row in rows:
        print(row)

def delete_entry():
    print("1. Delete by name\n2. Delete by phone")
    choice = input("Choose option: ")
    if choice == "1":
        name = input("Enter name to delete: ")
        cur.execute("DELETE FROM phonebook WHERE first_name = %s", (name,))
    elif choice == "2":
        phone = input("Enter phone to delete: ")
        cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
    conn.commit()
    print("Deleted successfully!")

# Function to return all records based on a pattern
def query_by_pattern():
    pattern = input("Enter pattern to search (name, surname, or phone): ")
    cur.execute("SELECT * FROM phonebook WHERE first_name ILIKE %s OR phone ILIKE %s", (f"%{pattern}%", f"%{pattern}%"))
    rows = cur.fetchall()
    for row in rows:
        print(row)

# Create procedure to insert or update user
cur.execute("""
    CREATE OR REPLACE PROCEDURE insert_or_update_user(name VARCHAR, phone VARCHAR)
    LANGUAGE plpgsql
    AS $$
    BEGIN
        IF EXISTS (SELECT 1 FROM phonebook WHERE first_name = name) THEN
            UPDATE phonebook SET phone = phone WHERE first_name = name;
        ELSE
            INSERT INTO phonebook (first_name, phone) VALUES (name, phone);
        END IF;
    END;
    $$;
""")
conn.commit()

# Call procedure to insert or update user
def insert_or_update_user():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    cur.execute("CALL insert_or_update_user(%s, %s)", (name, phone))
    conn.commit()
    print("User inserted or updated successfully!")

# Create procedure to insert many users
cur.execute("""
    CREATE OR REPLACE PROCEDURE insert_many_users(users JSONB)
    LANGUAGE plpgsql
    AS $$
    DECLARE
        user_record JSONB;
        invalid_users JSONB := '[]'::JSONB;
    BEGIN
        FOR user_record IN SELECT * FROM jsonb_array_elements(users) LOOP
            IF user_record->>'phone' ~ '^[0-9]+$' THEN
                INSERT INTO phonebook (first_name, phone)
                VALUES (user_record->>'name', user_record->>'phone')
                ON CONFLICT (first_name) DO UPDATE SET phone = EXCLUDED.phone;
            ELSE
                invalid_users := invalid_users || user_record;
            END IF;
        END LOOP;
        RAISE NOTICE 'Invalid users: %', invalid_users;
    END;
    $$;
""")
conn.commit()

# Call procedure to insert many users
def insert_many_users():
    while True:
        try:
            n = int(input("Enter number of users to insert: "))
            break  # Exit the loop if the input is valid
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    users = []
    for _ in range(n):
        name = input("Enter name: ")
        phone = input("Enter phone: ")
        users.append({"name": name, "phone": phone})
    cur.execute("CALL insert_many_users(%s::JSONB)", (json.dumps(users),))
    conn.commit()
    print("Users inserted successfully!")

# Create function for querying data with pagination
cur.execute("""
    CREATE OR REPLACE FUNCTION query_with_pagination(limit_val INT, offset_val INT)
    RETURNS TABLE(id INT, first_name VARCHAR, phone VARCHAR)
    LANGUAGE plpgsql
    AS $$
    BEGIN
        RETURN QUERY SELECT * FROM phonebook LIMIT limit_val OFFSET offset_val;
    END;
    $$;
""")
conn.commit()

# Call function for querying data with pagination
def query_with_pagination():
    limit = int(input("Enter limit: "))
    offset = int(input("Enter offset: "))
    cur.execute("SELECT * FROM query_with_pagination(%s, %s)", (limit, offset))
    rows = cur.fetchall()
    for row in rows:
        print(row)

# Create procedure to delete data by username or phone
cur.execute("""
    CREATE OR REPLACE PROCEDURE delete_by_username_or_phone(identifier VARCHAR)
    LANGUAGE plpgsql
    AS $$
    BEGIN
        DELETE FROM phonebook WHERE first_name = identifier OR phone = identifier;
    END;
    $$;
""")
conn.commit()

# Call procedure to delete data by username or phone
def delete_by_username_or_phone():
    identifier = input("Enter username or phone to delete: ")
    cur.execute("CALL delete_by_username_or_phone(%s)", (identifier,))
    conn.commit()
    print("Data deleted successfully!")

def main():
    while True:
        print("\nPhoneBook Menu:")
        print("1. Insert from console")
        print("2. Insert from CSV")
        print("3. Update entry")
        print("4. Query data")
        print("5. Delete entry")
        print("6. Query by pattern")
        print("7. Insert or update user")
        print("8. Insert many users")
        print("9. Query with pagination")
        print("10. Delete by username or phone")
        print("11. Exit")
        choice = input("Choose option: ")
        if choice == "1":
            insert_from_console()
        elif choice == "2":
            insert_from_csv()
        elif choice == "3":
            update_entry()
        elif choice == "4":
            query_data()
        elif choice == "5":
            delete_entry()
        elif choice == "6":
            query_by_pattern()
        elif choice == "7":
            insert_or_update_user()
        elif choice == "8":
            insert_many_users()
        elif choice == "9":
            query_with_pagination()
        elif choice == "10":
            delete_by_username_or_phone()
        elif choice == "11":
            break
        else:
            print("Invalid option")

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
