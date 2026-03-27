# Housing Conditions and Self-Reported Health Among Indigenous Peoples in Canada

Project Proposal: submitted separately.

## Introduction

This project examines how housing conditions are associated with self-reported general health and mental health in Canada using official data from Statistics Canada. The main goal is descriptive rather than predictive: to clean the published dataset in Python, organize it into interpretable analytical views, and build a dashboard that clearly shows how repair needs, crowding, and geography relate to well-being.

The topic is important because housing is widely recognized as a social determinant of health. Conditions such as overcrowding, structural damage, and the need for major repairs can contribute to stress, lower quality of life, and poorer physical and mental health outcomes. For Indigenous populations in Canada, housing conditions are especially important to study because they are connected to broader structural inequalities, access to services, and geographic differences across the country.

This project is based on Statistics Canada Table 41-10-0080-01, titled *General health and mental health by housing situation, First Nations people living off reserve, Métis and Inuit*. The table is drawn from the 2022 Indigenous Peoples Survey (IPS). According to Statistics Canada, the target population for the IPS is the Indigenous identity population of Canada aged 1 year and over living in private dwellings, excluding persons living on reserves and settlements and in certain First Nations communities in Yukon and the Northwest Territories. That scope matters because the dashboard and the report are describing this published survey population, not the entire Canadian population and not all Indigenous communities in every setting.

The project also follows the structure proposed earlier in the semester: data understanding, cleaning, exploratory visualization, interpretation, and dashboard presentation. Over the past several weeks, the work focused on identifying which parts of the published table were most suitable for analysis and which kinds of visualizations best communicated the relationship between health and housing. The final result is a descriptive dashboard that moves from a national snapshot to regional variation and then to the two housing dimensions that matter most in the data: repair needs and crowding.

The central research question is:

**How are self-reported general health and mental health distributed across different housing conditions and regions in the Indigenous Peoples Survey data for Canada in 2022?**

To answer that question, the dashboard focuses on three tasks:

1. describe the national baseline for health, repair needs, and crowding;
2. compare severe crowding across regions, provinces, and territories;
3. show how health composition changes across repair conditions and crowding levels.

## Background/Literature Review

Housing and health are closely connected in public health research. The World Health Organization has emphasized that poor housing conditions can increase health risks through structural problems, exposure, instability, and psychosocial stress. Housing is not just a physical shelter; it shapes safety, comfort, privacy, and everyday well-being. This is why housing is often discussed as a social determinant of health rather than simply as a consumer good.

The relationship is especially relevant when studying mental health. Housing stress, overcrowding, and inadequate repair conditions can produce chronic stress, reduce privacy, and affect family dynamics. Research on housing stress and affordability has shown meaningful associations between poor housing conditions and psychological distress. These findings suggest that when we study general health and mental health together, housing conditions can help explain differences in how people report their well-being.

For Indigenous populations in Canada, this issue has both public health and social significance. The National Collaborating Centre for Indigenous Health has described housing as a key determinant of First Nations, Inuit, and Métis health, noting that quality, affordability, safety, and crowding affect both physical and emotional well-being. In this context, a descriptive data analysis project is valuable because it can make patterns in official national data easier to interpret and communicate.

This project is not intended to make a causal claim that housing conditions directly cause any specific health outcome. The published Statistics Canada table is aggregated, which means it summarizes groups rather than following individuals. Even so, descriptive analysis is still useful. If the dashboard shows that fair-or-poor health is consistently more common in more difficult housing conditions, that pattern contributes evidence to the broader discussion of housing as a determinant of health.

The literature also supports the use of transparent, reproducible computational workflows. Many housing and health discussions remain descriptive, but not all are implemented in a way that is easy to reproduce and inspect. One contribution of this project is methodological: it shows how Python can be used to parse a published Statistics Canada table, handle suppressed values, recalculate shares from person counts, and present the results in an interactive dashboard.

## Dataset

