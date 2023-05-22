import pickle

# Function to update load priority and manage loads
def manage_loads(load_priority, load_status, total_load, load_limit):
    if total_load > load_limit:
        # Turn off loads starting from the lowest priority until total load is below the limit
        for load_id in load_priority:
            if load_status[load_id] == "ON":
                load_status[load_id] = "OFF"
                total_load -= load_id
                if total_load <= load_limit:
                    break
    else:
        # Turn on loads starting from the highest priority until total load is below the limit
        for load_id in reversed(load_priority):
            if load_status[load_id] == "OFF":
                load_status[load_id] = "ON"
                total_load += load_id
                if total_load >= load_limit:
                    break

    return total_load

# Load the load priority and load status dictionaries from file (if exist)
try:
    with open('load_priority.pickle', 'rb') as file:
        load_priority = pickle.load(file)
    with open('load_status.pickle', 'rb') as file:
        load_status = pickle.load(file)
except IOError:
    load_priority = []
    load_status = {}

# Example initialization (you can modify this according to your requirements)
load_priority = [1, 2, 3, 4, 5]  # Update with your load priorities
load_status = {1: "ON", 2: "ON", 3: "ON", 4: "ON", 5: "ON"}  # Update with your load statuses
total_load = sum(load_priority)
load_limit = 10  # Update with your load limit

print("Current load status:", load_status)

while True:
    choice = raw_input("Enter 'u' to update load priority, 'q' to quit, or any other key to simulate load change: ")

    if choice == 'u':
        # Update load priority
        load_priority = []
        for _ in range(len(load_status)):
            load_id = int(raw_input("Enter load ID: "))
            load_priority.append(load_id)

        # Save the updated load priority to file
        with open('load_priority.pickle', 'wb') as file:
            pickle.dump(load_priority, file)

        print("Updated load priority:", load_priority)

    elif choice == 'q':
        break

    else:
        # Simulate load change
        total_load = manage_loads(load_priority, load_status, total_load, load_limit)
        print("Current load status:", load_status)
        print("Total load:", total_load)

# Save the load status dictionary to file
with open('load_status.pickle', 'wb') as file:
    pickle.dump(load_status, file)
