# National Household Travel Survey (NHTS) & Domestic Tourism Expenditure Survey (DTES)
### NSS 80th Round (July 2025 – June 2026) | Ministry of Statistics and Programme Implementation (MoSPI)

[![Survey Round](https://img.shields.io/badge/NSS%20Round-80th-blue.svg)](#dataset-overview)
[![Schedule](https://img.shields.io/badge/Schedule-21.1%20(sch211)-green.svg)](#microdata-architecture)
[![Coverage](https://img.shields.io/badge/Coverage-All--India%20(Rural%20%2B%20Urban)-orange.svg)](#survey-methodology)
[![Microdata Identifier](https://img.shields.io/badge/DDI-DDI--IND--MOSPI--NSSO--DTES--2025--26-purple.svg)](#official-documentation)

---

## Table of Contents
1. [Dataset Overview](#dataset-overview)
2. [Directory Layout & File Manifest](#directory-layout--file-manifest)
3. [Official Documentation & Resources](#official-documentation--resources)
4. [Survey Methodology & Sampling Design](#survey-methodology--sampling-design)
5. [Microdata Architecture (The 8 Levels)](#microdata-architecture-the-8-levels)
6. [Relational Schema & Primary Keys](#relational-schema--primary-keys)
7. [Survey Weights & Multiplier Calculation](#survey-weights--multiplier-calculation)
8. [Key Benchmarks & Findings from the Report](#key-benchmarks--findings-from-the-report)
9. [Step-by-Step Guide for EDA & Data Analysis](#step-by-step-guide-for-eda--data-analysis)
10. [Python Code Recipes for Analysis](#python-code-recipes-for-analysis)
11. [Gotchas, Caveats & Best Practices](#gotchas-caveats--best-practices)

---

## Dataset Overview

The **Domestic Tourism Expenditure Survey (DTES)**, integrated with the **National Household Travel Survey (NHTS)**, was canvassed in the **80th Round of the National Sample Survey (NSS)** between **July 2025 and June 2026** by the Household Survey Division (HSD) of the National Statistics Office (NSO), MoSPI, Government of India.

### Key Objectives
* **Tourism Satellite Account (TSA)**: Quantify domestic tourism volume and expenditure according to international definitions (UNWTO / System of National Accounts) to estimate tourism's direct contribution to India's GDP.
* **Transport Planning & Railway Demand**: Meet data requirements of the **Ministry of Railways** and regional transport authorities on travel patterns, modal splits, peak commuting hours, and trip durations.
* **Mobility Equity & Expenditure Profiling**: Assess disparities across rural/urban sectors, income deciles, and gender in daily work/school commuting as well as non-work and overnight travel.

### Survey Scale
* **FSUs Surveyed**: 24,651 First Stage Units (14,244 Rural villages + 10,407 Urban UFS blocks).
* **Households Surveyed**: 246,113 households (142,603 Rural + 103,510 Urban).
* **Persons Listed**: 1,016,109 individuals.
* **Overnight Trips Recorded**:
  * Last 365 Days (Health, Holiday, Shopping, Pilgrimage): 392,834 trips.
  * Last 30 Days (Social, Business, Other): 331,332 trips.
* **Same-Day Trips Recorded**: 227,706 trips.

---

## Directory Layout & File Manifest

```text
├── National Household Travel Survey Report.pdf    # Official MoSPI Factsheet & Press Note (Oct 2026)
├── app.py                                         # Interactive Streamlit intelligence dashboard
├── NHTS_Key_Benchmarks_and_Findings.ipynb        # Executable notebook reproducing all benchmarks & findings
├── output/                                        # Generated publication charts (.png) and benchmark tables (.csv)
├── Indian Household Travel Data  DTES_data.zip     # Original compressed microdata archive
├── README.md                                      # This comprehensive guide
├── data/                                          # Fixed-width microdata text files (.TXT)
│   ├── sch211l01.TXT                              # Level 01: Identification & Field Operations
│   ├── sch211l02.TXT                              # Level 02: Household Characteristics & MPCE
│   ├── sch211l03.TXT                              # Level 03: Demographic Roster of Members
│   ├── sch211l04.TXT                              # Level 04: Overnight Trips (365-Day Reference)
│   ├── sch211l05.TXT                              # Level 05: Overnight Trips (30-Day Reference)
│   ├── sch211l06.TXT                              # Level 06: Itemized Trip Expenditure (365-Day)
│   ├── sch211l07.TXT                              # Level 07: Itemized Trip Expenditure (30-Day)
│   └── sch211l08.TXT                              # Level 08: Same-Day Trips & Expenditures (30-Day)
├── docs/                                          # Scraped official documentation, codebooks & layouts
│   ├── DTES_Vol_I.pdf                             # Instructions to Field Staff (Concepts & Sampling)
│   ├── DTES_Vol_II.pdf                            # Schedules of Enquiry (Questionnaires 0.0 & 21.1)
│   ├── Estimation_Procedure_DTES.pdf              # Statistical estimation formula & weights guide
│   ├── Data_Layout80211.xlsx / .csv               # Field boundaries, lengths, and variable definitions
│   ├── parsed_layout.json                         # Programmatic JSON layout for all 8 levels
│   ├── CODEs_for_Blocks_of_Sch211.xlsx            # Master code values & descriptions
│   ├── Note_for_users_DTES_80.docx / .pdf         # Official guidance on microdata usage & scope
│   ├── README_DTES_211_80.docx / .pdf             # Official data release notes
│   ├── metadata.json                              # NADA portal study metadata
│   └── DDI-IND-MOSPI-NSSO-DTES-2025-26.xml        # DDI 2.5 XML Codebook specification
└── CODEs_for_Blocks_of_Sch211/                    # Individual CSV codebooks per schedule block
    ├── Block_01.csv                               # Identification item codes
    ├── Block_02.csv                               # Field operation status codes
    ├── Block_03.csv                               # Demographic roster codes (relation, education)
    ├── Block_04.csv                               # Household characteristics (religion, social group)
    ├── Block_5.1.csv                              # 365-day trip codes (purposes, travel modes, stays)
    ├── Block_5.2.csv                              # 30-day trip codes
    ├── Block_6.1.csv                              # 365-day expenditure item codes & booking modes
    ├── Block_6.2.csv                              # 30-day expenditure item codes & booking modes
    └── Block_7.csv                                # Same-day trip purpose & expenditure codes
```

---

## Official Documentation & Resources

1. **Factsheet / Report (`National Household Travel Survey Report.pdf`)**:
   Summarizes high-level national indicators released by MoSPI on October 5, 2026: modal shares of workers and students, average commute times, rush hours, commute costs, and overnight trip choices.
2. **Field Instructions (`docs/DTES_Vol_I.pdf`)**:
   Mandatory reading for understanding definitions: what constitutes a "trip" ($\ge 1\text{ km}$), "travel day" (3:00 AM to 2:59 AM), "primary mode", and boundary rules for sample selection.
3. **Questionnaires (`docs/DTES_Vol_II.pdf`)**:
   Contains exact visual forms for Schedule 0.0 (Listing) and Schedule 21.1 (DTES questionnaire).
4. **Layout Specifications (`docs/parsed_layout.json` & `docs/Data_Layout80211.csv`)**:
   Provides 1-indexed byte positions, variable lengths, and field names for all 8 levels.
5. **Codebooks (`CODEs_for_Blocks_of_Sch211/`)**:
   Direct CSV mappings from numeric codes in data files to descriptive text labels.
6. **Estimation Methodology (`docs/Estimation_Procedure_DTES.pdf`)**:
   Formulae for aggregates, sub-sample comparisons, ratio estimates, and standard error computations.

---

## Survey Methodology & Sampling Design

### Geographic Scope
Covers the entire Indian Union (all States and Union Territories), excluding only a few inaccessible villages in the Andaman & Nicobar Islands.

### Multi-Stage Stratified Sampling Framework
1. **First Stage Units (FSUs)**:
   * **Rural Sector**: Villages from Census 2011 (updated to exclude newly urbanized villages).
   * **Urban Sector**: Urban Frame Survey (UFS) blocks from the latest frame.
   * Large FSUs were notionally divided into **Sub-Units (SUs)** or **Sub-Divisions** to maintain uniform cluster sizes.
2. **Stratification & Allocation**:
   * Each district within a State/UT constitutes a basic stratum.
   * In urban areas, million-plus cities formed separate strata.
   * Allocation of FSUs across districts was proportional to projected population as of March 1, 2025.
3. **Sub-Rounds**:
   The 1-year survey period was split into 4 equal sub-rounds of 3 months each to capture seasonal patterns in travel:
   * *Sub-Round 1*: July – September 2025 (Monsoon)
   * *Sub-Round 2*: October – December 2025 (Festive / Autumn)
   * *Sub-Round 3*: January – March 2026 (Winter)
   * *Sub-Round 4*: April – June 2026 (Summer holiday season)
4. **Second Stage Stratification (SSS) within FSUs**:
   Households listed in each FSU were stratified into 5 distinct groups:
   * **SSS 1**: Households with $\ge 1$ member completing an overnight trip during last 365 days for *Medical / Holidaying / Shopping / Pilgrimage* with UMPCE $> A$.
   * **SSS 2**: Same as SSS 1, but with UMPCE $\le A$.
   * **SSS 3**: From remaining households, those with $\ge 1$ member completing any other overnight trip during last 30 days with UMPCE $> A$.
   * **SSS 4**: Same as SSS 3, but with UMPCE $\le A$.
   * **SSS 5**: Other households.
   *(Where $A$ is the median UMPCE cut-off determined during household listing).*
   * **Sample size**: 2 households surveyed from each SSS (total 10 households per FSU).

---

## Microdata Architecture (The 8 Levels)

| File | Level | Block | Entity | Records | File Size | Description |
| :--- | :---: | :---: | :--- | :---: | :---: | :--- |
| `sch211l01.TXT` | 01 | Blocks 1 & 2 | Sample Household | 246,113 | 15.0 MB | Administrative and survey operational details: State, District, FSU, Sector, Sub-round, informant code, survey date, response status. |
| `sch211l02.TXT` | 02 | Block 4 | Household | 246,113 | 16.9 MB | Household characteristics: Household size, religion, social group, household type, principal occupation, UMPCE (Usual Monthly Per Capita Consumer Expenditure). |
| `sch211l03.TXT` | 03 | Block 3 | Member | 1,016,109 | 54.3 MB | Demographic roster of all household members: Age, sex, relation to head, marital status, educational attainment. |
| `sch211l04.TXT` | 04 | Block 5.1 | Overnight Trip (365d) | 392,834 | 28.5 MB | Trips in past 365 days for special purposes (**Medical, Holidaying, Shopping, Pilgrimage**): Leading purpose, mode of travel, stay type, destination state/country, start month. |
| `sch211l05.TXT` | 05 | Block 5.2 | Overnight Trip (30d) | 331,332 | 24.0 MB | Trips in past 30 days for other purposes (**Social, Business, Education, etc.**): Leading purpose, travel mode, accommodation, destination. |
| `sch211l06.TXT` | 06 | Block 6.1 | Trip Spend (365d) | 138,204 | 50.1 MB | Comprehensive itemized expenditures on 365-day trips: Package cost, hotel/homestay, food & drink, railway/road/air fare, shopping, health/medical, bookings via internet/tour operators. |
| `sch211l07.TXT` | 07 | Block 6.2 | Trip Spend (30d) | 115,234 | 41.8 MB | Comprehensive itemized expenditures on 30-day trips across the same expense categories. |
| `sch211l08.TXT` | 08 | Block 7 | Same-Day Trip (30d) | 227,706 | 27.8 MB | Trips completed within 24 hours in past 30 days: Leading purpose, members count, breakdown of expenditure (transport, shopping, food, entertainment, medical). |

---

## Relational Schema & Primary Keys

```
+-------------------------------------------------------------+
|                      HOUSEHOLD (Level 01 & 02)              |
| PK: [Round + Schedule + FSU + Sector + State + ... + HH_No] |
+------------------------------+------------------------------+
                               |
            +------------------+------------------+
            | 1:N                                 | 1:N
            v                                     v
+-------------------------+         +-------------------------------+
|   PERSON (Level 03)     |         |   TRIPS (Levels 04 & 05)      |
| PK: HH_Key + Person_Srl |         | PK: HH_Key + Trip_Srl         |
+-------------------------+         +---------------+---------------+
                                                    |
                                                    | 1:1 (conditional)
                                                    v
                                    +-------------------------------+
                                    | TRIP SPEND (Levels 06 & 07)   |
                                    | PK: HH_Key + Trip_Srl         |
                                    +-------------------------------+
```

### Key Field Byte Ranges

All files share the identical **34-byte Household Identifier**:
* **Round** (bytes 1–2): Always `80`.
* **Schedule** (bytes 3–5): Always `211`.
* **FSU Serial No** (bytes 6–10).
* **Sample Type** (byte 11): Central sample (`1`) or State sample (`2`).
* **Sector** (byte 12): `1` = Rural, `2` = Urban.
* **State** (bytes 13–14): Census 2011 State Code (e.g. `07` = Delhi, `27` = Maharashtra).
* **NSS Region** (bytes 15–17).
* **District** (bytes 18–19).
* **Stratum** (bytes 20–21).
* **Sub-stratum** (bytes 22–23).
* **Sub-Round** (byte 24): `1` to `4`.
* **FOD Sub-Region** (bytes 25–28).
* **Sample Sub-Unit (SU) No** (bytes 29–30).
* **Sample Sub-Division No** (byte 31).
* **Second-Stage-Stratum (SSS)** (byte 32): `1` to `5`.
* **Sample Household No** (bytes 33–34).
* **Level** (bytes 35–36): `01` to `08`.

### Entity-Specific Keys
* **Person Serial Number**: bytes 37–38 in `sch211l03.TXT`.
* **Trip Serial Number**: bytes 37–38 in `sch211l04.TXT`, `sch211l05.TXT`, `sch211l06.TXT`, `sch211l07.TXT`, and `sch211l08.TXT`.

---

## Survey Weights & Multiplier Calculation

Because NSS utilizes a complex multi-stage stratified sampling design with differing selection probabilities across rural/urban strata and household expenditure classes, **raw sample counts do not reflect population totals**.

### Applying Sampling Weights
* Every record in all 8 files ends with a **10-byte Multiplier** field:
  * Level 01: bytes 53–62
  * Level 02: bytes 61–70
  * Level 03: bytes 45–54
  * Level 04: bytes 65–74
  * Level 05: bytes 65–74
  * Level 06: bytes 369–378
  * Level 07: bytes 369–378
  * Level 08: bytes 117–126
* **Formula for Final Weight**:
  $$\text{Final Weight} = \frac{\text{Multiplier}}{100}$$
  *(When combining all 4 sub-rounds together).*
* All records belonging to the same FSU $\times$ SSS share the same weight.

> [!WARNING]
> **Advisory from MoSPI (`docs/Note_for_users_DTES_80.pdf`)**:
> Auxiliary demographic variables (e.g., total members, age, gender) are gathered to compute **rates, ratios, and distributions** (e.g. % of workers using rail, average spend per visitor). **Do not use this survey to generate total population headcounts or overall sex ratios**, as the sample design was optimized for travel behavior and tourism expenditure control totals.

---

## Key Benchmarks & Findings from the Report

The findings published in the **National Household Travel Survey Factsheet** ([`National Household Travel Survey Report.pdf`](file:///Users/shubham/CODE/Projects/Data/Indian%20Travel%20/National%20Household%20Travel%20Survey%20Report.pdf)) provide ready benchmarks to validate your EDA:

### 1. Workforce & Education Mobility
* **Dominant Worker Mode**: Two-wheelers account for **42.6%** of all worker commutes across India (37.1% rural; 52.3% urban). Walking accounts for 28.3%, bicycles 10.7%, buses 6.7%, and private cars 3.0%.
* **Urban Mass Transit Surges**: Metro, suburban rail, monorail, and trams account for 5.0% of urban commutes nationwide, but spike in **Maharashtra (20.7%)**, **West Bengal (16.5%)**, and **Delhi (14.4%)**.
* **Student Commuting**: Walking leads at **37.0%** (47.3% for age 6–14), followed by buses (29.5%) and bicycles (15.8%).

### 2. Commute Times & Rush Hours
* **Average Journey Time**:
  * Students: **23 minutes** (87.6% reach within 30 minutes).
  * Workers: **25 minutes** (83.4% reach within 30 minutes).
* **Morning Peak Windows**:
  * Students: 82.0% depart between 7:00 AM and 10:00 AM (peak 8:00–9:00 AM at 35.7%).
  * Workers: 94.9% depart before 10:00 AM (56.5% between 8:00–10:00 AM; 33.7% between 6:00–8:00 AM).

### 3. Monthly Commuting Expenditure
* **Average Student Commute Cost**: ₹443/month (₹617 urban vs ₹361 rural).
* **Average Worker Commute Cost**: ₹785/month (₹1,044 urban vs ₹612 rural).
* **Gender Spend Disparity**: Male workers spend an average of ₹835/month versus ₹533/month for female workers.

### 4. Household Overnight Travel
* **Transport Modes**: Buses (55.8%) and Railways (17.7%) account for **73.5%** of all overnight journeys; cars account for 15.1% and two-wheelers 8.8%.
* **Purposes**: 70.2% of overnight household travel is for social, communication, and religious purposes.
* **Expenditure (Level 06 Sample Data)**:
  * Mean expenditure per 365-day special overnight trip: **₹18,784** (median: **₹7,850**).

---

## Step-by-Step Guide for EDA & Data Analysis

### Step 1: Parse Fixed-Width Records
Because the microdata files are raw fixed-width text without delimiters, load field positions from [`docs/parsed_layout.json`](file:///Users/shubham/CODE/Projects/Data/Indian%20Travel%20/docs/parsed_layout.json) or [`docs/Data_Layout80211.csv`](file:///Users/shubham/CODE/Projects/Data/Indian%20Travel%20/docs/Data_Layout80211.csv).

### Step 2: Decode Numeric Codes to Categorical Labels
Join or map categorical columns using the CSVs in [`CODEs_for_Blocks_of_Sch211/`](file:///Users/shubham/CODE/Projects/Data/Indian%20Travel%20/CODEs_for_Blocks_of_Sch211):
* `Sector`: `1` $\rightarrow$ Rural, `2` $\rightarrow$ Urban
* `Leading Purpose` (Block 5.1):
  * `2` $\rightarrow$ Holidaying, leisure & recreation
  * `4` $\rightarrow$ Pilgrimage & religious activities
  * `6` $\rightarrow$ Health & medical
  * `7` $\rightarrow$ Shopping
* `Mode of Travel`: `01` $\rightarrow$ On foot, `02` $\rightarrow$ Bus, `03` $\rightarrow$ Train/railways, `05` $\rightarrow$ Air, `06` $\rightarrow$ Own motorized, `08` $\rightarrow$ Rental/cab
* `Type of Stay`: `01` $\rightarrow$ Hotel, `02` $\rightarrow$ Guest house, `03` $\rightarrow$ Dharamshala, `05` $\rightarrow$ Homestay, `11` $\rightarrow$ Friends/relatives

### Step 3: Construct Composite Keys for Joins
Create a unified household ID string to merge household demographics with trip rosters:
```python
df['hh_id'] = (
    df['FSU Serial No.'].astype(str) + '_' +
    df['Sector'].astype(str) + '_' +
    df['State'].astype(str) + '_' +
    df['Second-stage-stratum no.'].astype(str) + '_' +
    df['Sample hhld. No.'].astype(str)
)
```

### Step 4: Perform Weighted Aggregations
Always use the normalized weight:
$$\bar{X}_w = \frac{\sum w_i \cdot x_i}{\sum w_i}$$

---

## Python Code Recipes for Analysis

### 1. Reusable Fixed-Width Loader
```python
import json
import pandas as pd

def load_level(level_name, data_dir='data', layout_path='docs/parsed_layout.json', max_rows=None):
    """
    Load an NSS 80th Round level as a pandas DataFrame using parsed_layout.json.
    Example: load_level('level_04')
    """
    file_map = {
        'level_01': 'sch211l01.TXT',
        'level_02': 'sch211l02.TXT',
        'level_03': 'sch211l03.TXT',
        'level_04': 'sch211l04.TXT',
        'level_05': 'sch211l05.TXT',
        'level_06': 'sch211l06.TXT',
        'level_07': 'sch211l07.TXT',
        'level_08': 'sch211l08.TXT',
    }
    with open(layout_path) as f:
        layout = json.load(f)
    
    fields = layout[level_name]['fields']
    colspecs = [(f['start'] - 1, f['end']) for f in fields]
    colnames = [f['name'] for f in fields]
    
    filepath = f"{data_dir}/{file_map[level_name]}"
    df = pd.read_fwf(filepath, colspecs=colspecs, names=colnames, nrows=max_rows, dtype=str)
    
    # Strip whitespace
    for col in df.columns:
        df[col] = df[col].str.strip()
        
    # Convert Multiplier to numeric weight
    if 'Multiplier' in df.columns:
        df['weight'] = pd.to_numeric(df['Multiplier'], errors='coerce') / 100.0
        
    return df
```

### 2. Analyzing Overnight Trip Purposes (Level 04)
```python
# Load 365-day overnight trips
df_trips = load_level('level_04')

# Decode leading purpose
purpose_map = {
    '2': 'Holidaying & Leisure',
    '4': 'Pilgrimage & Religious',
    '6': 'Health & Medical',
    '7': 'Shopping',
    '9': 'Others'
}
df_trips['purpose_label'] = df_trips['Leading purpose for all the members performing the trip'].map(purpose_map)

# Compute weighted distribution
weighted_counts = df_trips.groupby('purpose_label')['weight'].sum()
weighted_share = (weighted_counts / weighted_counts.sum()) * 100
print(weighted_share.sort_values(ascending=False))
```

### 3. Merging Trips with Detailed Expenditures (Level 04 + Level 06)
```python
# Load trips and expenditures
df_trips = load_level('level_04')
df_spend = load_level('level_06')

# Build join key: Household ID + Trip Serial No
def make_trip_key(df):
    return (
        df['FSU Serial No.'] + '_' +
        df['State'] + '_' +
        df['Sector'] + '_' +
        df['Second-stage-stratum no.'] + '_' +
        df['Sample hhld. No.'] + '_' +
        df['Trip serial no.']
    )

df_trips['trip_id'] = make_trip_key(df_trips)
df_spend['trip_id'] = make_trip_key(df_spend)

# Merge
df_merged = pd.merge(df_trips, df_spend[['trip_id', 'Total (3+10)', 'Sub-total (4.1 to 4.6)', 'Sub-total (5.1 to 5.2)', 'sub-total (6.1 to 6.8)', 'sub-total (7.01 to 7.10)']], on='trip_id', how='inner')

# Numeric conversion
df_merged['total_spend'] = pd.to_numeric(df_merged['Total (3+10)'], errors='coerce')

# Average spend by purpose
avg_spend_by_purpose = df_merged.groupby('purpose_label').apply(
    lambda g: (g['total_spend'] * g['weight']).sum() / g['weight'].sum()
)
print("Weighted Average Spend by Purpose (INR):")
print(avg_spend_by_purpose)
```

### 4. Fast Querying: Converting Fixed-Width TXT to Parquet
```python
import os

# Convert all 8 levels to parquet for sub-second analytical queries
os.makedirs('data_parquet', exist_ok=True)
for lvl in [f'level_0{i}' for i in range(1, 9)]:
    print(f"Converting {lvl}...")
    df = load_level(lvl)
    df.to_parquet(f"data_parquet/{lvl}.parquet", index=False)
print("All levels converted to Parquet!")
```

### 5. Launching the Interactive Streamlit Intelligence Dashboard
An interactive, high-definition dashboard is included in [`app.py`](app.py) with full support for Plotly charts, metric scorecards, tabs, and dataset filters.
```sh
# Run using the project virtual environment
streamlit run app.py
```
* Access URL: `http://localhost:8501`
* Features: Executive Summary Scorecards, Workforce Mobility Explorer, Student Mode Transition Curves, Rush Hour Departure Distributions, Gender Disparity Analyzers, Tourism Seasonality & Expenditure Anatomy, and an Interactive Microdata CSV Query/Download Tool.

---

## Gotchas, Caveats & Best Practices

1. **Fixed-Width Column Offsets**:
   Python string slicing and Pandas `read_fwf` use 0-indexed, half-open intervals `[start-1, end]`. In contrast, official layout documents use 1-indexed inclusive intervals. [`parsed_layout.json`](file:///Users/shubham/CODE/Projects/Data/Indian%20Travel%20/docs/parsed_layout.json) stores the 1-indexed boundaries; always subtract 1 from the start position when using Python.
2. **Package vs. Non-Package Trips**:
   In Levels 06 and 07, if a trip was undertaken as a "Package Tour" (Item 3), itemized expenses (accommodation, transport, meals) may be left blank or recorded as `0`, with the entire amount consolidated under `Package component (Rs.)`. Always analyze `Total (3+10)` when estimating overall trip expenditure.
3. **Reimbursements**:
   Item 12/13 and 14/15 in Levels 06 & 07 capture direct employer/government reimbursements. If analyzing net out-of-pocket household expenses, subtract reimbursements from gross expenditure.
4. **Blank Fields in Microdata**:
   Unanswered or not-applicable fields in the fixed-width text files are padded with spaces (` `), not zeros. Coerce them to `NaN` using `errors='coerce'` before mathematical operations.
5. **Memory Management**:
   Level 03 (Person Roster) has over 1 million rows and Level 04/05 have 300k+ rows. Specify only the columns you need via `colspecs` or convert raw text files to **Apache Parquet** or **DuckDB** tables for optimal speed and memory efficiency.

---

## Citation & License

When publishing research or dashboards based on this microdata, cite the dataset as follows:
> **National Statistics Office (NSO)**. *Domestic Tourism Expenditure Survey (DTES) / National Household Travel Survey (NHTS), NSS 80th Round (July 2025 – June 2026)*. Ministry of Statistics and Programme Implementation (MoSPI), Government of India. Reference ID: `DDI-IND-MOSPI-NSSO-DTES-2025-26`.