The dataset used in this project is the local file `4110008001_databaseLoadingData.csv`, downloaded from Statistics Canada Table 41-10-0080-01. The updated version of the file used in the final dashboard is not a simple flat CSV. It is a wide-format export that contains metadata rows, repeated year labels, region columns, and multiple statistics for each housing and health category. Because of that layout, the first step of the project was to build a parser that converts the published table into a long analytical format.

The parsed dataset contains 10,400 rows and the following main fields:

- `Geography`
- `Indigenous identity`
- `Age group`
- `Gender`
- `Overall health`
- `Housing - Needs repairs`
- `Persons per room (crowding)`
- `Statistics`
- `VALUE`
- `STATUS`

The table includes four types of published statistics:

- Number of persons
- Percent
- Low 95% confidence interval
- High 95% confidence interval

The `STATUS` field is also important. Rows marked `F` are too unreliable to publish and do not contain a usable value. Rows marked `E` are estimates that should be interpreted with caution. In the final dashboard, `F` rows are excluded, while `E` rows are retained. This matches the course workflow developed during the semester: do not silently keep fully suppressed data, but do not discard every estimated value if it is still part of the published evidence.

One major difference between the refreshed file and the earlier working version is the structure of the demographic fields. In the updated file, geography is richly represented, but `Indigenous identity`, `Age group`, and `Gender` appear as totals in the published layout used for the final dashboard. That means the strongest comparisons available in this version of the table are geographic and housing-based rather than subgroup comparisons by identity, age, or gender. This is why the final dashboard is centered on regional variation, repair needs, and crowding.

Another important methodological choice concerns how the health comparisons are calculated. Some of the published percentages in the raw table are normalized within health categories, which makes them less useful for directly answering the question “how does health composition change across housing conditions?” To make that comparison clearer, the dashboard uses `Number of persons` rows and then recomputes within-condition shares in Python. This produces interpretable stacked comparisons such as:

- within each repair condition, what share of people report excellent or very good, good, or fair or poor health?
- within each crowding level, what share of people report excellent or very good, good, or fair or poor health?

This approach preserves the official counts while making the visual comparisons much easier to interpret.

## Methods

The final analytical workflow is descriptive and reproducible. The logic is implemented in `analysis_utils.py`, while `app.py` uses those functions to render the dashboard.

The process can be summarized in five steps:

1. **Parse the Statistics Canada export.**  
   The updated CSV is read and transformed from wide format into a long table. Geography, health category, repair condition, crowding category, statistic type, published value, and status flag are all retained.

2. **Normalize text and clean status values.**  
   Text labels are stripped and standardized so that categories such as `Overall health` and `Persons per room (crowding)` can be used consistently. Rows with `STATUS = F` are excluded from the analytical views.

3. **Select the analytical slices needed for the dashboard.**  
   National snapshot views use Canada totals. The regional map uses province, territory, and regional rows. The repair and crowding charts use `Number of persons` so that condition-specific shares can be recomputed clearly.

4. **Recalculate within-condition health composition.**  
   For each repair condition and for each crowding level, the analysis calculates the share of people in three health categories:
   - Excellent or very good
   - Good
   - Fair or poor

5. **Build an interpretive dashboard.**  
   The final dashboard is organized as a narrative:
   - national baseline,
   - regional map,
   - repair needs and health,
   - crowding and health.

This structure reflects the original proposal and the weekly progress reports. It also improves interpretability. Instead of presenting many disconnected charts, the dashboard now leads the user through a consistent story about housing and health.

## Results

### 1. National Snapshot

The first dashboard section establishes the national baseline for the published population. The Canada total in the table is 1,077,810 people. From that total, the dashboard shows two important housing summaries.

First, repair needs:

- 54.2% are in dwellings needing only regular maintenance
- 32.1% are in dwellings needing minor repairs
- 13.7% are in dwellings needing major repairs

Second, crowding:

- 92.9% are in dwellings with one person or fewer per room
- 3.5% are in dwellings with more than one but less than 1.5 persons per room
- 3.5% are in dwellings with 1.5 persons or more per room

