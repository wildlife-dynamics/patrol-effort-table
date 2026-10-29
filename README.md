# Patrol Effort Table Workflow

## Introduction

This workflow helps you to measure and compare **patrol effort** across your rangers, teams, patrol types, or time periods by turning patrol tracks and patrol legs from **EarthRanger** into a configurable summary table.

**What this workflow does:**
- Downloads patrol observations and patrol legs (the segments a patrol is made of, with their team, members and assets) from EarthRanger for a chosen time range
- Builds a configurable **summary table** of patrol effort per category (per ranger, team, member, asset, patrol type, or patrol serial number), per time period, or per region, with metrics such as patrol count, patrol days, distance, duration, area covered, active and elapsed leg duration, leg count, and member-days
- Optionally splits the table into per-group dashboard views — by ranger, team, member, asset, patrol type, patrol serial number, a time period such as month, or a **spatial feature group** (regions defined in EarthRanger)

**Who should use this:**
- Conservation managers monitoring patrol coverage and field effort
- Protected-area supervisors comparing effort across rangers, patrol types, periods, or regions
- Researchers analyzing how much patrolling happened, where, and when

Looking for the maps that used to accompany this table? They are available as separate workflows: the **Patrol Trajectory & Event Map** and the **Patrol Track Density Map**.

---

## Prerequisites

Before using this workflow, you need:

1. **Ecoscope Desktop** installed on your computer
   - If you haven't installed it yet, please follow the installation instructions for Ecoscope Desktop

2. **EarthRanger Data Source** configured in Ecoscope Desktop
   - You must have already set up a connection to your EarthRanger server
   - Your data source should be configured with proper authentication credentials
   - You'll need to know the name of your configured data source (e.g., `"mep_dev"`)

3. **Patrols recorded in EarthRanger**
   - At least one **patrol type** must exist in your EarthRanger site (e.g., `"ecoscope_patrol"`)
     - You can find them at `https://<your-site>.pamdas.org/admin/activity/patroltype/`
   - Patrols must be linked to a **patrol subject** (the ranger) for the per-ranger summary to work

4. **Patrol leg roster** (optional, only for the Team, Member and Asset groupers and the Member-days metric)
   - EarthRanger records each patrol as one or more **legs**; on sites with the patrol roster feature, every leg also carries a **team**, its **members** and its **assets** (vehicles, equipment)
   - Without it, the Team / Member / Asset groupers show a single `None` group and **Member-days** is blank — every other metric is unaffected

5. **Spatial feature groups** (optional, only for the Spatial grouper)
   - To split the table by region, your EarthRanger site must define at least one **spatial feature group** (a named set of region polygons)
   - You can find them in your EarthRanger Admin site under **Mapping → Spatial Feature Groups**

---

## Installation

1. Select "Workflow Templates" tab
2. Click "+ Add Template"
3. Copy and paste this URL https://github.com/wildlife-dynamics/patrol-effort-table and wait for the workflow template to be downloaded and initialized
4. The template will now appear in your available template list

---

## Configuration Guide

### Basic Configuration

#### 1. Workflow Details
Add information to help differentiate this workflow run from others.

- **Workflow Name** (required): A short, descriptive name for this run
  - Example: `"Patrol Effort Table"`
- **Workflow Description** (optional): Additional context about this run
  - Example: `"Per-category patrol effort summary table."`

#### 2. Data Source
Select the EarthRanger connection to pull patrols from.

- **Data Source** (required): The name of one of your configured EarthRanger data sources
  - Example: `"mep_dev"`
  - Note: This must match a data source you've already configured in Ecoscope Desktop

#### 3. Time Range
Choose the period of time to analyze. Only patrols within this window will be included.

- **Since** (required): The start date and time
  - Example: `2015-01-10T00:00:00`
- **Until** (required): The end date and time
  - Example: `2015-02-28T23:59:59`
- **Timezone** (required): The timezone used to interpret your dates and to display times in the outputs
  - Example: `Africa/Nairobi (UTC+03:00)` or `UTC (UTC+00:00)`

