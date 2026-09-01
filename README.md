# hardware-health-checker

A small Python tool that checks your computer's OS, CPU, memory, and disk, warns you if disk or memory is running low, and saves each check to a file so you can look back at them later.

One file. Only needs `psutil`.

## What it checks

- **OS** - name, version, and architecture
- **CPU** - how many cores you have
- **RAM** - total, free, and percent used
- **Disk** - total, used, and free space for **one** drive: the one you run the script from

## Warnings

Two warnings, with fixed limits:

- Disk is 85% full or more
- Free memory is 2 GB or less

To change these, edit the numbers in `health_checks()`.

## Menu

1. Run a check and save it
2. Show the last 5 saved checks
3. Save the newest check as a text file
4. Quit

## Setup

Needs Python 3.9 or newer.

```
python -m pip install psutil
python hardware_checker.py
```

You pick options from a menu, so it can't be run on a schedule or from a script yet.

## Files it makes

Both are saved in the folder you run the script from, so running it from a different folder starts a separate log.

- `hardware_log.json` - all past checks
- `latest_report.txt` - the newest check as plain text

## Known problems

- **The log can get wiped.** If `hardware_log.json` gets damaged, the script treats it as empty and overwrites it on the next run. You lose every past check and it doesn't tell you.
- Saved checks don't record which computer they came from.
- Only one drive is checked.
- No CPU load, temperature, or drive health info.
- No tests yet.

## What it is not

This only looks at the computer it's running on. It doesn't run in the background, doesn't have a web API, and doesn't check other machines.