The dashboard also compares the national composition of general health and mental health. For general health, 42.3% report excellent or very good health and 23.9% report fair or poor health. For mental health, 37.2% report excellent or very good health and 29.5% report fair or poor mental health. This means the national baseline is already somewhat more fragile for mental health than for general health.

This baseline is important because it frames the rest of the analysis. The later charts are easier to interpret when the viewer already knows what the Canada total looks like.

### 2. Regional Map

The updated Statistics Canada file made one major improvement to the project: it introduced regional, provincial, and territorial geography into the dashboard. This allowed the addition of a real regional map rather than a placeholder visualization.

The most revealing map setting is:

- `Measure = Total, self-perceived general health`
- `Crowding category = 1.5 persons or more per room`
- `Statistic = Percent`

Under that setting, the highest published value appears in Nunavut at 31.4%. The broader `Territories` grouping also stands out at 21.3%, followed by the Northwest Territories at 7.2%. Most provinces have much lower values, with Ontario at 2.0%, Quebec at 1.8%, and the Atlantic provinces at 1.7%.

This regional contrast is one of the clearest findings in the entire project. Severe crowding is not distributed evenly across geography. The northern geographies stand out sharply, especially Nunavut. That result strengthens the proposal’s aim of including geography in the analysis and supports the argument that housing conditions differ meaningfully across regions.

The map also becomes more informative when the user switches from total health to `fair or poor` health categories. For example, fair-or-poor mental health under severe crowding is highest in Nunavut at 34.9%, again followed by the Territories grouping at 20.2%. The exact interpretation should be cautious because these are published aggregated values rather than raw microdata, but the pattern is still visually and substantively important.

### 3. Repair Needs and Health

The strongest relationship in the dashboard appears in the repair-needs section. This section uses `Number of persons` and then recalculates the share of health categories within each repair condition.

For **general health**, the composition changes substantially as repair needs worsen:

| Repair condition | Excellent or very good | Good | Fair or poor |
| --- | ---: | ---: | ---: |
| Regular maintenance only | 50.4% | 32.2% | 17.3% |
| Minor repairs needed | 35.6% | 37.1% | 27.2% |
| Major repairs needed | 26.1% | 31.9% | 42.0% |

This is a strong descriptive pattern. In dwellings needing only regular maintenance, the fair-or-poor share is 17.3%. In dwellings needing major repairs, it rises to 42.0%. That is a dramatic shift.

For **mental health**, the pattern is just as strong:

| Repair condition | Excellent or very good | Good | Fair or poor |
| --- | ---: | ---: | ---: |
| Regular maintenance only | 43.5% | 32.5% | 23.9% |
| Minor repairs needed | 31.6% | 35.5% | 32.9% |
| Major repairs needed | 25.6% | 31.4% | 43.0% |

Again, fair-or-poor mental health increases sharply as housing repair conditions worsen. The line chart in the dashboard summarizes this pattern directly by plotting the fair-or-poor share across repair levels for both general and mental health. Both lines rise, and both peak in the major-repairs category.

This is the clearest headline result of the project: **more severe repair needs are associated with worse self-reported health composition, both for general health and for mental health**.

### 4. Crowding and Health

The crowding section tells a more nuanced story than the repair-needs section. The relationship is still meaningful, but it is not equally strong for general health and mental health.

For **general health**, the fair-or-poor share does not rise monotonically across the crowding categories:

| Crowding level | Excellent or very good | Good | Fair or poor |
| --- | ---: | ---: | ---: |
| 1 or fewer per room | 42.5% | 33.7% | 23.8% |
| More than 1 and less than 1.5 | 40.3% | 30.9% | 28.9% |
| 1.5 or more per room | 40.2% | 38.3% | 21.5% |

The middle crowding category has the highest fair-or-poor general health share. This means that the crowding pattern for general health is not as simple or as strong as the repair-needs pattern.

For **mental health**, however, the pattern is clearer:

| Crowding level | Excellent or very good | Good | Fair or poor |
| --- | ---: | ---: | ---: |
| 1 or fewer per room | 37.8% | 33.1% | 29.1% |
| More than 1 and less than 1.5 | 32.2% | 34.1% | 33.7% |
| 1.5 or more per room | 28.2% | 37.7% | 34.1% |

