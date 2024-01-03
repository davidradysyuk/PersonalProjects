import customtkinter as ctk
from tkcalendar import Calendar
import mysql.connector

window = ctk.CTk()
window.title("Atlas: Your Gateway to the World")
window.geometry('920x570')


def format_date(date_str):
    """Convert date from m/d/yy to yyyy-mm-dd format."""
    try:
        month, day, year = date_str.split('/')
        year = f"20{year}"  # Adjust for yy to yyyy
        return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
    except ValueError:
        print(f"Invalid date format: {date_str}")
        return None


def format_flight_info(flight):
    return (f"Flight ID: {flight[0]}, Flight Number: {flight[1]}, "
            f"Departure City: {flight[2]}, Arrival City: {flight[3]}, "
            f"Departure Date: {flight[4]}, Return Date: {flight[5]}, "
            f"Available Seats: {flight[6]}, Ticket Price: ${flight[7]:.2f}, "
            f"Departure Country: {flight[8]}, Arrival Country: {flight[9]}, "
            f"Departure from Origin Time: {flight[10]}, "
            f"Departure from Destination Time: {flight[11]}, "
            f"Arrival to Destination Time: {flight[12]}, "
            f"Arrival to Origin Time: {flight[13]}\n")


def show_flight_info(flight_info):
    flight_data = flight_info.split(', ')
    flight_number = flight_data[1].split(': ')[1]
    dep_city = flight_data[2].split(': ')[1]  # Extracting departure city
    arrival_city = flight_data[3].split(': ')[1]  # Extracting arrival city
    departure_date = flight_data[4].split(': ')[1]
    return_date = flight_data[5].split(': ')[1]
    available_seats = flight_data[6].split(': ')[1]
    dep_from_origin_time = flight_data[10].split(': ')[1]
    dep_from_dest_time = flight_data[11].split(': ')[1]
    arrival_to_dest_time = flight_data[12].split(': ')[1]
    arrival_to_origin_time = flight_data[13].split(': ')[1]

    info_text = (
        f"Your flight number is {flight_number},\n"
        f"it will depart on {departure_date} and return on {return_date}.\n"
        f"There are {available_seats} seat(s) left.\n\n"
        f"You will be leaving {dep_city} at {dep_from_origin_time} and arriving in {arrival_city} at {arrival_to_dest_time}.\n"
        f"You will leave {arrival_city} at {dep_from_dest_time} and come back home at {arrival_to_origin_time}.\n\n"
        f"Would you like to book this ticket?"
    )

    window = ctk.CTk()
    window.title("Flight Information")
    window.geometry('400x250')

    flight_textbox = ctk.CTkTextbox(window, state="normal", width=400, height=200)
    flight_textbox.grid(row=0, column=0, padx=0, pady=0)
    flight_textbox.insert("0.0", info_text)
    flight_textbox.configure(state="disabled")

    def book_ticket():
        booking_window = ctk.CTkToplevel(window)
        booking_window.title("Booking Details")
        booking_window.geometry("300x300")

        # Create and place input fields
        label_first_name = ctk.CTkLabel(booking_window, text="First Name:")
        label_first_name.pack()
        entry_first_name = ctk.CTkEntry(booking_window)
        entry_first_name.pack()

        label_last_name = ctk.CTkLabel(booking_window, text="Last Name:")
        label_last_name.pack()
        entry_last_name = ctk.CTkEntry(booking_window)
        entry_last_name.pack()

        label_email = ctk.CTkLabel(booking_window, text="Email:")
        label_email.pack()
        entry_email = ctk.CTkEntry(booking_window)
        entry_email.pack()

        label_phone = ctk.CTkLabel(booking_window, text="Phone Number:")
        label_phone.pack()
        entry_phone = ctk.CTkEntry(booking_window)
        entry_phone.pack()

        def confirm_booking():
            # Extract user input
            first_name = entry_first_name.get()
            last_name = entry_last_name.get()
            email = entry_email.get()
            phone = entry_phone.get()

            # Add logic to validate and store the input data

            print("Booking Confirmed")  # Placeholder for confirmation logic
            booking_window.destroy()

        done_button = ctk.CTkButton(booking_window, text="Done", command=confirm_booking)
        done_button.pack(pady=10)

    def cancel_booking():
        window.destroy()

    yes_button = ctk.CTkButton(window, text="Yes", command=book_ticket)
    yes_button.grid(row=1, column=0, padx=10, sticky="w")

    no_button = ctk.CTkButton(window, text="No", command=cancel_booking)
    no_button.grid(row=1, column=0, padx=10, sticky="e")

    window.mainloop()


