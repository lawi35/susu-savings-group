# Rotating Susu Savings Group

A small Python command-line program for managing one rotating savings group. Members contribute a fixed amount each week, and the full pot goes to the next member in join order only when every member has paid in full.

## Requirements

- Python 3.10 or newer
- No third-party packages required

## Run the program

```bash
python main.py
```

Enter the weekly contribution in GHS, then add members in the order they should receive the pot. Use the menu to record payments, close the week, or display a report.

## Run the tests

```bash
python -m unittest discover -s tests -v
```

The tests cover partial payments, a week that cannot close, unknown and duplicate members, invalid and excessive amounts, exact money handling, adding members after contributions begin, and reporting/payout history.

## Example

For three members (Ama, Kofi, Esi) contributing GHS 50.00 each, the pot is GHS 150.00. If Esi has paid only GHS 30.00, closing the week reports that Esi owes GHS 20.00 and does not pay out. Once Esi pays the remaining amount, closing the week pays Ama GHS 150.00 and advances the group to week 2.

## Money handling

All amounts are converted to integer pesewas to avoid binary floating-point rounding errors. Input may contain up to two decimal places.
