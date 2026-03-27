import matplotlib.pyplot as plt
import pandas as pd
import pydeck as pdk
import seaborn as sns
import streamlit as st

from analysis_utils import (
    CROWDING_LEVELS,
    SHORT_CROWDING_LABELS,
    get_fair_poor_trend,
    get_geography_map_data,
    get_health_composition_by_crowding,
    get_health_composition_by_repairs,
    get_national_housing_distribution,
    get_overall_health_mix,
    get_story_metrics,
    load_dataset,
)

sns.set_theme(style="whitegrid")

st.set_page_config(
    page_title="Indigenous Health and Housing Dashboard",
    layout="wide",
)

HEALTH_COLORS = {
    "Excellent or very good": "#2E8B57",
    "Good": "#F2C14E",
    "Fair or poor": "#C44536",
}


@st.cache_data
def load_dashboard_data():
    data = load_dataset()
    story_metrics = get_story_metrics(data)
    overall_mix = get_overall_health_mix(data)
    repair_distribution = get_national_housing_distribution(data, "repairs")
    crowding_distribution = get_national_housing_distribution(data, "crowding")
    general_repairs = get_health_composition_by_repairs(data, "general")
    mental_repairs = get_health_composition_by_repairs(data, "mental")
    general_crowding = get_health_composition_by_crowding(data, "general")
    mental_crowding = get_health_composition_by_crowding(data, "mental")
    repair_trend = get_fair_poor_trend(data, "repairs")
    crowding_trend = get_fair_poor_trend(data, "crowding")
    return {
        "data": data,
        "story_metrics": story_metrics,
        "overall_mix": overall_mix,
        "repair_distribution": repair_distribution,
        "crowding_distribution": crowding_distribution,
        "general_repairs": general_repairs,
        "mental_repairs": mental_repairs,
        "general_crowding": general_crowding,
        "mental_crowding": mental_crowding,
        "repair_trend": repair_trend,
        "crowding_trend": crowding_trend,
    }


def render_stacked_percent_chart(
    frame,
    index_col,
    title,
    category_col="Health category",
    legend_title="Health category",
    y_label="Share of people within each housing condition (%)",
):
    pivot = (
        frame.pivot(index=index_col, columns=category_col, values="Share")
        .fillna(0)
        .reindex(columns=["Excellent or very good", "Good", "Fair or poor"])
    )
    fig, ax = plt.subplots(figsize=(10, 5))
    pivot.plot(
        kind="bar",
        stacked=True,
        color=[HEALTH_COLORS[column] for column in pivot.columns],
        ax=ax,
        width=0.7,
    )
    ax.set_title(title)
    ax.set_xlabel("")
    ax.set_ylabel(y_label)
    ax.set_ylim(0, 100)
    ax.legend(title=legend_title, frameon=False)
    ax.tick_params(axis="x", rotation=12)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


def render_simple_bar(frame, category_col, value_col, title, x_label="", y_label="Percent"):
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=frame, x=category_col, y=value_col, ax=ax, palette="Blues_d")
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.tick_params(axis="x", rotation=12)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


def render_fair_poor_trend(frame, title, x_label):
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(
        data=frame,
        x="Housing condition",
        y="Share",
        hue="Health type",
        style="Health type",
        markers=True,
        dashes=False,
        linewidth=2.5,
        palette=["#8E44AD", "#C0392B"],
        ax=ax,
    )
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel("Fair or poor share (%)")
    ax.legend(title="")
    ax.tick_params(axis="x", rotation=12)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


dashboard = load_dashboard_data()
data = dashboard["data"]
story_metrics = dashboard["story_metrics"]

st.title("Indigenous Health and Housing Dashboard")
st.caption(
    "This dashboard follows the original project proposal: use Python to clean Statistics Canada data "
    "and visually examine how housing conditions relate to self-reported general and mental health."
)
st.info(
    "Data at a glance: this dashboard analyzes Statistics Canada Table 41-10-0080-01, based on the 2022 "
    "Indigenous Peoples Survey. The published table covers the Indigenous identity population of Canada "
    "aged 1 year and over living in private dwellings, with exclusions noted by Statistics Canada for "
    "people living on reserves and settlements and for certain First Nations communities in Yukon and the "
    "Northwest Territories. The dashboard focuses on self-reported general health, self-reported mental "
    "health, housing repair needs, household crowding, and regional variation across Canada."
)

metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
with metric_col1:
    st.metric("People in the Canada total", f"{story_metrics['total_population']:,.0f}")
with metric_col2:
    st.metric("Major repairs needed", f"{story_metrics['major_repairs_share']:.1f}%")
with metric_col3:
    st.metric("Severe crowding", f"{story_metrics['severe_crowding_share']:.1f}%")
with metric_col4:
    st.metric(
        "Highest severe crowding region",
        f"{story_metrics['top_region']} ({story_metrics['top_region_value']:.1f}%)",
    )

