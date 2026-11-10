import csv

class ToDoList:

    def __init__(self):
        self.tasks = []

    def add_task(self, name, description, priority):
        new_task = Task(name, description, priority)
        self.tasks.append(new_task)

    def remove_task(self, name):
        for task in self.tasks:
            if task.name == name:
                self.tasks.remove(task)
                print("The task was removed successfully")
                return
        print("Task not found!")

    def show_tasks(self):
        if not self.tasks:
            print("No tasks found.")
        else:
            for task in self.tasks:
                print(task.__str__())

    def save_to_csv(self):
        try:
            with open("Historical data.csv", mode="w", encoding="utf-8", newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Name", "Description", "Priority"])
                for task in self.tasks:
                    writer.writerow([task.name, task.description, task.priority])
            print("Tasks saved successfully")
        except PermissionError:
            print("ERROR: File is open in another program. Please close it and try again.")
        except Exception as e:
            print(f"Error saving: {e}")

    def load_from_csv(self):
        try:
            with open("Historical data.csv", mode="r", encoding="utf-8") as file:
                reader = csv.reader(file)
                header = next(reader, None)
                if header is None:
                    print("File is empty. Nothing to load.")
                    return
                
                existing_names = [task.name for task in self.tasks]
                added_count = 0
                total_rows = 0
                
                skipped_rows = 0
                for row in reader:
                    total_rows += 1
                    if len(row) < 3:
                        skipped_rows += 1
                        continue
                    if row[0] not in existing_names:
                        self.tasks.append(Task(row[0], row[1], row[2]))
                        existing_names.append(row[0])
                        added_count += 1
                
                if total_rows == 0:
                    print("File is empty or contains no valid data.")
                elif added_count == 0:
                    print(f"No new tasks were added (all {total_rows} task(s) already exist).")
                else:
                    print(f"Successfully loaded {added_count} new task(s) from {total_rows} total task(s).")

                if skipped_rows:
                    print(f"Skipped {skipped_rows} malformed row(s).")
                    
        except FileNotFoundError:
            print("Historical data file not found.")
        except Exception as e:
            print(f"Error loading: {e}")


class Task:
    def __init__(self, name, description, priority):
        self.name = name
        self.description = description
        self.priority = priority

    def __str__(self):
        return f"name: {self.name} | description: {self.description} | priority: {self.priority}"


def show_welcome():
    print("=" * 40)
    print("     Welcome to To-Do List Manager")
    print("=" * 40)
    print("  Organize your tasks easily and quickly!")
    print("  Choose an option from the menu below.")
    print("=" * 40)
    print()


to_do_list = ToDoList()
show_welcome()

while True:
    print("1.Add new task")
    print("2.Delete task")
    print("3.View task list")
    print("4.Save the to-do list to a CSV file")
    print("5.Load from CSV file")
    print("6.Exit")
    
    while True:
        try:
            selection = int(input("Enter your choice: "))
            break
        except ValueError:
            print("Please enter a number")
            print("-"*35)

    match selection:
        case 1:
            name = input("Enter your task name: ")
            description = input("Enter your description: ")
            while True:
                try:
                    priority = int(input("Choose task priority\n1.High\n2.Medium\n3.Low\nselected: "))
                    if not 1 <= priority <= 3:
                        print("Please enter a valid priority")
                        continue
                    match priority:
                        case 1:
                            priority = "High"
                        case 2:
                            priority = "Medium"
                        case 3:
                            priority = "Low"
                    break
                except ValueError:
                    print("Please enter a number")
            to_do_list.add_task(name, description, priority)
            print("The new task was saved successfully")
            print("-"*35)
        case 2:
            name = input("Enter your task name: ")
            to_do_list.remove_task(name)
            print("-"*35)
        case 3:
            print("-"*35)
            to_do_list.show_tasks()
            print("-"*35)
        case 4:
            to_do_list.save_to_csv()
            print("-"*35)
        case 5:
            to_do_list.load_from_csv()
            print("-"*35)
        case 6:
            print("Exiting...")
            break
        case _:
            print("Please choose a number between 1 and 6")
            print("-"*35)