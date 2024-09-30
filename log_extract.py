import win32evtlog

def read_event_logs(log_name, output_file):
    # Open the event log
    server = 'localhost'
    hand = win32evtlog.OpenEventLog(server, log_name)
    
    # Read log entries
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    events = []
    
    while True:
        # Read the events in chunks
        records = win32evtlog.ReadEventLog(hand, flags, 0)
        if not records:
            break
        for record in records:
            # Extract relevant information from the event
            event_id = record.EventID
            time_generated = record.TimeGenerated.Format()
            source_name = record.SourceName
            event_message = record.StringInserts
            
            events.append({
                'event_id': event_id,
                'time_generated': time_generated,
                'source_name': source_name,
                'message': event_message
            })
    
    # Write the extracted events to a file (simple text format for now)
    with open(output_file, 'w') as file:
        for event in events:
            file.write(f"Time: {event['time_generated']}, Source: {event['source_name']}, Event ID: {event['event_id']}, Message: {event['message']}\n")
    
    print(f"Logs extracted to {output_file}")

if __name__ == "__main__":
    log_name = 'Security'  # Change to the log name you want to read (e.g., "Application", "System")
    output_file = 'extracted_security_logs.txt'
    
    read_event_logs(log_name, output_file)