#### 4. Patrol Types
Choose which patrols to include.

- **Patrol Types** (optional): One or more patrol types to analyze
  - Example: `["ecoscope_patrol"]`
  - Note: The available options are loaded from your selected data source. Leave empty to include all patrol types.

#### 5. Group Data (optional)
Split the summary table into separate per-group dashboard views. Leave empty for a single combined view.

- **Category** grouper: Group by a data column, chosen in its **Index Name** dropdown
  - Options: `Patrol Serial Number`, `Patrol Type`, `Patrol Subject`, `Team`, `Member`, `Asset`
  - Note: `Team`, `Member` and `Asset` come from the patrol leg roster. A patrol leg with several members (or assets) counts in full for each of them — grouping by `Member` gives every member of a leg its whole distance and duration, and splits **Member-days** between them.
- **Time** grouper: Group by a time period
  - Options: `Year`, `Month`, `Year and Month`, `Day of the year`, `Day of the month`, `Day of the week`, `Hour`, `Date`
- **Spatial** grouper: Group by region using a spatial feature group from your EarthRanger site
  - **Spatial Regions**: The name of the spatial feature group whose polygons define the regions
  - Note: The available options are loaded from your selected data source. Each patrol track segment is assigned to the region it falls inside, and one view is produced per region containing data.
- Note: You can add more than one grouper (e.g., Patrol Subject **and** Month) to split by every combination.

#### 6. Patrol Effort Summary
Configure the summary table.

- **Summarize by**: What becomes the table's rows. Works like **Group Data** — add one or more of:
  - **Category**: an **Index Name** of `Patrol Subject` (default), `Patrol Type`, `Patrol Serial Number`, `Team`, `Member`, or `Asset`
  - **Time**: a time period such as `Year`, `Month`, `Year and Month`, `Day of the week`, `Hour`, or `Date`
  - **Spatial**: the regions of a **spatial feature group** from your EarthRanger site
  - You may add more than one to group rows by a combination (e.g., Patrol Subject and Month). Leave empty for a single overall row.
- **Summary Metrics** (required): The columns shown for each category. Add one or more of:
  - **Patrol Count**: Number of distinct patrols
  - **Patrol Days**: Number of distinct days on which patrolling occurred
  - **Total Distance**: Distance travelled along the patrol tracks, in `Kilometers (km)` or `Meters (m)`
  - **Total Duration**: Time from the first to the last recorded position of each patrol, in `Hours (h)` or `Days (d)`
  - **Area Covered (Merged)**: Ground area covered, with overlapping patrol swaths merged (set **Swath Width (m)**)
  - **Area Covered (Unmerged)**: Ground area covered, summed per patrol without merging overlaps
  - **Active Duration**: Time spent on patrol legs (the scheduled start to end of each leg, gaps between legs excluded), in `Hours (h)` or `Days (d)`
  - **Elapsed Duration**: Time from the start of a patrol's first leg to the end of its last leg, in `Hours (h)` or `Days (d)`
  - **Leg Count**: Number of distinct patrol legs
  - **Member-days**: Number of members on each leg multiplied by the calendar days the leg spans, summed; blank on sites without the patrol leg roster
  - Default: `Patrol Count`, `Total Distance`, `Total Duration`, `Patrol Days`, `Area Covered (Merged)`, `Area Covered (Unmerged)`, `Active Duration`
  - **Custom**: An escape hatch — give the column a **Display Name**, then pick any **Statistic** (count, sum, mean, median, min, max, nunique) over any **Column**, set **Decimal Places**, and optionally **Convert Units**
    - When **Convert Units** is on, the target unit is appended to the column header automatically — e.g., a metric named `Avg Leg Distance` converted to `km` appears as `Avg Leg Distance (km)`

---

### Advanced Configuration

These optional settings are hidden by default in Ecoscope Desktop and can be revealed by expanding the "Advanced Configurations" section of the relevant card.

