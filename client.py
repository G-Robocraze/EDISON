import pickle

# Function to select the least priority item
def select_least_priority(priority_list):
    if priority_list:
        least_priority_item = min(priority_list)
        priority_list.remove(least_priority_item)
        return least_priority_item
    else:
        return None

# Load the priority list from file (if exists)
try:
    with open('priority_list.pickle', 'rb') as file:
        priority_list = pickle.load(file)
except IOError:
    priority_list = []

# Example usage
print("Current priority list:", priority_list)

while True:
    choice = raw_input("Enter an item to add to the priority list (or 'q' to quit): ")
    if choice == 'q':
        break
    priority_list.append(choice)

print("Selected least priority item:", select_least_priority(priority_list))

# Save the updated priority list to file
with open('priority_list.pickle', 'wb') as file:
    pickle.dump(priority_list, file)
