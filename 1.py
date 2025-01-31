from datetime import datetime, timedelta

class Event:
    def __init__(self, start_time, end_time, description):
        self.start_time = start_time
        self.end_time = end_time
        self.description = description

    def __repr__(self):
        return f"Event({self.start_time}, {self.end_time}, '{self.description}')"

    def __str__(self):
        return f'"{self.description}", Start: "{self.start_time.strftime("%H:%M")}", End: "{self.end_time.strftime("%H:%M")}"'


class EventScheduler:
    def __init__(self):
        self.events = []

    def add_event(self, start_time, end_time, description):
        new_event = Event(start_time, end_time, description)
        
        # Check for conflicts
        if self.check_conflict(new_event):
            print(f"Conflict detected for event '{description}'!")
            alternative_times = self.suggest_alternatives(new_event)
            if alternative_times:
                print("Suggested alternative time slots:")
                for time in alternative_times:
                    print(f"- {time[0]} to {time[1]}")
            else:
                print("No alternative times available.")
        else:
            self.events.append(new_event)
            print(f"Event '{description}' added successfully!")

    def check_conflict(self, new_event):
        for event in self.events:
            if not (new_event.end_time <= event.start_time or new_event.start_time >= event.end_time):
                return True  # Conflict detected
        return False

    def suggest_alternatives(self, new_event):
        available_slots = []
        
        # Sort events by start time to easily check for gaps
        sorted_events = sorted(self.events, key=lambda e: e.start_time)
        
        # Check the time gaps before and after existing events
        for i in range(len(sorted_events) - 1):
            current_event = sorted_events[i]
            next_event = sorted_events[i + 1]
            
            # Suggest gap between current_event and next_event
            if current_event.end_time < next_event.start_time:
                gap_start = current_event.end_time
                gap_end = next_event.start_time
                if gap_end - gap_start >= (new_event.end_time - new_event.start_time):
                    available_slots.append((gap_start, gap_end))
        
        # Suggest time slots after the last event
        if len(sorted_events) > 0:
            last_event = sorted_events[-1]
            gap_start = last_event.end_time
            # Assuming a fixed end of day time (e.g., 9 PM)
            gap_end = datetime.combine(gap_start.date(), datetime.max.time()).replace(hour=21, minute=0)
            if gap_end - gap_start >= (new_event.end_time - new_event.start_time):
                available_slots.append((gap_start, gap_end))
        
        return available_slots

    def display_events(self):
        if not self.events:
            print("No events scheduled.")
        else:
            print("Events:")
            for i, event in enumerate(self.events, 1):
                print(f"{i}. {event}")


# Helper function to parse time from string to datetime object
def parse_time(time_str):
    return datetime.strptime(time_str, "%Y-%m-%d %H:%M")

# Example usage
scheduler = EventScheduler()

# Add some events
scheduler.add_event(parse_time("2025-01-31 09:00"), parse_time("2025-01-31 10:30"), "Meeting A")
scheduler.add_event(parse_time("2025-01-31 10:00"), parse_time("2025-01-31 11:30"), "Workshop B")
scheduler.add_event(parse_time("2025-01-31 12:00"), parse_time("2025-01-31 13:00"), "Lunch Break")
scheduler.add_event(parse_time("2025-01-31 10:30"), parse_time("2025-01-31 12:00"), "Presentation C")

# Display all events
scheduler.display_events()
