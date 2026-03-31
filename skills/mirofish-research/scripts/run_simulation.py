#!/usr/bin/env python3
"""
MiroFish Research Automation Script
Usage: python3 run_simulation.py --seed /tmp/seed.txt --prompt "模拟..." --name "scenario"
"""
import requests, json, time, sys, argparse

BASE = "http://localhost:5001"

def check_health():
    try:
        r = requests.get(f"{BASE}/health", timeout=5)
        return r.json().get("status") == "ok"
    except:
        return False

def generate_ontology(seed_file, prompt, name="Simulation"):
    print(f"[1/4] Generating ontology from seed...")
    with open(seed_file, 'rb') as f:
        r = requests.post(
            f"{BASE}/api/graph/ontology/generate",
            files={'files': (seed_file, f, 'text/plain')},
            data={'simulation_requirement': prompt, 'project_name': name},
            timeout=120
        )
    if r.status_code != 200:
        print(f"  ERROR: {r.status_code} - {r.text[:200]}")
        return None
    data = r.json()["data"]
    print(f"  ✓ project_id: {data['project_id']}")
    entities = data.get("ontology", {}).get("entity_types", [])
    entities_str = [str(e) for e in entities]
    print(f"  ✓ entities detected: {', '.join(entities_str)}")
    return data["project_id"]

def prepare_simulation(project_id, prompt):
    print(f"[2/4] Preparing simulation...")
    r = requests.post(
        f"{BASE}/api/simulation/prepare",
        json={"project_id": project_id, "simulation_requirement": prompt},
        timeout=300
    )
    if r.status_code != 200:
        print(f"  ERROR: {r.status_code} - {r.text[:200]}")
        return None
    data = r.json()["data"]
    sim_id = data["simulation_id"]
    print(f"  ✓ sim_id: {sim_id}")
    print(f"  ✓ agents: {data.get('agent_count', 'N/A')}")
    return sim_id

def start_simulation(sim_id, max_rounds=10):
    print(f"[3/4] Starting simulation (max {max_rounds} rounds)...")
    r = requests.post(
        f"{BASE}/api/simulation/start",
        json={"simulation_id": sim_id, "max_rounds": max_rounds},
        timeout=30
    )
    if r.status_code != 200:
        print(f"  ERROR: {r.status_code} - {r.text[:200]}")
        return False
    print(f"  ✓ Started!")
    return True

def monitor(sim_id, poll_interval=15, timeout_min=30):
    print(f"[4/4] Monitoring (polling every {poll_interval}s)...")
    deadline = time.time() + timeout_min * 60
    while time.time() < deadline:
        r = requests.get(f"{BASE}/api/simulation/{sim_id}/run-status", timeout=10)
        status = r.json()
        s = status.get("status", "unknown")
        round_info = status.get("current_round", "?")
        print(f"  status: {s} | round: {round_info}")
        if s == "completed":
            report_id = status.get("report_id")
            if report_id:
                return report_id
        elif s == "error":
            print(f"  ✗ Simulation failed")
            return None
        time.sleep(poll_interval)
    print("  ✗ Timeout")
    return None

def fetch_report(report_id):
    r = requests.get(f"{BASE}/api/report/{report_id}", timeout=30)
    return r.json()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", required=True)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--name", default="Simulation")
    parser.add_argument("--rounds", type=int, default=8)
    args = parser.parse_args()

    if not check_health():
        print("✗ MiroFish backend not running! Start with: cd ~/clawd-projects/MiroFish && npm run dev")
        sys.exit(1)

    project_id = generate_ontology(args.seed, args.prompt, args.name)
    if not project_id: sys.exit(1)

    sim_id = prepare_simulation(project_id, args.prompt)
    if not sim_id: sys.exit(1)

    if not start_simulation(sim_id, args.rounds): sys.exit(1)

    report_id = monitor(sim_id)
    if report_id:
        report = fetch_report(report_id)
        print("\n=== REPORT ===")
        print(json.dumps(report, ensure_ascii=False, indent=2)[:3000])
    else:
        print("No report generated.")