def get_user_selection():
    dep_city_selection = dep_city_var.get()
    arrival_city_selection = arrival_city_var.get()
    departure_date = format_date(dep_calendar.get_date())
    return_date = format_date(ret_calendar.get_date())

    if not departure_date or not return_date:
        print("Invalid date provided")
        return

    connection = connect_to_database()
    if connection is not None:
        try:
            cursor = connection.cursor()
            query = """
                SELECT * FROM flights 
                WHERE departure_city = %s AND arrival_city = %s 
                AND departure_date = %s AND return_date = %s
            """
            cursor.execute(query, (dep_city_selection, arrival_city_selection, departure_date, return_date))
            flights = cursor.fetchall()

            # Clear the textbox before adding new items
            for flight in flights:
                flight_info = format_flight_info(flight)
                flight_frame = ctk.CTkFrame(right_frame)
                flight_frame.pack(pady=15)

                # Format the date to display only month and day
                departure_month_day = flight[4].strftime("%b %d")
                return_month_day = flight[5].strftime("%b %d")

                # Include Price, Departure Date (month and day), and Return Date (month and day) in button text
                flight_button_text = (
                    f"Price: ${flight[7]:.2f}, "
                    f"Depart: {departure_month_day}, "
                    f"Return: {return_month_day}"
                )
                flight_button = ctk.CTkButton(flight_frame, text=flight_button_text, height=70, width=30)
                flight_button.grid()
                flight_button.bind("<Button-1>", lambda event, info=flight_info: show_flight_info(info))
        except mysql.connector.Error as error:
            print("Error fetching flights from MySQL table:", error)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


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
    global cursor
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
# Configure the grid for the main window
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=0)  # Column for the vertical dividing line
window.grid_columnconfigure(2, weight=1)

# Create frames for the left and right sides
left_frame = ctk.CTkFrame(window)
left_frame.grid(row=0, column=0, sticky="nsew")
right_frame = ctk.CTkFrame(window)
right_frame.grid(row=0, column=2, sticky="nsew")

# Departure City Dropdown
dep_city_var = ctk.StringVar()
label_dep_city = ctk.CTkLabel(left_frame, text="I am departing from:")
label_dep_city.grid(row=0, column=0, sticky="w", padx=(182, 0))
dep_city_dropdown = ctk.CTkOptionMenu(left_frame, variable=dep_city_var, values=cities)
dep_city_dropdown.grid(row=1, column=0, sticky="w", padx=(182, 0))
dep_city_var.set(cities[0])  # Set the default city

# Arrival City Dropdown
arrival_city_var = ctk.StringVar()
label_arrival_city = ctk.CTkLabel(left_frame, text="I'd like to go to:")
label_arrival_city.grid(row=2, column=0, sticky="w", padx=(182, 0))
arrival_city_dropdown = ctk.CTkOptionMenu(left_frame, variable=arrival_city_var, values=cities)
arrival_city_dropdown.grid(row=3, column=0, sticky="w", padx=(182, 0))
arrival_city_var.set(cities[0])  # Set the default city

# Departure Date Calendar
label_dep_date = ctk.CTkLabel(left_frame, text="Select your departure date:")
label_dep_date.grid(row=4, column=0, sticky="w", padx=(175, 0))
dep_calendar = Calendar(left_frame)
dep_calendar.grid(row=5, column=0, sticky="w", padx=(150, 0))

# Return Date Calendar
label_ret_date = ctk.CTkLabel(left_frame, text="Select your return date:")
label_ret_date.grid(row=6, column=0, sticky="w", padx=(192, 0))
ret_calendar = Calendar(left_frame)
ret_calendar.grid(row=7, column=0, sticky="w", padx=(150, 0))

button = ctk.CTkButton(left_frame, text="View available flights", command=get_user_selection)
button.grid(row=8, column=0, sticky="w", padx=(192, 0), pady=(20, 0))

# Create and place the vertical dividing line
vertical_line = ctk.CTkFrame(window, width=2, height=570, fg_color="gray")
vertical_line.grid(row=0, column=1, sticky="ns")

# Right Frame for displaying flights
right_frame = ctk.CTkFrame(window)
right_frame.grid(row=0, column=2, sticky="nsew", padx=0)

window.mainloop()
