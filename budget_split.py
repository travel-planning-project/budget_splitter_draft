def add_members():
    
    members = {}
    n = int(input("Enter number of members: "))
    for _ in range(n):
        name = input("Enter member name: ")
        members[name] = 0.0  # start with 0 paid
    return members


def record_expense(members, shares):
    payer = input("Who paid? ")
    amount = float(input("How much did they pay? "))

    # Add to payer's total paid
    members[payer] += amount

    # Decide how to split
    choice = int(input("Split options:\n1. Split among all equally\n2. Split among selected members\nChoose: "))

    if choice == 1:
        per_head = amount / len(members)
        for member in members:
            shares[member] += per_head

    elif choice == 2:
        selected = input("Enter selected members (comma separated): ").split(",")
        selected = [m.strip() for m in selected if m.strip() in members]

        split_choice = int(input("1. Split equally\n2. Enter custom shares\nChoose: "))

        if split_choice == 1:
            per_head = amount / len(selected)
            for member in selected:
                shares[member] += per_head
        else:
            total_entered = 0
            for member in selected:
                val = float(input(f"Enter share for {member}: "))
                shares[member] += val
                total_entered += val
            if abs(total_entered - amount) > 1e-6:
                print("⚠ Warning: Entered shares do not match the paid amount!")


def show_summary(members, shares):
    print("\n--- Expense Summary ---")
    print(f"{'Member':<15}{'Paid':<10}{'Share':<10}{'Pending':<10}")
    pending_map = {}
    for member in members:
        paid = members[member]
        share = shares[member]
        pending = share - paid
        pending_map[member] = pending
        print(f"{member:<15}{paid:<10.2f}{share:<10.2f}{pending:<10.2f}")
    return pending_map


def settle_expenses(pending_map):
    owes = [(m, amt) for m, amt in pending_map.items() if amt > 0]   # needs to pay
    gets = [(m, -amt) for m, amt in pending_map.items() if amt < 0]  # should receive

    i, j = 0, 0
    settlements = []

    while i < len(owes) and j < len(gets):
        owe_name, owe_amt = owes[i]
        get_name, get_amt = gets[j]

        settled_amt = min(owe_amt, get_amt)
        settlements.append(f"{owe_name} pays {get_name}: {settled_amt:.2f}")

        owes[i] = (owe_name, owe_amt - settled_amt)
        gets[j] = (get_name, get_amt - settled_amt)

        if owes[i][1] == 0:
            i += 1
        if gets[j][1] == 0:
            j += 1

    print("\n--- Settlements ---")
    if settlements:
        for s in settlements:
            print(s)
    else:
        print("No settlements needed! Everyone is even.")


members = add_members()
shares = {name: 0.0 for name in members}

while True:
    record_expense(members, shares)
    cont = input("Add another expense? (y/n): ")
    if cont.lower() != "y":
        break

pending_map = show_summary(members, shares)
settle_expenses(pending_map)
