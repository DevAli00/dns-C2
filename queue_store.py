from collections import deque

sessions = {}

def create_session(session_id, goal, os, user, hostname):
    sessions[session_id] = {
        "goal": goal,
        "os": os,
        "user": user,
        "hostname": hostname,
        "task_queue": deque(),
        "history": [],
        "status": "idle",
        "last_task": None,   # tracks most recently dispatched command
    }

def add_task(session_id, command):
    sessions[session_id]["task_queue"].append(command)
    sessions[session_id]["status"] = "active"

def get_next_task(session_id):
    queue = sessions[session_id]["task_queue"]
    if len(queue) == 0:
        return None
    task = queue.popleft()
    sessions[session_id]["last_task"] = task
    return task

def store_result(session_id, command, output):
    sessions[session_id]["history"].append({
        "command": command,
        "output": output
    })