#!/usr/bin/env python3
"""
Allianz Care Visit Counter
Tracks visits that may require doctor notes after certain limits
"""

import json
import sys
from datetime import datetime
from pathlib import Path

COUNTER_FILE = Path(__file__).parent / "counters.json"

def load_counters():
    """Load counter data"""
    if COUNTER_FILE.exists():
        return json.loads(COUNTER_FILE.read_text())
    return {
        "physiotherapy": {"current_count": 0, "max_before_note": 4, "visits": []},
        "psychiatry_sessions": {"current": 0, "max_before_review": 5, "visits": []},
        "specialist_visits": {"current": 0, "max_before_note": 4, "visits": []}
    }

def save_counters(data):
    """Save counter data"""
    COUNTER_FILE.write_text(json.dumps(data, indent=2))

def add_visit(treatment_type, date, provider, amount, currency, diagnosis):
    """Add a new visit and check if note is needed"""
    counters = load_counters()
    
    # Map treatment types to counter categories
    category_map = {
        "physiotherapy": "physiotherapy",
        "physio": "physiotherapy",
        "psychiatry": "psychiatry_sessions",
        "psychotherapy": "psychiatry_sessions",
        "specialist": "specialist_visits",
        "specialist visit": "specialist_visits"
    }
    
    category = category_map.get(treatment_type.lower(), treatment_type.lower())
    
    if category not in counters:
        counters[category] = {
            "current_count": 0,
            "max_before_note": 4,
            "visits": [],
            "alert_sent": False
        }
    
    # Add visit
    counters[category]["current_count"] += 1
    counters[category]["visits"].append({
        "date": date,
        "provider": provider,
        "amount": amount,
        "currency": currency,
        "diagnosis": diagnosis
    })
    
    # Check if approaching limit
    current = counters[category]["current_count"]
    max_limit = counters[category].get("max_before_note", 4)
    remaining = max_limit - current
    
    alert_message = ""
    if remaining == 1:
        alert_message = f"⚠️ ALERT: This is your {current}th {category} visit. After {max_limit} visits, you may need a doctor's note. Next visit will require documentation."
    elif remaining <= 0:
        alert_message = f"🚨 IMPORTANT: You have reached {current} {category} visits. A doctor's note/referral is now REQUIRED for continued coverage."
        counters[category]["alert_sent"] = True
    
    save_counters(counters)
    
    return {
        "category": category,
        "current_count": current,
        "max_limit": max_limit,
        "remaining": remaining,
        "alert": alert_message
    }

def get_status(category=None):
    """Get current counter status"""
    counters = load_counters()
    
    if category:
        if category in counters:
            data = counters[category]
            return {
                "category": category,
                "current": data["current_count"],
                "max": data.get("max_before_note", 4),
                "remaining": data.get("max_before_note", 4) - data["current_count"],
                "visits": data["visits"]
            }
        return {"error": f"Category '{category}' not found"}
    
    # Return all categories
    summary = {}
    for cat, data in counters.items():
        summary[cat] = {
            "current": data["current_count"],
            "max": data.get("max_before_note", 4),
            "remaining": data.get("max_before_note", 4) - data["current_count"]
        }
    return summary

def reset_counter(category):
    """Reset a counter (e.g., after getting doctor's note)"""
    counters = load_counters()
    if category in counters:
        counters[category]["current_count"] = 0
        counters[category]["alert_sent"] = False
        counters[category]["visits"] = []
        save_counters(counters)
        return {"success": True, "message": f"{category} counter reset to 0"}
    return {"error": f"Category '{category}' not found"}

def main():
    if len(sys.argv) < 2:
        print("Usage: counter.py {add|status|reset} [args...]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "add":
        if len(sys.argv) < 7:
            print("Usage: counter.py add <treatment_type> <date> <provider> <amount> <currency> [diagnosis]")
            sys.exit(1)
        result = add_visit(
            sys.argv[2],  # treatment_type
            sys.argv[3],  # date
            sys.argv[4],  # provider
            sys.argv[5],  # amount
            sys.argv[6],  # currency
            sys.argv[7] if len(sys.argv) > 7 else ""  # diagnosis
        )
        print(json.dumps(result, indent=2))
    
    elif command == "status":
        category = sys.argv[2] if len(sys.argv) > 2 else None
        result = get_status(category)
        print(json.dumps(result, indent=2))
    
    elif command == "reset":
        if len(sys.argv) < 3:
            print("Usage: counter.py reset <category>")
            sys.exit(1)
        result = reset_counter(sys.argv[2])
        print(json.dumps(result, indent=2))
    
    else:
        print(f"Unknown command: {command}")
        print("Usage: counter.py {add|status|reset} [args...]")

if __name__ == "__main__":
    main()