#### Patrol Filtering (Patrol Types card)

- **Patrol Status**: Restrict the analysis to patrols in specific states
  - Default: `Done`
  - Options: `Active`, `Overdue`, `Done`, `Cancelled`
  - Note: Leave empty to include patrols of all statuses. Patrols that start before or end after your time range are always included as long as they overlap it.

#### Filter Data

- **Bounding Box**: Latitude/longitude box that patrol observations must fall inside
  - Defaults to the whole world: `min_y: -90`, `max_y: 90`, `min_x: -180`, `max_x: 180`
- **Filter Exact Point Coordinates**: A list of `(latitude, longitude)` pairs to exclude
  - Default: excludes common GPS-error coordinates such as `(0, 0)` "null island"
  - Example: adding `{y: 0.0, x: 0.0}` hides any observation recorded exactly at the equator/prime meridian intersection
- **Trajectory Filter**: Removes outlier patrol track segments so noisy GPS jumps don't inflate distance, duration, and coverage
  - **Minimum / Maximum Segment Length (Meters)**: Defaults `0.001` / `100000`
  - **Minimum / Maximum Segment Duration (Seconds)**: Defaults `1` / `172800`
  - **Minimum / Maximum Segment Speed (Kilometers per Hour)**: Defaults `0.01` / `500`

---

## Running the Workflow

Once you've configured all the settings:

1. **Review your configuration**
   - Double-check your time range, data source, and the patrol types you selected

2. **Save and run**
   - Click "Submit" and the workflow will show up in the "My Workflows" table in Ecoscope Desktop
   - Click "Run" and the workflow will begin processing

3. **Monitor progress and wait for completion**
   - You'll see status updates as the workflow runs
   - Processing time depends on:
     - The size of your date range
     - The number of patrols in the system
     - The number of rangers active in the period
   - The workflow completes with status "Success" or "Failed"

---

## Understanding Your Results

After the workflow completes successfully, you'll see a dashboard with the summary table. If you set one or more groupers in **Group Data**, a view selector appears at the top so you can switch between per-group views (e.g., one per ranger, per month, or per region).

### Visual Outputs (Dashboard)

#### Patrol Effort Summary
- **Format**: Interactive sortable table
- **Features**:
  - Click any column header to sort by that metric
  - Download the table using the download button
  - One row per group value (per ranger, patrol type, time period, or region, depending on your **Summarize by** entries)
- **Columns**: One column per Summarize by entry (e.g., `Patrol Subject`, `Patrol Type`, `Month`; a Team, Member or Asset entry is headed `Patrol Team Name`, `Patrol Member Names` or `Patrol Asset Names`) followed by one column per metric you selected — the track metrics first (Patrol Count, Patrol Days, Total Distance, Total Duration, Area Covered, Custom), then the leg metrics (Active Duration, Elapsed Duration, Leg Count, Member-days)

### Grouped Outputs

If you configured groupers under **Group Data**, the table is produced once per group and a view selector lets you switch between them — for example a separate summary table for each ranger, each team member, each month in your time range, or each region of a spatial feature group.

### How the Results Are Calculated

#### Track metrics
Patrol Count, Patrol Days, Total Distance, Total Duration and the Area Covered metrics are computed from the **patrol tracks**: the sequence of GPS positions recorded during each patrol, joined into track segments. Total Duration runs from the first to the last position of a patrol, so it includes any pause between the patrol's legs. The **Trajectory Filter** decides which segments count.

#### Area covered
Each track segment is widened to a corridor of **Swath Width (m)** on either side. **Area Covered (Merged)** dissolves the corridors of all patrols in a row into one shape, so ground patrolled twice is counted once; **Area Covered (Unmerged)** adds the corridors patrol by patrol, so repeat coverage counts again.

