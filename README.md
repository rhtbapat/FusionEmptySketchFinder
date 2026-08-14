# Empty Sketch Finder — Autodesk Fusion Add-In

> Quickly find and clean up empty sketches across an Autodesk Fusion design — including sketches inside nested components.

---

## ✨ Features

* **Find empty sketches** — scans the active Fusion design for sketches that contain no sketch geometry
* **Entire-design scan** — searches sketches across all components in the design, not just the root component
* **Component-aware results** — displays each empty sketch together with the component it belongs to
* **Bulk cleanup** — delete all detected empty sketches in a single operation
* **Safety confirmation** — asks for confirmation before permanently deleting sketches
* **Deletion status** — reports how many sketches were successfully removed and identifies any that could not be deleted
* **Simple workflow** — runs as a single command without additional configuration or settings
* **Fusion toolbar integration** — adds **Find Empty Sketches** to the **Solid → Modify** panel

---

## 🔍 What Is Considered an Empty Sketch?

Empty Sketch Finder checks the sketch entities contained in each sketch.

A sketch is considered empty when it contains no:

* Lines
* Arcs
* Circles
* Ellipses
* Elliptical arcs
* Fitted splines
* Fixed splines
* Additional sketch points

The scan runs through **all components** in the active Fusion design, making it useful for cleaning up larger assemblies and component-based models.

---

## 🧰 Workflow

When **Find Empty Sketches** is run:

1. The add-in scans every component in the active design
2. All empty sketches are collected
3. A dialog displays:

   * The total number of empty sketches found
   * Each sketch name
   * The component containing the sketch
4. Click **OK** to continue with deletion, or **Cancel** to leave the design unchanged
5. A second confirmation is shown before any sketches are deleted
6. After cleanup, the add-in reports the deletion results

If no empty sketches are found, the add-in simply reports that the design is already clean.

---

## 🚀 Installation

1. Download or clone this repository

2. Place the `FusionEmptySketchFinder` folder containing:

   * `EmptySketchFinder.py`
   * `EmptySketchFinder.manifest`

   in your Fusion add-ins directory:

   * **Mac:** `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns/`
   * **Windows:** `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns/`

3. In Fusion, open **Utilities → Scripts and Add-Ins** (or press `Shift+S`)

4. Switch to the **Add-Ins** tab

5. Select **EmptySketchFinder**

6. Click **Run**

The included manifest is currently configured with `runOnStartup` set to `false`, so the add-in must be started from **Scripts and Add-Ins** after launching Fusion unless you change that setting.

---

## 🎯 How to Use

1. Open a Fusion design
2. Go to the **Solid** workspace
3. Open the **Modify** panel
4. Click **Find Empty Sketches**
5. Review the list of detected empty sketches and their component locations
6. Click:

   * **Cancel** to close without making changes
   * **OK** to proceed with deleting all detected empty sketches
7. Confirm the deletion when prompted

The add-in will report how many sketches were successfully deleted.

---

## 💡 Why Use It?

Empty sketches can accumulate while experimenting with features, importing geometry, restructuring components, or deleting old sketch geometry.

Although they may not affect the final model, unnecessary sketches can:

* Clutter the Browser
* Make large designs harder to navigate
* Leave behind unused design objects
* Make model cleanup more tedious

Empty Sketch Finder provides a quick way to identify and remove them throughout the complete design.

---

## ⚠️ Notes

* A Fusion design must be active before running the command.
* The add-in searches sketches across **all components** in the active design.
* Deletion is performed in bulk — individual sketches cannot currently be selected for deletion from the results dialog.
* You are shown the sketch names and component locations before deletion begins.
* A second warning is displayed before any sketches are permanently removed.
* Sketch deletion cannot be undone through the add-in itself, so review the list before confirming.
* The current add-in version is `1.0.0`.

---

## 📄 License

MIT License — free to use, modify, and distribute.
