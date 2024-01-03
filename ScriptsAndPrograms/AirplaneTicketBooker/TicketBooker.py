import customtkinter as ctk
from tkcalendar import Calendar
import mysql.connector

window = ctk.CTk()
window.title("Atlas: Your Gateway to the World")
window.geometry('920x570')


def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            database='airport'
        )
        return connection
    except mysql.connector.Error as error:
        print("Error connecting to MySQL:", error)
        return None


def fetch_cities():
    connection = connect_to_database()
    if connection is not None:
        try:
            cursor = connection.cursor()
            query = "SELECT city_name FROM cities ORDER BY city_name"
            cursor.execute(query)
            cities = [row[0] for row in cursor.fetchall()]
            cities.insert(0, "Choose a city")  # Adding default option
            return cities
        except mysql.connector.Error as error:
            print("Error fetching cities from MySQL table:", error)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")
    return ["Choose a city"]


cities = fetch_cities()

dep_city_var = ctk.StringVar()
label = ctk.CTkLabel(window, text="I am departing from:")
label.pack(anchor='w', padx=(60, 0))
dep_city_var.set(cities[0])  # Set the default city
dep_city_dropdown = ctk.CTkOptionMenu(window, variable=dep_city_var, values=cities)
dep_city_dropdown.pack(anchor='w', padx=(60, 0))

arrival_city_var = ctk.StringVar()
label = ctk.CTkLabel(window, text="I'd like to go to:")
label.pack(anchor='w', padx=(60, 0))
arrival_city_var.set(cities[0])  # Set the default city
arrival_city_dropdown = ctk.CTkOptionMenu(window, variable=arrival_city_var, values=cities)
arrival_city_dropdown.pack(anchor='w', padx=(60, 0))

# Create and pack the departure date calendar
dep_calendar_label = ctk.CTkLabel(window, text="Select your departure date:")
dep_calendar_label.pack(anchor='w', padx=(45, 0))
dep_calendar = Calendar(window)
dep_calendar.pack(anchor='w', padx=(20, 0))

# Create and pack the return date calendar
ret_calendar_label = ctk.CTkLabel(window, text="Select your return date:")
ret_calendar_label.pack(anchor='w', padx=(60, 0))
ret_calendar = Calendar(window)
ret_calendar.pack(anchor='w', padx=(20, 0))


def get_user_selection():
    dep_city_selection = dep_city_var.get()
    arrival_city_selection = arrival_city_var.get()

    departure_date = dep_calendar.get_date()
    return_date = ret_calendar.get_date()

    print("Departure City:", dep_city_selection)
    print("Arrival City:", arrival_city_selection)
    print("Departure Date:", departure_date)
    print("Return Date:", return_date)


button = ctk.CTkButton(window, text="Get User Selection", command=get_user_selection)
button.pack(anchor='w', padx=(60, 0), pady=(20, 0))

window.mainloop()