#### Leg metrics
Active Duration, Elapsed Duration, Leg Count and Member-days are computed from the **patrol legs** EarthRanger records for each patrol (its planned start and end times, team, members and assets), not from GPS positions. Active Duration adds up the legs' own durations; Elapsed Duration spans a whole patrol from its first leg's start to its last leg's end and is credited to the row of its first leg. Member-days counts, for each leg, its members times the calendar days the leg touches. Legs are clipped to your **Time Range**.

#### Groups with several members or assets
A leg with two members belongs to both. When you group or summarize by `Member` (or `Asset`), every member receives the leg's full distance and duration, and the table's rows no longer add up to the overall total. Member-days is the exception: it is split between the members so that the column still sums correctly.

#### Regions
With a Spatial grouper, each track segment is assigned to the region it falls inside. A leg's durations and Member-days are shared between regions in proportion to the track distance its patrol covered in each; Leg Count counts a leg once in every region it touched.

---

## Common Use Cases & Examples

Here are some typical scenarios and how to configure the workflow for each:

### Example 1: Per-Ranger Effort Summary
**Goal**: Rank rangers by patrol effort with full metrics.

**Configuration**:
- **Time Range**:
  - Since: `2015-01-10T00:00:00`
  - Until: `2015-02-28T23:59:59`
  - Timezone: `Africa/Nairobi (UTC+03:00)`
- **Data Source**: `"mep_dev"`
- **Patrol Types**: `["ecoscope_patrol"]`
- **Summarize by**: `Patrol Subject`
- **Summary Metrics**: Patrol Count, Total Distance (km), Total Duration (h), Patrol Days, Area Covered (Merged & Unmerged)

**Result**:
- A per-ranger summary table with all selected metrics, sortable by any column

---

### Example 2: Split by Ranger and Month
**Goal**: Produce a separate table per ranger for each month of the period.

**Configuration**:
- **Time Range**: `2015-01-10T00:00:00` to `2015-02-28T23:59:59`, Timezone `UTC (UTC+00:00)`
- **Data Source**: `"mep_dev"`
- **Patrol Types**: `["ecoscope_patrol"]`
- **Group Data**:
  - Category grouper: `Patrol Subject`
  - Time grouper: `Month`
- **Summarize by**: `Patrol Subject`

**Result**:
- A view selector at the top of the dashboard lets you pick each ranger × month combination, each with its own summary table

---

### Example 3: Effort per Region
**Goal**: Compare patrol effort between the regions of your protected area.

**Configuration**:
- **Time Range**: `2015-01-10T00:00:00` to `2015-02-28T23:59:59`, Timezone `UTC (UTC+00:00)`
- **Data Source**: `"mep_dev"`
- **Group Data**:
  - Spatial grouper → **Spatial Regions**: the name of a spatial feature group defined in your EarthRanger site (e.g., a "Management Sectors" group)
- **Summarize by**: `Patrol Subject`
- **Summary Metrics**: Patrol Count, Total Distance (km), Total Duration (h)

**Result**:
- One summary-table view per region that contains patrol data, so you can compare effort between sectors

---

### Example 4: Custom Metrics
**Goal**: Add custom statistics to the table beyond the presets.

**Configuration**:
- **Time Range**: `2015-01-10T00:00:00` to `2015-02-28T23:59:59`, Timezone `UTC (UTC+00:00)`
- **Data Source**: `"mep_dev"`
- **Summarize by**: `Patrol Type`
- **Summary Metrics**:
  - Patrol Count
  - Custom → Statistic `nunique`, Column `patrol_serial_number`, Decimal Places `0` (labelled "Distinct Serials")
  - Custom → Statistic `mean`, Column `dist_meters`, **Convert Units** from `m` to `km` (labelled "Avg Leg Distance" — the `(km)` suffix is appended to the column header automatically)

**Result**:
- A summary table grouped by patrol type with your custom columns alongside the presets

---

### Example 5: Effort per Team with Leg Metrics
**Goal**: See one table per team, with time on legs, number of legs and member-days alongside the track metrics.