st.markdown(
    """
### Dashboard storyline

This dashboard follows the original goal from the proposal:

1. clean the Statistics Canada data in Python,
2. explore the relationship between housing conditions and self-reported health,
3. compare regions,
4. present the findings through clear visualizations.

To keep the story easy to follow, the dashboard moves from a **national baseline**, to a **regional map**, and then to the two housing dimensions discussed in the proposal: **repair needs** and **crowding**.
"""
)

guide_tab, snapshot_tab, map_tab, repairs_tab, crowding_tab, data_tab = st.tabs(
    [
        "Guide",
        "National Snapshot",
        "Regional Map",
        "Repair Needs and Health",
        "Crowding and Health",
        "Data",
    ]
)

with guide_tab:
    st.subheader("How this dashboard aligns with the project proposal")
    st.markdown(
        """
The proposal described a workflow built around Python, Tableau-style visual storytelling, and reproducible data analysis. This dashboard is fully aligned with that plan.

It also follows the weekly progress reports:

- **Week 1**: understand the variables and decide which fields matter.
- **Week 2**: clean the data and create the first set of exploratory visuals.
- **Week 3**: focus on the variables that best explain the story, especially major repairs, crowding, and fair-or-poor health outcomes.

One important note about the refreshed CSV: this version of the file is organized mainly around **geography**, while identity, age group, and gender are provided as totals. Because of that, the strongest final story is about how **repair needs**, **crowding**, and **regional variation** relate to general and mental health.
"""
    )

    st.subheader("How to read the visuals")
    st.markdown(
        """
- The national charts use `Number of persons` and then recalculate percentages inside each housing condition. This makes the comparisons easier to interpret than relying on the raw published percentages alone.
- The regional map uses the published geography breakdown from the updated Statistics Canada file.
- The health charts focus on three categories: `Excellent or very good`, `Good`, and `Fair or poor`.
- In the repair and crowding tabs, the most important signal to watch is whether the `Fair or poor` share grows when housing conditions become more difficult.
"""
    )

with snapshot_tab:
    st.subheader("1. National baseline")
    st.write(
        "Before comparing regions or housing conditions, it helps to see the national baseline. "
        "These charts establish the starting point for the rest of the story."
    )

    left_col, right_col = st.columns(2)
    with left_col:
        render_stacked_percent_chart(
            dashboard["overall_mix"],
            index_col="Health type",
            title="Overall health composition in the Canada total",
            category_col="Category",
            y_label="Share within each health measure (%)",
        )
        st.caption(
            "Mental health starts from a slightly more fragile baseline: the fair-or-poor share is higher for mental health than for general health in the Canada total."
        )

    with right_col:
        repairs = dashboard["repair_distribution"].copy()
        repairs["Category"] = pd.Categorical(
            repairs["Category"],
            categories=[
                "Regular maintenance only",
                "Minor repairs needed",
                "Major repairs needed",
            ],
            ordered=True,
        )
        render_simple_bar(
            repairs.sort_values("Category"),
            category_col="Category",
            value_col="Share",
            title="How housing repair needs are distributed nationally",
            y_label="Share of people (%)",
        )
        st.caption(
            "Most people fall into the regular-maintenance group, but a meaningful share still lives in dwellings needing major repairs."
        )

    render_simple_bar(
        dashboard["crowding_distribution"].assign(
            Category=lambda frame: pd.Categorical(
                frame["Category"],
                categories=[
                    "1 or fewer per room",
                    "More than 1 and less than 1.5",
                    "1.5 or more per room",
                ],
                ordered=True,
            )
        ).sort_values("Category"),
        category_col="Category",
        value_col="Share",
        title="How household crowding is distributed nationally",
        y_label="Share of people (%)",
    )
    st.caption(
        "Crowding is less common nationally than repair needs, but it becomes much more visible once the data is broken down by region."
    )

