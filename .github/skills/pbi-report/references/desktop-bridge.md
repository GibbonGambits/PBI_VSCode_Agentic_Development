# Reloading and looking at pages yourself: Microsoft's Desktop Bridge (optional)

You cannot see a report page. Without help you must ask the developer to reload the project in Power BI Desktop and look. With Microsoft's Desktop Bridge you reload the project and take a picture of every page yourself, and then look at the pictures.

Everything in the template works without it. It is an optional step.

## Before you use it

- It is treated as a preview feature. Microsoft's release notes of September 2026 list it without a preview label; Microsoft's page on editing project files still calls it a preview. The developer installs its tools, and that is the yes: use it whenever the script finds them, without asking and without a row in the brief.
- It needs Windows and the Desktop option "Enable external tool access to Power BI Desktop through secure local APIs" (File > Options and settings > Options > Security). Microsoft says that option is on by default, and that an administrator can switch it off. Microsoft names no minimum version of Power BI Desktop; its release notes first list the Desktop Bridge in June 2026 (version 2.155.756.0), so expect it from that version on.
- It needs two command-line tools that Microsoft publishes on npm: `@microsoft/powerbi-desktop-bridge-cli` and `@microsoft/powerbi-report-authoring-cli` (the second is a public preview). The developer installs them. Never install them yourself.
- Check at the start of every task: run `status`. When it says a tool is not installed, it prints the setup lines; show them to the developer at the start of your answer, then carry on without the Bridge. The lines, for a terminal on Windows:

```
winget install OpenJS.NodeJS.LTS
npm.cmd install -g @microsoft/powerbi-desktop-bridge-cli @microsoft/powerbi-report-authoring-cli
```

  After the first line the developer closes and reopens VS Code. In PowerShell the second line says `npm.cmd`, not `npm`: Windows often blocks npm's PowerShell script.
- When Desktop does not have the project open, open it yourself with `open`, without asking. It starts Power BI Desktop on the project's own `.pbip` file, and only when no Desktop window has the project open already.

## The commands

```
python scripts/desktop_bridge.py status .
python scripts/desktop_bridge.py open .
python scripts/desktop_bridge.py reload .
python scripts/desktop_bridge.py reload . --with-model
python scripts/desktop_bridge.py screenshots .
python scripts/desktop_bridge.py clean "<folder of pictures>"
```

1. `status` says whether Desktop has this project open, and whether Desktop holds unsaved changes.
2. `open` opens the project in Desktop when no window has it. Desktop then shows the files as they are, so no reload is needed straight after it.
3. `reload` first runs the project check and stops on errors. It stops when Desktop has unsaved changes, because a reload throws them away: ask the developer to save, then run it again. Use `--with-model` when model files (`.tmdl`) changed: without it a changed measure is not reloaded.
4. `screenshots` writes one picture for each page into a temporary folder outside the project, and prints the page name beside each file.
5. Look at every picture of a page you changed. Look for: text that is cut off, visuals that overlap or leave the page, a visual that shows an error icon or is empty, a title or a number format that is wrong, a slicer that is too small for its text. A visual with an error icon after a measure changed means the DAX is wrong: fix it before you go on.
6. `clean` deletes the pictures. Always run it when you have looked: a picture can show data.

Exit code 3 means "not available here": no Windows, or the tools are not installed. Then carry on the old way: ask the developer to reload and to look at the pages you name.

## What it does not do

- It does not refresh data. After a reload the numbers on a page may be old; a measure you just changed shows its new result only for data that is already loaded. Say so when you report.
- It does not read the error box Desktop shows when a file fails to load. If the reload fails, or a picture is missing, ask the developer what Desktop says.
- It cannot query the model. Facts about the data: the file data-facts.md of the skill `pbi-semantic-model`.
- A reload resets filters and selections in the open Desktop window.
- Microsoft says a reload does not cover every file: `definition.pbir`, `mobileState.json`, `semanticModelDiagramLayout.json` and a `report.json` beside `definition.pbir` are not to be edited outside Desktop.
- Header icons always show in Desktop while a report is edited. The "off" setting applies in reading view only, so a picture still shows them.

## What the script never does

It never publishes, deploys, packs, opens a workspace or installs a tool. It calls Microsoft's tools for exactly four things: status, opening this project's own `.pbip` file, reload, and pictures of pages.

## Without the Bridge, with Desktop's own reload

Power BI Desktop from August 2026 has the preview feature "Detect and reload external PBIP changes" (File > Options and settings > Options > Preview features). With it on, Desktop shows the banner "Apply external changes" when files change, and the developer selects it. Otherwise the developer closes and reopens the project.

## Status of this guidance

`status` and `screenshots` ran on a developer's computer in November 2026. `open` and `reload --with-model` follow the tools' own code and documentation and have not been run yet. The tests replace the tools with stand-ins.

## Sources

Read on 11 November 2026. Restated in this template's own words.

- Microsoft Learn: "Power BI Desktop Bridge overview" (https://learn.microsoft.com/power-bi/developer/agentic/power-bi-desktop-bridge-overview); "Edit PBIP files outside Power BI Desktop" (https://learn.microsoft.com/power-bi/developer/projects/projects-external-editing); the Power BI Desktop update archive, June and September 2026 (https://learn.microsoft.com/power-bi/fundamentals/desktop-latest-update-archive).
- The two npm packages named above (MIT licence): their README files and change logs.
- Microsoft's `skills-for-fabric` repository (MIT), skill `powerbi-report-cli`: its notes on Power BI Desktop, on the check for unsaved changes before a reload, and on keeping pictures outside the project.
- `Mofaji/Agentic-PBIP-Template` (MIT) was read to learn how the calls work. None of its code is used: this template stays Python standard library only.

Checklist items: 49, 67
