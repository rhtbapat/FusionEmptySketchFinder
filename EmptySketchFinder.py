# =============================================================================
# Empty Sketch Finder
# =============================================================================
# Author:      Rohit Bapat
# Email:       rhtbapat@gmail.com
# Command:     Empty Sketch Finder
# Description: A Fusion add-in that searches for empty sketches in the document
#              and provides an option to delete all empty sketches at once.
# =============================================================================

import adsk.core, adsk.fusion
_static_handlers = []
CMD_ID   = "emptySketchFinderCmd"
CMD_NAME = "Find Empty Sketches"
CMD_DESC = "Lists and deletes empty sketches in the active design"
PANEL_ID = "SolidModifyPanel"


def get_design():
    return adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)


def find_empty_sketches(design):
    results = []
    for comp in design.allComponents:
        for sk in comp.sketches:
            c = sk.sketchCurves
            total = (c.sketchLines.count + c.sketchArcs.count +
                     c.sketchCircles.count + c.sketchEllipses.count +
                     c.sketchEllipticalArcs.count +
                     c.sketchFittedSplines.count +
                     c.sketchFixedSplines.count +
                     sk.sketchPoints.count - 1)
            if total <= 0:
                results.append({"sketch": sk, "name": sk.name, "loc": comp.name})
    return results


class CommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self): super().__init__()
    def notify(self, args):
        try:
            cmd = args.command
            cmd.isAutoExecute = True
            onExec    = CommandExecuteHandler()
            onDestroy = CommandDestroyHandler()
            cmd.execute.add(onExec)
            cmd.destroy.add(onDestroy)
            _static_handlers.extend([onExec, onDestroy])
        except:
            import traceback
            adsk.core.Application.get().userInterface.messageBox(traceback.format_exc(), CMD_NAME)


class CommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self): super().__init__()
    def notify(self, args):
        ui     = adsk.core.Application.get().userInterface
        design = get_design()
        try:
            if not design:
                ui.messageBox("No active Fusion design found.", CMD_NAME)
                return

            sketches = find_empty_sketches(design)

            # ---- No empty sketches ----
            if not sketches:
                ui.messageBox("No empty sketches found in this design.", CMD_NAME)
                return

            # ---- Build list and ask user ----
            rows = ["Found {} empty sketch(es):".format(len(sketches)), ""]
            for i, item in enumerate(sketches, 1):
                rows.append("  {}. {}  [{}]".format(i, item["name"], item["loc"]))
            rows.append("")
            rows.append("Click OK to delete all, or Cancel to close.")
            msg = "\n".join(rows)

            # ---- OK = Delete All, Cancel = Close ----
            result = ui.messageBox(
                msg, CMD_NAME,
                adsk.core.MessageBoxButtonTypes.OKCancelButtonType,
                adsk.core.MessageBoxIconTypes.InformationIconType)

            if result != adsk.core.DialogResults.DialogOK:
                return

            # ---- Confirm before deleting ----
            confirm = ui.messageBox(
                "Are you sure you want to delete all {} empty sketch(es)? This cannot be undone.".format(len(sketches)),
                CMD_NAME,
                adsk.core.MessageBoxButtonTypes.OKCancelButtonType,
                adsk.core.MessageBoxIconTypes.WarningIconType)

            if confirm != adsk.core.DialogResults.DialogOK:
                return

            # ---- Delete all ----
            count  = 0
            failed = []
            for item in sketches:
                if item["sketch"].deleteMe():
                    count += 1
                else:
                    failed.append(item["name"])

            if failed:
                ui.messageBox("{} deleted. Could not delete: {}".format(count, ", ".join(failed)), CMD_NAME)
            else:
                ui.messageBox("{} sketch(es) deleted successfully.".format(count), CMD_NAME)

        except:
            import traceback
            ui.messageBox(traceback.format_exc(), CMD_NAME)


class CommandDestroyHandler(adsk.core.CommandEventHandler):
    def __init__(self): super().__init__()
    def notify(self, args): pass


def run(context):
    global _static_handlers
    _static_handlers = []
    app = adsk.core.Application.get()
    ui  = app.userInterface
    try:
        old = ui.commandDefinitions.itemById(CMD_ID)
        if old: old.deleteMe()
        cmdDef = ui.commandDefinitions.addButtonDefinition(CMD_ID, CMD_NAME, CMD_DESC)
        onCreate = CommandCreatedHandler()
        cmdDef.commandCreated.add(onCreate)
        _static_handlers.append(onCreate)
        panel = ui.allToolbarPanels.itemById(PANEL_ID)
        if panel:
            ctrl = panel.controls.addCommand(cmdDef)
            ctrl.isPromotedByDefault = False
    except:
        import traceback
        ui.messageBox(traceback.format_exc(), "EmptySketchFinder - Load Error")


def stop(context):
    global _static_handlers
    app = adsk.core.Application.get()
    ui  = app.userInterface
    try:
        panel = ui.allToolbarPanels.itemById(PANEL_ID)
        if panel:
            ctrl = panel.controls.itemById(CMD_ID)
            if ctrl: ctrl.deleteMe()
        cmdDef = ui.commandDefinitions.itemById(CMD_ID)
        if cmdDef: cmdDef.deleteMe()
    except:
        import traceback
        ui.messageBox(traceback.format_exc(), "EmptySketchFinder - Stop Error")
    finally:
        _static_handlers = []