with map_tab:
    st.subheader("2. Regional variation")
    st.write(
        "The refreshed dataset now includes regions, provinces, and territories. "
        "This lets us show a real regional map rather than a placeholder heatmap."
    )

    health_options = [
        "Total, self-perceived general health",
        "Self-perceived general health, fair or poor",
        "Total, self-perceived mental health",
        "Self-perceived mental health, fair or poor",
    ]

    map_col1, map_col2, map_col3 = st.columns(3)
    with map_col1:
        map_health = st.selectbox(
            "Measure",
            options=health_options,
            index=0,
        )
    with map_col2:
        map_crowding = st.selectbox(
            "Crowding category",
            options=CROWDING_LEVELS,
            index=2,
            format_func=lambda value: SHORT_CROWDING_LABELS[value],
        )
    with map_col3:
        map_statistic = st.selectbox(
            "Statistic",
            options=["Percent", "Number of persons"],
            index=0,
        )

    include_regions = st.checkbox("Include aggregate regions", value=False)

    map_rows = get_geography_map_data(
        data,
        overall_health=map_health,
        crowding_category=map_crowding,
        statistic=map_statistic,
        include_canada=False,
        include_aggregate_regions=include_regions,
    )

    if map_rows.empty:
        st.warning("No regional records are available for the current selection.")
    else:
        map_view = st.columns([1.8, 1.2])
        with map_view[0]:
            heatmap_layer = pdk.Layer(
                "HeatmapLayer",
                data=map_rows,
                get_position="[lon, lat]",
                get_weight="VALUE",
                radiusPixels=80,
                opacity=0.75,
            )
            point_layer = pdk.Layer(
                "ScatterplotLayer",
                data=map_rows,
                get_position="[lon, lat]",
                get_radius=65000,
                get_fill_color="[196, 69, 54, 180]",
                pickable=True,
            )
            deck = pdk.Deck(
                map_style="mapbox://styles/mapbox/light-v9",
                initial_view_state=pdk.ViewState(
                    latitude=58.0,
                    longitude=-98.0,
                    zoom=2.9,
                ),
                layers=[heatmap_layer, point_layer],
                tooltip={
                    "html": "<b>{Geography}</b><br/>{Statistics}: {VALUE}<br/>Status: {STATUS}",
                    "style": {"backgroundColor": "#203040", "color": "white"},
                },
            )
            st.pydeck_chart(deck)

        with map_view[1]:
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.barplot(
                data=map_rows.sort_values("VALUE", ascending=False),
                x="VALUE",
                y="Geography",
                palette="Reds_r",
                ax=ax,
            )
            ax.set_title("Regional ranking")
            ax.set_xlabel(map_statistic)
            ax.set_ylabel("")
            fig.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

        st.caption(
            "This view makes the regional story easy to see. The northern geographies, especially Nunavut, stand out when severe crowding is selected."
        )

with repairs_tab:
    st.subheader("3. Repair needs and health")
    st.write(
        "This is the clearest relationship in the dashboard. We compare the composition of health outcomes within each repair condition using the number of persons."
    )

    repairs_cols = st.columns(2)
    with repairs_cols[0]:
        render_stacked_percent_chart(
            dashboard["general_repairs"],
            index_col="Housing condition",
            title="General health composition within each repair condition",
        )
        st.caption(
            "As repair needs become more severe, the fair-or-poor share of general health grows noticeably."
        )

    with repairs_cols[1]:
        render_stacked_percent_chart(
            dashboard["mental_repairs"],
            index_col="Housing condition",
            title="Mental health composition within each repair condition",
        )
        st.caption(
            "The same pattern appears for mental health, and the increase is even more pronounced at the major-repairs level."
        )

    render_fair_poor_trend(
        dashboard["repair_trend"],
        title="Fair or poor health becomes more common as repair needs worsen",
        x_label="Repair condition",
    )
    st.markdown(
        """
Main takeaway from this section:

- Moving from `Regular maintenance only` to `Major repairs needed` raises the fair-or-poor share sharply for both general and mental health.
- This is the strongest descriptive pattern in the dashboard.
- It aligns closely with the proposal's goal of showing how housing conditions are linked to self-reported well-being.
"""
    )

with crowding_tab:
    st.subheader("4. Crowding and health")
    st.write(
        "Crowding tells a more nuanced story than repair needs. The pattern is still important, but it is clearer for mental health than for general health."
    )

    crowding_cols = st.columns(2)
    with crowding_cols[0]:
        render_stacked_percent_chart(
            dashboard["general_crowding"],
            index_col="Housing condition",
            title="General health composition within each crowding level",
        )
        st.caption(
            "General health shifts across crowding levels, but the movement is less consistent than the repair-needs pattern."
        )

    with crowding_cols[1]:
        render_stacked_percent_chart(
            dashboard["mental_crowding"],
            index_col="Housing condition",
            title="Mental health composition within each crowding level",
        )
        st.caption(
            "Mental health responds more clearly to crowding: the fair-or-poor share rises as households become more crowded."
        )

    render_fair_poor_trend(
        dashboard["crowding_trend"],
        title="Crowding has a clearer descriptive relationship with mental health",
        x_label="Crowding condition",
    )
    st.markdown(
        """
Main takeaway from this section:

- Crowding is still relevant, but its descriptive link is strongest for mental health.
- In the Canada total, fair-or-poor mental health increases from the lowest crowding group to the most crowded group.
- This gives the project a balanced conclusion: **repair needs show the strongest overall pattern, while crowding adds an important regional and mental-health dimension**.
"""
    )

with data_tab:
    st.subheader("Data notes")
    st.markdown(
        """
This dashboard uses the updated Statistics Canada table now stored in the project folder.

Important notes:

- The refreshed file is geography-rich but keeps identity, age, and gender at total values.
- The health composition charts use `Number of persons` and compute within-condition shares in Python.
- Rows flagged with `F` were excluded from the visuals because they are too unreliable to publish.
- `E` values are retained, which matches the course workflow of using caution rather than dropping every estimate automatically.
"""
    )

    if st.checkbox("Show raw parsed dataset"):
        st.dataframe(data)
