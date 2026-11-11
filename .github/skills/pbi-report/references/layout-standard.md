# The layout standard

Copilot cannot see a page. It changes positions blind. So layout is set by numbers that `python scripts/check_project.py .` can check. The "Layout" rules in the skill still apply; this file adds the numbers.

A value in the brief always wins. The theme sets no page size and no spacing.

## The numbers

| Number | Default | For a 1920 x 1080 page |
|---|---|---|
| Page size, in pixels | 1280 x 720 | 1920 x 1080 |
| Outer margin | 24 | 32 |
| Gap between visuals | 16 | 24 |
| Grid step | 8 | 8 |
| Title | Top-left at x 24, y 24, in a band 56 high | At x 32, y 32, band 72 high |
| Content starts at | y 96 (24 + 56 + 16) | y 128 (32 + 72 + 24) |
| 1 to 3 slicers | In the title band, at its right end, each 160 x 56, one gap apart | Each 232 x 64 |
| 4 or more slicers | One column at the left, 208 wide | 312 wide |

- An existing report keeps its own page size. Write it in section 2 of the brief. For a size other than these two, the brief must also give the margin and the gap; if it does not, ask.
- Every x, y, width and height is a multiple of the grid step.
- Left, top and right margins equal the margin. The bottom margin is at least the margin: a page need not be full.
- Slicers sit in the same place on every page (item 61).
- A tooltip page has its own small canvas. The margin, gap, grid and page-size rules do not apply to it.

## What the script checks

| Code | Rule | Level |
|---|---|---|
| G001 | A visual reaches outside the page | fail |
| G002 | Two data visuals overlap | fail |
| G003 | x, y, width or height is not on the grid | warn |
| G004 | Outer margins differ from the margin | warn |
| G005 | Visuals of the same kind in one row have different heights | warn |
| G006 | The gap between neighbours differs from the gap | warn |
| G007 | The page size differs from the brief or the default | warn |
| G008 | A rotated visual: its position is not checked | note |

- A "data visual" is a visual with fields. Shapes, images, text boxes and buttons have none, so a background shape behind a chart is not an overlap.
- Not an overlap either: a visual marked hidden, a visual that a bookmark hides, and a group against its own members.
- A visual inside a group is compared only with the other members of that group, because it is not known where a member's position counts from. So when a page has groups, a clean G002 does not prove item 49's "0 overlapping visuals": the developer looks at that page.
- Checklist item 49 asks for 0 overlapping visuals, and for a review when 3 or more visuals on a page are off the grid or badly aligned.
- An exception counts only when section 10 of the brief lists the code, the page and the visual with a reason. A full-page background shape is listed with `G004`.

## What a position change can touch

| Thing | What is known | What to do |
|---|---|---|
| Groups | A member names its group. Microsoft's schema does not say whether a member's x and y count from the page or from the group | Never move or resize a group or a visual inside one. Tell the developer; they do it in Power BI Desktop |
| Bookmarks | Microsoft's bookmark schema holds no position or size. A bookmark does store which visuals are hidden | No bookmark file changes. Do not un-stack visuals that a bookmark shows one at a time |
| Phone layout | Each visual's phone position is its own `mobile.json`. `mobileState.json` must not be edited outside Desktop | Leave both alone. Ask the developer to look at the phone layout |
| Tooltip pages | Own small canvas | Never re-lay them out |
| Drillthrough pages | A normal canvas; nothing in the schema ties its back button or filters to positions | Same rules as other pages |
| Tab order and stacking order | Microsoft asks that tab order follows the reading order | Do not change `tabOrder` or `z`. Ask the developer to check the tab order after visuals move |
| Rotated visuals | Their real bounds are not known from the numbers | Leave alone and say so |

## How to change positions

1. Run `python scripts/list_visuals.py . --page <page>` and `python scripts/check_project.py .`.
2. Work out each new x, y, width and height by arithmetic from the numbers above. Show the developer the sums and the old and new values, and wait for a yes.
3. Apply with `python scripts/set_positions.py . --dry-run --move "<page>/<visual>=<x>,<y>,<width>,<height>"`, then without `--dry-run`. `--snap` only rounds existing numbers to the grid. The script changes the four numbers and nothing else, and refuses groups, members, rotated visuals and anything that would leave the page.
4. Run the check again.
5. Name the pages that changed and ask the developer to reload the project in Power BI Desktop and look at each one. The script prints the list. Never say a page looks right from the files alone.

## Sources

Read on 11 November 2026. Restated in this template's own words.

- Checklist items 49 to 53, 61 and 70 were read; the standard gives numbers for items 20, 49, 52 and 61.
- Microsoft Learn: "Apply page size and settings in a Power BI report" (16:9 is the default type; 1280 x 720 is its first size); "Use gridlines and snap-to-grid"; "Group visuals"; "Create report bookmarks"; "Create tooltips based on report pages"; "Mobile-optimized reports"; "Design reports for accessibility" (tab order); "Power BI Desktop project report folder". Microsoft Learn gives no pixel numbers for margin, gap or grid.
- Microsoft's `skills-for-fabric` repository (MIT), skill `powerbi-report-cli`, `references/design/layout.md`: the 8-pixel grid; 24 margin and 16 gap on a 1280 page; 32 and 24 on a 1920 page; a header 72 high on a 1920 page; slicers 56 high (1280) or 64 high (1920), about 12% of the page wide, beside the title when there are 1 to 3, or in a left column of about 206 (1280) or 310 (1920) when there are more; no overlap of data visuals. Widths are put on the grid here: 160, 232, 208, 312.
- This template's own arithmetic, approved by the owner and not from a source: a title band 56 high on a 1280 page (the height of the slicers that share it); content starting one gap below the band, at y 96 or y 128; one single gap everywhere (G006).
- Microsoft's report schemas: `visualContainer` (position, group, hidden), `visualConfiguration` (fields), `page` (tooltip and drillthrough pages), `bookmark`, `visualContainerMobileState`.
- Kurt Buhler's `power-bi-agentic-development` repository (GPL-3.0): ideas only, on equal margins and gaps. No text was copied.

Where sources disagree:

- Size of a new page: Microsoft's report skill starts at 1920 x 1080; Microsoft Learn lists 1280 x 720 first. The owner chose 1280 x 720 and keeps 1920 x 1080 as the second set.
- Gaps: Microsoft's report skill allows two sizes on a page, a tighter one inside a group of visuals and a wider one between groups (16 and 24). This standard asks for one gap, so G006 is stricter than Microsoft; it is a warning.
- Where content starts on a 1920 page: Microsoft's skill puts it directly under the header, at y 104. This standard leaves one gap, y 128.

Not confirmed from Microsoft: where a group member's position counts from; whether an automatically made phone layout changes when desktop positions change.

Checklist items: 20, 49, 52, 61
