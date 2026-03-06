import pandas as pd
import random
import webbrowser
import time
from datetime import datetime

FAANG_CSV = "faang_30_sets.csv"
PATTERN_CSV = "patternWise.csv"

def load_faang_sets(csv_path):
    df = pd.read_csv(csv_path)
    grouped = df.groupby("Set Number")
    sets = {k: list(zip(v["Problem"], v["URL"])) for k, v in grouped}
    return sets

def load_pattern_sets(csv_path):
    df = pd.read_csv(csv_path)
    return df

def get_available_patterns(df):
    return sorted(df["Pattern"].unique())

def start_timer(seconds):
    print("\n⏳ Timer Started: 1 hour 30 min")
    while seconds > 0:
        mins, secs = divmod(seconds, 60)
        timer = f"{mins:02d}:{secs:02d}"
        print(f"\rRemaining: {timer}", end="")
        time.sleep(1)
        seconds -= 1
    print("\n\n⏰ TIME UP! Stop coding.")

def practice_session():
    print("\n" + "="*40)
    print("  LEETCODE PRACTICE SESSION")
    print("="*40)
    print("\nChoose your practice mode:")
    print("1. FAANG Mock Interview (Random Set)")
    print("2. Pattern-Wise Practice")
    
    choice = input("\nEnter your choice (1 or 2): ").strip()
    
    if choice == "1":
        # FAANG Mode
        sets = load_faang_sets(FAANG_CSV)
        chosen_set = random.choice(list(sets.keys()))
        problems = sets[chosen_set]
        
        print("\n" + "="*40)
        print("  FAANG MOCK INTERVIEW")
        print("="*40)
        print(f"\n🧩 Selected Set: {chosen_set}\n")
        
    elif choice == "2":
        # Pattern-Wise Mode
        df = load_pattern_sets(PATTERN_CSV)
        patterns = get_available_patterns(df)
        
        print("\n" + "="*40)
        print("  PATTERN-WISE PRACTICE")
        print("="*40)
        print("\nAvailable Patterns:")
        for i, pattern in enumerate(patterns, 1):
            print(f"{i}. {pattern}")
        
        pattern_choice = input("\nEnter pattern number or name: ").strip()
        
        # Handle both number and name input
        if pattern_choice.isdigit():
            pattern_idx = int(pattern_choice) - 1
            if 0 <= pattern_idx < len(patterns):
                selected_pattern = patterns[pattern_idx]
            else:
                print("Invalid pattern number!")
                return
        else:
            # Try to match by name (case-insensitive)
            matches = [p for p in patterns if pattern_choice.lower() in p.lower()]
            if matches:
                selected_pattern = matches[0]
            else:
                print("Pattern not found!")
                return
        
        # Get all problems for the selected pattern
        pattern_df = df[df["Pattern"] == selected_pattern]
        
        # Group by set and randomly choose one
        sets = pattern_df.groupby("Set")
        set_names = list(sets.groups.keys())
        chosen_set = random.choice(set_names)
        
        problems_df = pattern_df[pattern_df["Set"] == chosen_set]
        problems = list(zip(problems_df["Problem"], problems_df["URL"]))
        
        print(f"\n🎯 Pattern: {selected_pattern}")
        print(f"🧩 Selected Set: {chosen_set}\n")
        
    else:
        print("Invalid choice! Please run the script again.")
        return

    # Open the problems in browser
    for i, (title, url) in enumerate(problems, 1):
        print(f"{i}. {title} -> {url}")
        webbrowser.open(url)

    print("\nAll links opened in browser.")
    input("\nPress ENTER to start 1.5-hour timer...")

    start_time = datetime.now()
    start_timer(5400)   # 1.5 hours = 5400 sec
    end_time = datetime.now()

    print("\nSession Summary:")
    print("----------------")
    print(f"Start: {start_time}")
    print(f"End:   {end_time}")

    # Mark performance
    results = []
    for i, (title, _) in enumerate(problems, 1):
        status = input(f"Status for Problem {i} ({title}) [done/skipped]: ")
        results.append((title, status.strip().lower()))

    print("\nYour Results:")
    for title, status in results:
        print(f"- {title}: {status}")

    print("\n🔥 Good job! Come back tomorrow for next set.\n")

if __name__ == "__main__":
    practice_session()
