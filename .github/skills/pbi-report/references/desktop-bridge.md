# Reloading and looking at pages yourself: Microsoft's Desktop Bridge (optional)

You cannot see a report page. Without help you must ask the developer to reload the project in Power BI Desktop and look. With Microsoft's Desktop Bridge you reload the project and take a picture of every page yourself, and then look at the pictures.

Everything in the template works without it. It is an optional step.

## Before you use it

- It is treated as a preview feature. Microsoft's release notes of September 2026 list it without a preview label; Microsoft's page on editing project files still calls it a preview. So use it only after the developer's yes, and record that yes in section 11 of `docs/report-brief.md`.
- It needs Windows, Power BI Desktop of June 2026 (2.155.756.0) or later, and the Desktop option "Enable external tool access to Power BI Desktop through secure local APIs" (File > Options and settings > Options > Security). Microsoft says that option is on by default, and that an administrator can switch it off.
- It needs two command-line tools that Microsoft publishes on npm: `@microsoft/powerbi-desktop-bridge-cli` and `@microsoft/powerbi-report-authoring-cli` (the second is a public preview). The developer installs them. Never install them yourself.
- The developer opens the project in Power BI Desktop. The script never starts Desktop.

## The four commands

```
python scripts/desktop_bridge.py status .
python scripts/desktop_bridge.py reload .
python scripts/desktop_bridge.py reload . --with-model
python scripts/desktop_bridge.py screenshots .
python scripts/desktop_bridge.py clean "<folder of pictures>"
```

1. `status` says whether Desktop has this project open, and whether Desktop holds unsaved changes.
2. `reload` first runs the project check and stops on errors. It stops when Desktop has unsaved changes, because a reload throws them away: ask the developer to save, then run it again. Use `--with-model` when model files (`.tmdl`) changed.
3. `screenshots` writes one picture for each page into a temporary folder outside the project, and prints the page name beside each file.
4. Look at every picture of a page you changed. Look for: text that is cut off, visuals that overlap or leave the page, a visual that shows an error icon or is empty, a title or a number format that is wrong, a slicer that is too small for its text.
5. `clean` deletes the pictures. Always run it when you have looked: a picture can show data.

Exit code 3 means "not available here": no Windows, or the tools are not installed. Then carry on the old way: ask the developer to reload and to look at the pages you name.

## What it does not do

- It does not refresh data. After a reload the numbers on a page may be old; a measure you just changed shows its new result only for data that is already loaded. Say so when you report.
- It does not read the error box Desktop shows when a file fails to load. If the reload fails, or a picture is missing, ask the developer what Desktop says.
- It cannot query the model. Facts about the data: the file data-facts.md of the skill `pbi-semantic-model`.
- A reload resets filters and selections in the open Desktop window.
- Microsoft says a reload does not cover every file: `definition.pbir`, `mobileState.json`, `semanticModelDiagramLayout.json` and a `report.json` beside `definition.pbir` are not to be edited outside Desktop.
- Header icons always show in Desktop while a report is edited. The "off" setting applies in reading view only, so a picture still shows them.

## What the script never does

It never publishes, deploys, packs, opens a workspace, starts Desktop or installs a tool. It calls Microsoft's tools for exactly three things: status, reload, and pictures of pages.

## Without the Bridge, with Desktop's own reload

Power BI Desktop from August 2026 has the preview feature "Detect and reload external PBIP changes" (File > Options and settings > Options > Preview features). With it on, Desktop shows the banner "Apply external changes" when files change, and the developer selects it. Otherwise the developer closes and reopens the project.

## Status of this guidance

Written, not run. Power BI Desktop could not be run where this template was built. The calls follow Microsoft's documentation of the two tools; the tests replace the tools with stand-ins.

## Sources

Read on 11 November 2026. Restated in this template's own words.

- Microsoft Learn: "Power BI Desktop Bridge overview" (https://learn.microsoft.com/power-bi/developer/agentic/power-bi-desktop-bridge-overview); "Edit PBIP files outside Power BI Desktop" (https://learn.microsoft.com/power-bi/developer/projects/projects-external-editing); the Power BI Desktop update archive, June and September 2026 (https://learn.microsoft.com/power-bi/fundamentals/desktop-latest-update-archive).
- The two npm packages named above (MIT licence): their README files and change logs.
- Microsoft's `skills-for-fabric` repository (MIT), skill `powerbi-report-cli`: its notes on Power BI Desktop, on the check for unsaved changes before a reload, and on keeping pictures outside the project.
- `Mofaji/Agentic-PBIP-Template` (MIT) was read to learn how the calls work. None of its code is used: this template stays Python standard library only.

Checklist items: 49, 67