In this case, fair-or-poor mental health rises as crowding increases, while the excellent-or-very-good share falls. The increase is not as large as the repair-needs effect, but it is consistent enough to support the interpretation that crowding is more strongly associated with mental health than with general health in this published table.

This difference between repair needs and crowding matters. It means the project does not end with a single oversimplified conclusion. Instead, it reaches a more balanced result:

- repair needs show the strongest descriptive relationship with both general and mental health;
- crowding shows a meaningful additional relationship, especially for mental health;
- regional variation makes severe crowding especially important in northern geographies.

## Discussion

The final dashboard supports the broad argument of the project proposal: housing situation is meaningfully related to self-reported health in the Indigenous Peoples Survey data. The evidence is strongest for repair needs. As housing conditions move from regular maintenance to major repairs, the share of fair-or-poor health rises sharply. This is true for both general health and mental health, and the shift is large enough to be visible immediately in the charts.

Crowding contributes a second layer to the story. At the national level, severe crowding is less common than repair needs, but the regional map shows that it is not evenly distributed. The map makes it clear that certain northern geographies, especially Nunavut, stand out strongly. This gives the dashboard a useful geographic dimension that was missing from the earlier working version of the dataset.

The crowding-health relationship is also more nuanced than the repair-health relationship. For general health, the pattern is mixed. For mental health, however, the fair-or-poor share increases as crowding becomes more severe. This suggests that mental health may be more sensitive to crowded living conditions in the published data than general health is.

These results should be interpreted carefully. The project does not establish causation. The data are aggregated and published in table form, not individual-level survey microdata. The dashboard describes patterns in the official Statistics Canada output; it does not estimate causal effects and it does not predict outcomes for individual people or communities.

The scope of the refreshed file also matters. In this final version, geography is the strongest comparison dimension, while identity, age, and gender are shown as totals in the export used by the dashboard. Because of that, the final visual story is more regional and housing-focused than subgroup-focused. This is not a weakness so much as a reflection of the actual published structure of the data that was available for the final delivery.

There are also limitations related to published suppression. Rows marked `F` had to be excluded. Rows marked `E` were retained with caution. That means some categories remain more uncertain than others. Even so, using the published counts and recalculating within-condition shares produced a more interpretable dashboard than relying only on the raw percentages in the table.

From a course perspective, the final project still meets the intended learning goals. It demonstrates:

- data cleaning,
- parsing a complex published dataset,
- handling suppressed values,
- transforming data into analytic views,
- exploratory visualization,
- regional comparison,
- and interactive dashboard communication.

Just as importantly, the project remains aligned with the proposal and the work completed during the semester. The final product is not trying to do more than the data can support. Instead, it presents a clear, reproducible, and evidence-based descriptive analysis of housing conditions and self-reported health.

## Acknowledgements

This project uses published data from Statistics Canada’s 2022 Indigenous Peoples Survey tables. The dashboard and analysis were developed as part of a Python data analysis course project. I also acknowledge the contextual guidance provided by public health and Indigenous health literature, which helped frame the interpretation of housing as a social determinant of health.

## References

Bentley, R., Baker, A., & Mason, K. (2012). *Housing affordability, housing stress and mental health*. BMC Public Health, 12(1), 1-8.

Government of Canada, Statistics Canada. (2024). *Indigenous Peoples Survey (IPS)*. Surveys and Statistical Programs. https://www23.statcan.gc.ca/imdb/p2SV.pl?Function=getSurvey&SDDS=3250

National Collaborating Centre for Indigenous Health. (2017). *Housing as a social determinant of First Nations, Inuit and Métis health*. https://www.ccnsa-nccah.ca/docs/determinants/FS-Housing-SDOH2017-EN.pdf

Statistics Canada. (2024). *Table 41-10-0080-01: General health and mental health by housing situation, First Nations people living off reserve, Métis and Inuit*. https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=4110008001

World Health Organization. (2018). *WHO Housing and Health Guidelines*. Geneva: World Health Organization.
