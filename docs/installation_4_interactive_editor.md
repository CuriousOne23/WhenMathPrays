# Installation Guide for Interactive Editor (Phase 2 Stable)

**Last Updated:** December 8, 2025  
**Version:** Phase 2.2 Stable (v2.2-stable tag)  
**Target Audience:** Users with no Python, GitHub, or programming experience  
**Time Required:** 20-30 minutes

---

## What You're Installing

The **Interactive Editor (Phase 2)** is a visual tool for exploring relationship dynamics using the Gamma Relational Persona (GRP) model. This is the latest version with advanced features including:

- View relationship trajectories in complex space (γ_self plane)
- Adjust relationship primitives (visibility, resonance, fidelity, altruism, shared breath)
- **Counterfactual Explorer:** Experiment with "what-if" scenarios using diagnostic markers
- Real-time trajectory preview as you make changes
- Professional PySide6/PyQtGraph interface

---

## Prerequisites: What You'll Need

- **Computer:** Windows, Mac, or Linux
- **Internet connection:** For downloading software
- **About 500 MB of free disk space**
- **Administrative access:** To install software

---

## Step 1: Install Python

Python is the programming language that runs the Interactive Editor.

### Windows:

1. **Download Python:**
   - Go to: https://www.python.org/downloads/
   - Click the big yellow button: **"Download Python 3.12.x"** (or latest version)
   - Save the file (it's about 25 MB)

2. **Install Python:**
   - Double-click the downloaded file (`python-3.12.x.exe`)
   - **⚠️ IMPORTANT:** Check the box that says **"Add Python to PATH"** at the bottom
   - Click **"Install Now"**
   - Wait 2-3 minutes for installation to complete
   - Click **"Close"** when finished

3. **Verify Installation:**
   - Press `Windows key + R`
   - Type: `cmd` and press Enter
   - In the black window that opens, type: `python --version`
   - You should see: `Python 3.12.x` (or similar)
   - If you see an error, restart your computer and try again

### Mac:

1. **Download Python:**
   - Go to: https://www.python.org/downloads/
   - Click: **"Download Python 3.12.x"** (or latest version)
   - Save the file (it's about 40 MB)

2. **Install Python:**
   - Double-click the downloaded `.pkg` file
   - Click **"Continue"** through the installation wizard
   - Click **"Install"** (you may need to enter your password)
   - Wait 2-3 minutes
   - Click **"Close"** when finished

3. **Verify Installation:**
   - Open **Terminal** (search for "Terminal" in Spotlight - press `Cmd + Space` and type "Terminal")
   - Type: `python3 --version`
   - You should see: `Python 3.12.x`

### Linux:

Most Linux distributions already have Python installed. Open a terminal and check:

```bash
python3 --version
```

If not installed, use your package manager:
- **Ubuntu/Debian:** `sudo apt install python3 python3-pip`
- **Fedora:** `sudo dnf install python3 python3-pip`
- **Arch:** `sudo pacman -S python python-pip`

---

## Step 2: Install Git

Git is version control software that lets you download the project code.

### Windows:

1. **Download Git:**
   - Go to: https://git-scm.com/download/win
   - The download should start automatically
   - Save the file (about 50 MB)

2. **Install Git:**
   - Double-click the downloaded file (`Git-x.xx.x-64-bit.exe`)
   - Click **"Next"** through all the screens (default options are fine)
   - Wait 2-3 minutes
   - Click **"Finish"**

3. **Verify Installation:**
   - Press `Windows key + R`
   - Type: `cmd` and press Enter
   - Type: `git --version`
   - You should see: `git version 2.xx.x`

### Mac:

1. **Install using Homebrew (recommended):**
   - Open Terminal
   - If you don't have Homebrew, install it first:
     ```bash
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
     ```
   - Then install Git:
     ```bash
     brew install git
     ```

2. **Verify Installation:**
   ```bash
   git --version
   ```

### Linux:

Use your package manager:
- **Ubuntu/Debian:** `sudo apt install git`
- **Fedora:** `sudo dnf install git`
- **Arch:** `sudo pacman -S git`

---

## Step 3: Download the WhenMathPrays Project

Now we'll download the actual Interactive Editor software.

### All Operating Systems:

1. **Choose a folder location:**
   - **Windows:** We recommend: `C:\Users\YourName\Documents\`
   - **Mac/Linux:** We recommend: `~/Documents/`

2. **Open Command Line:**
   - **Windows:** Press `Windows key + R`, type `cmd`, press Enter
   - **Mac/Linux:** Open Terminal

3. **Navigate to your chosen folder:**
   
   **Windows:**
   ```cmd
   cd C:\Users\YourName\Documents
   ```
   (Replace `YourName` with your actual username)
   
   **Mac/Linux:**
   ```bash
   cd ~/Documents
   ```

4. **Download the project:**
   ```bash
   git clone https://github.com/CuriousOne23/WhenMathPrays.git
   ```
   
   This will create a folder called `WhenMathPrays` and download all the files (about 50 MB, takes 1-2 minutes).

5. **Enter the project folder:**
   
   **Windows:**
   ```cmd
   cd WhenMathPrays
   ```
   
   **Mac/Linux:**
   ```bash
   cd WhenMathPrays
   ```

6. **Switch to the phase2 stable version:**
   
   The Interactive Editor Phase 2 is in the `phase2` branch. We'll use the latest stable version (v2.2-stable).
   
   ```bash
   git checkout phase2
   ```
   
   You should see: `Switched to branch 'phase2'`
   
   Then checkout the stable tag:
   ```bash
   git checkout v2.2-stable
   ```
   
   You should see: `Note: switching to 'v2.2-stable'`

---

## Step 4: Install Required Python Packages

The Interactive Editor needs additional Python libraries to work.

### All Operating Systems:

1. **Make sure you're in the WhenMathPrays folder** (from Step 3)

2. **Install packages:**
   
   **Windows:**
   ```cmd
   pip install -r requirements.txt
   ```
   
   **Mac/Linux:**
   ```bash
   pip3 install -r requirements.txt
   ```
   
   This will download and install:
   - PySide6 (for the user interface)
   - PyQtGraph (for plotting)
   - NumPy (for mathematical calculations)
   - Other dependencies
   
   **This takes 3-5 minutes.** You'll see progress as each package installs.

3. **Wait for completion:**
   - When finished, you should see: `Successfully installed ...`
   - If you see any errors, see the **Troubleshooting** section below

---

## Step 5: Run the Interactive Editor

You're ready to launch the application!

### Launch the Editor:

**Windows:**
```cmd
python tools\interactive_editor.py data\single_dating_to_love_M1.csv
```

**Mac/Linux:**
```bash
python3 tools/interactive_editor.py data/single_dating_to_love_M1.csv
```

### What Should Happen:

1. A window will open showing:
   - **Left side:** 5 plots for primitives (visibility, resonance, fidelity, altruism, shared breath)
   - **Right side:** Complex plane showing the relationship trajectory

2. You can now:
   - Drag markers to adjust primitive values
   - See the trajectory update in real-time
   - Experiment with relationship dynamics

3. **To close the editor:**
   - Click the X button in the window corner, or
   - Press `Ctrl+Q` (Windows/Linux) or `Cmd+Q` (Mac)

---

## Testing Your Installation

Let's make sure everything works:

### Test 1: Load a Scenario
- The editor should open with a scenario already loaded (Ann's dating journey)
- You should see colored dots (markers) on the primitive plots
- You should see a curved line (trajectory) on the right plot

### Test 2: Drag a Marker
- Click and drag any marker on a primitive plot
- The marker should move with your mouse
- The trajectory on the right should update (might take 1-2 seconds)

### Test 3: Diagnostic Marker (Counterfactual Explorer)
- Hold `Shift` and click on any primitive plot
- A red X should appear
- The trajectory should show a preview line in a different color

**If all three tests work: ✅ Installation successful!**

---

## Troubleshooting

### "Python is not recognized as a command"

**Problem:** Python wasn't added to your PATH during installation.

**Solution (Windows):**
1. Uninstall Python (Control Panel → Programs → Uninstall)
2. Reinstall Python, making sure to check **"Add Python to PATH"**
3. Restart your computer

**Solution (Mac):**
- Use `python3` instead of `python` in all commands

### "pip is not recognized as a command"

**Problem:** pip (Python package installer) isn't available.

**Solution:**
```bash
python -m pip install -r requirements.txt
```

Or on Mac/Linux:
```bash
python3 -m pip install -r requirements.txt
```

### "No module named 'PySide6'" (or similar)

**Problem:** Required packages didn't install properly.

**Solution:**
Try installing packages individually:
```bash
pip install PySide6
pip install pyqtgraph
pip install numpy
```

### "Cannot find file 'single_dating_to_love_M1.csv'"

**Problem:** You're not in the right folder.

**Solution:**
Make sure you're in the `WhenMathPrays` folder:
```bash
cd path/to/WhenMathPrays
```

Then try running the editor again.

### Window Opens But Is Blank

**Problem:** Graphics driver or Qt compatibility issue.

**Solution:**
1. Update your graphics drivers
2. Try setting an environment variable:
   ```bash
   set QT_OPENGL=software
   ```
   Then run the editor again

### Editor Opens But Crashes When Dragging Markers

**Problem:** Possible PyQtGraph version issue.

**Solution:**
```bash
pip install --upgrade pyqtgraph
```

### "Permission denied" Errors

**Problem:** You don't have write permissions in the folder.

**Solution:**
- **Windows:** Right-click the WhenMathPrays folder → Properties → Security → Edit → Give yourself "Full control"
- **Mac/Linux:** Try installing in your home directory instead of system folders

---

## Getting Help

If you encounter problems not listed here:

1. **Check the GitHub Issues page:**
   https://github.com/CuriousOne23/WhenMathPrays/issues
   
   Search for your error message - someone may have already solved it.

2. **Create a new issue:**
   - Click "New Issue"
   - Describe:
     - Your operating system (Windows/Mac/Linux)
     - What step you're on
     - The exact error message
     - What you've already tried
   
3. **Include diagnostic information:**
   Run these commands and include the output:
   ```bash
   python --version
   pip list
   ```

---

## Next Steps

Once installation is complete, read:
- **`interactive_editor_user_guide.md`** - Learn how to use all the features
- **`WHY_THIS_MATTERS.md`** - Understand the purpose of the GRP model
- **`docs/fidelity_asymmetry_research_questions.md`** - Dive into the mathematics

---

## Uninstalling

If you want to remove the Interactive Editor:

1. **Delete the WhenMathPrays folder:**
   - Just delete the folder you created in Step 3

2. **Uninstall Python (optional):**
   - **Windows:** Control Panel → Programs → Uninstall Python
   - **Mac:** `rm -rf /Library/Frameworks/Python.framework/Versions/3.12`
   - **Linux:** `sudo apt remove python3` (or equivalent for your distro)

3. **Uninstall Git (optional):**
   - **Windows:** Control Panel → Programs → Uninstall Git
   - **Mac:** `brew uninstall git`
   - **Linux:** `sudo apt remove git` (or equivalent)

---

## Quick Reference Card

**To run the editor:**
```bash
# Windows
cd C:\Users\YourName\Documents\WhenMathPrays
python tools\interactive_editor.py data\single_dating_to_love_M1.csv

# Mac/Linux
cd ~/Documents/WhenMathPrays
python3 tools/interactive_editor.py data/single_dating_to_love_M1.csv
```

**To update to the latest stable version:**
```bash
cd /path/to/WhenMathPrays
git fetch origin
git checkout v2.2-stable
pip install -r requirements.txt --upgrade
```

**To switch scenarios:**
```bash
python tools/interactive_editor.py data/single_dating_to_love_M2.csv
```

Available scenarios in the `data/` folder:
- `single_dating_to_love_M1.csv` - Ann's dating journey
- `single_dating_to_love_M2.csv` - Fred's dating journey
- `exes_reconnecting.csv` - Reconnecting after breakup

---

## System Requirements

**Minimum:**
- **OS:** Windows 10+, macOS 10.14+, Ubuntu 20.04+ (or equivalent Linux)
- **RAM:** 4 GB
- **Disk:** 500 MB free space
- **Display:** 1280x720 resolution
- **Python:** 3.9 or newer

**Recommended:**
- **RAM:** 8 GB or more
- **Display:** 1920x1080 or higher (better for viewing plots)
- **Python:** 3.12 (latest stable)

---

## License and Credits

**Project:** WhenMathPrays - Gamma Relational Persona (GRP) Model  
**Creator:** CuriousOne23  
**License:** Open Source (see LICENSE file)  
**Repository:** https://github.com/CuriousOne23/WhenMathPrays

---

*If you successfully install and use the Interactive Editor, please consider leaving feedback via GitHub Issues or contributing to the project!*
