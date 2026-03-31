#!/usr/bin/env python3
"""
Allianz Network Provider Lookup
Check if a doctor/hospital is in the Allianz Standard Network
"""

import json
import sys
from pathlib import Path

# This would ideally connect to Allianz API or database
# For now, using placeholder structure for manual entries

NETWORK_FILE = Path(__file__).parent / "network_providers.json"

def load_network():
    """Load network provider database"""
    if NETWORK_FILE.exists():
        return json.loads(NETWORK_FILE.read_text())
    return {
        "hong_kong": {
            "standard_network": [],
            "high_cost_providers": []
        },
        "singapore": {
            "standard_network": [],
            "high_cost_providers": []
        }
    }

def search_provider(name, location="hong_kong"):
    """Search for a provider in the network"""
    network = load_network()
    
    name_lower = name.lower()
    results = []
    
    # Search in standard network
    for provider in network.get(location, {}).get("standard_network", []):
        if name_lower in provider["name"].lower():
            results.append({
                "name": provider["name"],
                "type": "Standard Network",
                "co_pay": "20% for in-patient, 10% for out-patient",
                "direct_billing": True,
                "address": provider.get("address", ""),
                "phone": provider.get("phone", "")
            })
    
    # Search in high cost providers
    for provider in network.get(location, {}).get("high_cost_providers", []):
        if name_lower in provider["name"].lower():
            results.append({
                "name": provider["name"],
                "type": "High Cost Provider",
                "co_pay": "20% extra (total 40% for in-patient)",
                "direct_billing": True,
                "warning": "Higher co-insurance applies",
                "address": provider.get("address", ""),
                "phone": provider.get("phone", "")
            })
    
    return results

def check_provider(name, location="hong_kong"):
    """Check provider status and return formatted response"""
    results = search_provider(name, location)
    
    if not results:
        return {
            "found": False,
            "message": f"'{name}' not found in {location} network database.",
            "action": "Contact APG@pacificprime.com or check MyHealth App for full list"
        }
    
    return {
        "found": True,
        "providers": results,
        "count": len(results)
    }

def add_provider(name, provider_type, location="hong_kong", **details):
    """Add a provider to the database (manual entry)"""
    network = load_network()
    
    category = "standard_network" if provider_type == "standard" else "high_cost_providers"
    
    provider = {
        "name": name,
        **details
    }
    
    network[location][category].append(provider)
    
    NETWORK_FILE.write_text(json.dumps(network, indent=2))
    return {"success": True, "message": f"Added {name} to {location} {category}"}

def main():
    if len(sys.argv) < 2:
        print("Usage: network_lookup.py {check|add} [args...]")
        print("  check <provider_name> [location]")
        print("  add <name> <standard|high_cost> [location] [address] [phone]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "check":
        if len(sys.argv) < 3:
            print("Usage: network_lookup.py check <provider_name> [location]")
            sys.exit(1)
        name = sys.argv[2]
        location = sys.argv[3] if len(sys.argv) > 3 else "hong_kong"
        result = check_provider(name, location)
        print(json.dumps(result, indent=2))
    
    elif command == "add":
        if len(sys.argv) < 4:
            print("Usage: network_lookup.py add <name> <standard|high_cost> [location]")
            sys.exit(1)
        name = sys.argv[2]
        provider_type = sys.argv[3]
        location = sys.argv[4] if len(sys.argv) > 4 else "hong_kong"
        result = add_provider(name, provider_type, location)
        print(json.dumps(result, indent=2))
    
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()