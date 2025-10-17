import argparse, json, os, datetime as dt

DB = "habits.json"

def load():
    if not os.path.exists(DB):
        return {"habits": []}
    with open(DB, "r") as f:
        return json.load(f)

def save(db):
    with open(DB, "w") as f:
        json.dump(db, f, indent=2)

def add(name):
    db = load()
    db["habits"].append({"name": name, "done": False, "last_done": None})
    save(db)
    print(f"Added: {name}")

def ls():
    db = load()
    if not db["habits"]:
        print("(no habits yet)")
        return
    for i, h in enumerate(db["habits"], 1):
        flag = "✓" if h["done"] else " "
        when = h["last_done"] or "-"
        print(f"{i}. [{flag}] {h['name']} (last_done: {when})")

def check(index):
    db = load()
    i = int(index) - 1
    h = db["habits"][i]
    h["done"] = True
    h["last_done"] = dt.datetime.now().strftime("%Y-%m-%d")
    save(db)
    print(f"Checked: {h['name']}")

if __name__ == "__main__":
    p = argparse.ArgumentParser(prog="habits", description="Simple CLI habit tracker")
    sub = p.add_subparsers(dest="cmd", required=True)

    pa = sub.add_parser("add");   pa.add_argument("name")
    pl = sub.add_parser("list")
    pc = sub.add_parser("check"); pc.add_argument("index")

    args = p.parse_args()
    if args.cmd == "add": add(args.name)
    elif args.cmd == "list": ls()
    elif args.cmd == "check": check(args.index)
