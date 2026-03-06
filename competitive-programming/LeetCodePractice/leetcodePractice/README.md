# LeetCode Practice Session Script

A Python-based interactive practice session manager for LeetCode problems. This script helps you practice coding problems in two modes: **FAANG Mock Interview** or **Pattern-Wise Practice**.

## Features

- 🎯 **Two Practice Modes**:
  - **FAANG Mock Interview**: Randomly selects a set of problems from curated FAANG interview questions
  - **Pattern-Wise Practice**: Choose a specific pattern (e.g., Sliding Window, Two Pointers) to focus on

- ⏱️ **Built-in Timer**: 1.5-hour countdown timer to simulate real interview conditions

- 🌐 **Auto Browser Launch**: Automatically opens all selected problems in your browser

- 📊 **Progress Tracking**: Track which problems you completed or skipped after each session

- 📈 **Session Summary**: View start/end times and your performance results

## Prerequisites

- Python 3.x
- pandas library

## Installation

1. Clone or download this repository

2. Install required dependencies:
```bash
pip install pandas
```

3. Ensure you have the following CSV files in the same directory:
   - `faang_30_sets.csv` - FAANG interview problem sets
   - `patternWise.csv` - Pattern-based problem sets

## Usage

Run the script:
```bash
python3 script.py
```

### Mode 1: FAANG Mock Interview

1. Select option `1` from the main menu
2. A random set of FAANG problems will be selected
3. All problem links open in your browser
4. Press ENTER to start the 1.5-hour timer
5. After time's up, mark each problem as "done" or "skipped"

### Mode 2: Pattern-Wise Practice

1. Select option `2` from the main menu
2. View the list of available patterns:
   - Backtracking
   - Binary Search
   - Bit Manipulation
   - Dynamic Programming
   - Graph BFS/DFS
   - Greedy
   - Heap
   - Intervals
   - Sliding Window
   - Trees DFS
   - Tries
   - Two Pointers

3. Enter either:
   - The pattern number (e.g., `9` for Sliding Window)
   - The pattern name (e.g., `sliding` or `Sliding Window`)

4. A random set from your chosen pattern will be selected
5. All problem links open in your browser
6. Press ENTER to start the 1.5-hour timer
7. After time's up, mark each problem as "done" or "skipped"

## CSV File Format

### faang_30_sets.csv
```csv
Set Number,Problem,URL
Set 1,Problem Name,https://leetcode.com/problems/...
```

### patternWise.csv
```csv
Pattern,Set,Problem,URL
Sliding Window,Set 1,Problem Name,https://leetcode.com/problems/...
```

## Example Session

```
========================================
  LEETCODE PRACTICE SESSION
========================================

Choose your practice mode:
1. FAANG Mock Interview (Random Set)
2. Pattern-Wise Practice

Enter your choice (1 or 2): 2

========================================
  PATTERN-WISE PRACTICE
========================================

Available Patterns:
1. Backtracking
2. Binary Search
3. Bit Manipulation
4. Dynamic Programming
5. Graph BFS/DFS
6. Greedy
7. Heap
8. Intervals
9. Sliding Window
10. Trees DFS
11. Tries
12. Two Pointers

Enter pattern number or name: 9

🎯 Pattern: Sliding Window
🧩 Selected Set: Set 1

1. Longest Substring Without Repeating Characters -> https://leetcode.com/problems/...
2. Longest Repeating Character Replacement -> https://leetcode.com/problems/...
...

All links opened in browser.

Press ENTER to start 1.5-hour timer...
```

## Tips

- 🔥 Practice consistently - come back daily for new sets
- 📝 Take notes on patterns and approaches you learn
- ⏰ Try to complete problems within the time limit
- 🎯 Focus on one pattern at a time to build mastery
- 🔄 Review problems you skipped in future sessions

## License

Free to use for personal practice and learning.

---

**Happy Coding! 🚀**