**Configuration**:
- **Time Range**: `2026-01-05T00:00:00` to `2026-01-07T00:00:00`, Timezone `UTC (UTC+00:00)`
- **Data Source**: `"mep_dev"`
- **Patrol Types**: `["ecoscope_leg_test"]`
- **Group Data**:
  - Category grouper: `Team`
- **Summarize by**: `Patrol Subject`
- **Summary Metrics**: Patrol Count, Total Distance (km), Total Duration (h), Patrol Days, Area Covered (Merged & Unmerged), Active Duration (h), Elapsed Duration (h), Leg Count, Member-days

**Result**:
- One summary-table view per team, each with a row per ranger: the track metrics first, then `Active Duration (hrs)`, `Elapsed Duration (hrs)`, `Leg Count` and `Member-days`

---

## Troubleshooting

### Common Issues and Solutions

#### Workflow fails to start
**Problem**: The workflow exits immediately or reports a connection error.

**Solutions**:
- Confirm your **Data Source** name matches a connection you've configured in Ecoscope Desktop
- Re-enter your EarthRanger password if your session has expired
- Verify the EarthRanger server is reachable from your computer (open it in a browser)
- If you're on a VPN, try a different VPN server — some endpoints return 402/502 errors when the VPN routes incorrectly

#### Summary table is empty or shows fewer rows than expected
**Problem**: The table has no rows, or some categories you expected are missing.

**Solutions**:
- Widen the **Time Range** — patrols outside the window are excluded
- Clear the **Patrol Types** field to include every type
- Set **Patrol Status** to include `Active` and `Overdue` if you're looking at an in-progress period
- Check that the missing patrols have a **patrol subject** assigned in EarthRanger — patrols without one can't be attributed to a ranger
- Widen the **Bounding Box** if you've narrowed it to a small region

#### Some regions are missing from a spatially grouped run
**Problem**: You set a Spatial grouper but fewer region views appear than the feature group defines.

**Solutions**:
- Views are only produced for regions that contain patrol data in your time range — regions with no patrolling are omitted
- Confirm the spatial feature group's polygons actually cover your patrol area (check them in EarthRanger's mapping admin)
- Widen the **Time Range** so more patrols fall inside each region

#### Team, Member or Asset show `None`, and Member-days is blank
**Problem**: Grouping by `Team`, `Member` or `Asset` gives a single `None` group, and the **Member-days** column is empty.

**Solutions**:
- Your EarthRanger site does not record a team, members and assets on patrol legs (the patrol roster feature). Ask your EarthRanger administrator whether it can be enabled
- Patrols created before the feature was enabled keep showing `None` — narrow the **Time Range** to patrols recorded after it
- Every other metric and grouper is unaffected

#### Active Duration is lower than Total Duration
**Problem**: For the same row, **Active Duration** is smaller than **Total Duration**.

**Solutions**:
- This is expected when a patrol has more than one leg: Total Duration runs from the patrol's first to its last recorded position and includes the break between legs, while Active Duration counts only the legs' own time
- Compare **Elapsed Duration** with Total Duration instead — both span the whole patrol

#### Total Distance or Total Duration looks too high
**Problem**: A few patrols are inflating the totals with implausible values (huge teleports, very long segments).

**Solutions**:
- Tighten the **Trajectory Filter** in advanced settings — lower `Maximum Segment Length (Meters)` and `Maximum Segment Speed (Kilometers per Hour)` to drop GPS jumps
- Verify the underlying patrol observations in EarthRanger for outliers

#### Workflow runs very slowly
**Problem**: The workflow takes a long time to complete.

**Solutions**:
- Narrow your **Time Range** — large date ranges over many patrols take longer to fetch
- Limit **Patrol Types** to only what you need
- The first run after a cold start may be slower while the system warms up — subsequent runs are faster

#### Authentication errors
**Problem**: The workflow reports an authentication or permission error.

**Solutions**:
- Re-enter your EarthRanger credentials in Ecoscope Desktop
- Confirm your EarthRanger account has permission to view the requested patrol types
- Ask your EarthRanger administrator to grant access to the patrol types you selected
