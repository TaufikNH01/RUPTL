# ------------------- Imports ------------------- #
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go




# ------------------- RUEN ------------------- #

RUEN_PATH = '/Users/pikpes/streamlit/project/RUEN_rtu.csv'

# ------------------- Setup and Data Loading ------------------- #
def setup_ui():
    st.title("Solar PV Target: A Glimpse into RUEN & RUPTL Plans")
    st.markdown("Dive into interactive visuals that spotlight the Solar PV targets set out by the RUEN and RUPTL policies. Use the main visualization to get a broad overview, and tweak your view with sidebar customization tools. Curious about the specifics? Access the untouched data through the “raw data” button in the sidebar. Any dashboard access issues? Don’t hesitate to drop me an email at taufik.impact@gmail.com")
    
    st.sidebar.title("Sidebar Options")
    st.sidebar.markdown("Navigate through to select a specific year of interest, analyze the cumulative target, or group and compare regions of your choice")
    st.sidebar.header("Customization Options")
    st.subheader("RUEN")
    st.markdown("**RUEN**, short for *Rencana Umum Energi Nasional*, translates to the **National Energy General Plan**. According to *IESR's 2020 report*, RUEN is instrumental in molding Indonesia's national strategic blueprint, emphasizing the electricity and energy sectors. It lays the groundwork for spawning derivative or sub-policies within Indonesia's energy realm. This significant policy arose from the **Presidential Regulation of Indonesia No. 22** in 2017. Below, you'll delve into two visualization strategies: The **independent target** for each distinct year and The **cumulative target** spanning multiple years.  Visuals are split into: **(a) National Target** - An aggregate of provincial objectives. **(b) Provincial Breakdown from RUEN** - A chart sourced directly from RUEN, spotlighting targets specific to each province. Utilize the sidebar to switch between years, with data spanning from 2015 to 2025, for an all-encompassing look at Indonesia's energy goals over the decade.")



def load_data(filepath):
    try:
        df = pd.read_csv(filepath)
        df.columns = [str(col) if isinstance(col, int) else col for col in df.columns]
        return df, df.columns[1:].tolist()
    except FileNotFoundError:
        st.error(f"Error: The dataset file {filepath} was not found.")
        st.stop()

# ------------------- Sidebar Options ------------------- #

def select_indonesia_options(years):
    st.sidebar.subheader("RUEN (National) Filtering")
    
    # Default values for start and end year
    default_start_year = '2015'
    default_end_year = '2025'

    # Select year range for the national visualization with default values
    start_year_indonesia = st.sidebar.selectbox("Start Year (National)", options=years, index=years.index(default_start_year))
    end_year_indonesia = st.sidebar.selectbox("End Year (National)", options=years, index=years.index(default_end_year))

    # Warning if the end year precedes the start year
    if start_year_indonesia >= end_year_indonesia:
        st.sidebar.warning("Start year should precede end year.")
        st.stop()

    # Default to Scatterplot visualization
    viz_type = st.sidebar.selectbox("Visualization Style (National)", options=['Scatterplot', 'Bar Chart'], index=0)
    return start_year_indonesia, end_year_indonesia, viz_type


def select_province_options(years, df):
    st.sidebar.subheader("RUEN (Provincial) Filtering")
    
    # Select year range for the provincial visualization
    years_range = st.sidebar.slider("Year Range (Provincial)", min_value=int(years[0]), max_value=int(years[-1]), value=[int(years[0]), int(years[-1])])
    
    # Select specific provinces to visualize
    selected_provinces = st.sidebar.multiselect("Provinces", df['Province'].unique().tolist(), default=df['Province'].unique().tolist())
    return years_range, selected_provinces


# ------------------- Data Plotting ------------------- #

# Plotting the data for Indonesia
def plot_indonesia(df, start_year, end_year, viz_type):
    st.subheader('(a) National Target (MW)')
    yearly_total = df.iloc[:, 1:].sum().to_frame()
    yearly_total.columns = ['Target']
    
    # Calculate the cumulative totals
    cumulative_total = yearly_total.cumsum()

    # Filter based on year selection
    yearly_total_filtered = yearly_total.loc[start_year:end_year]
    cumulative_total_filtered = cumulative_total.loc[start_year:end_year]

    if viz_type == 'Scatterplot':
        fig_independent = go.Figure(go.Scatter(x=yearly_total_filtered.index, y=yearly_total_filtered['Target'], mode='lines+markers', name='Target'))
        fig_cumulative = go.Figure(go.Scatter(x=cumulative_total_filtered.index, y=cumulative_total_filtered['Target'], mode='lines+markers', name='Cumulative Target'))
    else:
        fig_independent = go.Figure(go.Bar(x=yearly_total_filtered.index, y=yearly_total_filtered['Target'], name='Target'))
        fig_cumulative = go.Figure(go.Bar(x=cumulative_total_filtered.index, y=cumulative_total_filtered['Target'], name='Cumulative Target'))

    fig_independent.update_layout(title=f'Independent Yearly Progression for National Target ({start_year}-{end_year}) in MW')
    st.plotly_chart(fig_independent)
    st.markdown("*The Independent Yearly Progression represents the specific targets set for each year, showcasing how the targets change annually.*")
    
    fig_cumulative.update_layout(title=f'Cumulative Progression for National Target ({start_year}-{end_year}) in MW')
    st.plotly_chart(fig_cumulative)
    st.markdown("*The Cumulative Progression illustrates the total targets accumulated over the selected range of years, highlighting the compounding effect of yearly targets.*")

    if st.sidebar.button('Show Raw Data for National Target'):
        st.subheader("Raw Data in MW")
        summed_data = df.drop(columns="Province").sum().to_frame().transpose()
        st.write(summed_data.loc[:, start_year:end_year])



def plot_province(df, years_range, selected_provinces):
    st.subheader('(b) Province (MW)')
    df_filtered = df[df['Province'].isin(selected_provinces)]
    
    independent_fig = px.bar(df_filtered, x='Province', y=str(years_range[1]), title=f"Independent Totals for {years_range[1]} by Province")
    st.plotly_chart(independent_fig)

    cumulative_fig = px.bar(df_filtered, x='Province', y=df_filtered.columns[-1], title=f"Cumulative Totals from {years_range[0]} to {years_range[1]} by Province")
    st.plotly_chart(cumulative_fig)

    if st.sidebar.button('Show Raw Data for Provinces'):
        st.write(df_filtered)

# ------------------- Main Function ------------------- #
def main():
    setup_ui()
    
    df, years = load_data(RUEN_PATH)
    
    start_year_indonesia, end_year_indonesia, viz_type = select_indonesia_options(years)
    plot_indonesia(df, start_year_indonesia, end_year_indonesia, viz_type)

    years_range, selected_provinces = select_province_options(years, df)
    plot_province(df, years_range, selected_provinces)

# Entry Point
if __name__ == "__main__":
    main()

    


# ------------------- RUPTL ------------------- #
RUPTL_PATH = '/Users/pikpes/streamlit/project/ruptl_trial.csv'

# ------------------- Setup and Data Loading ------------------- #
def load_data(filepath):
    try:
        df = pd.read_csv(filepath)
        df.columns = [str(col) if isinstance(col, int) else col for col in df.columns]
        return df, df.columns[1:].tolist()
    except FileNotFoundError:
        st.error(f"Error: The dataset file {filepath} was not found.")
        st.stop()

# ------------------- Sidebar Options ------------------- #
def select_options(df, header):
    st.sidebar.header(header)
    start_year = st.sidebar.selectbox(f"Select Start Year for {header}", df.columns[1:], index=0)
    end_year = st.sidebar.selectbox(f"Select End Year for {header}", df.columns[1:], index=len(df.columns[1:])-1)
    viz_type = st.sidebar.selectbox(f"Visualization Type for {header}", ["Line Graph", "Bar Graph", "Raw Data"])
    return start_year, end_year, viz_type

# ------------------- Data Plotting ------------------- #
def plot_ruptl(df, start_year, end_year, viz_type, title, is_cumulative=False):
    df_subset = df.loc[:, str(start_year):str(end_year)]
    
    if is_cumulative:
        df_subset = df_subset.cumsum(axis=1)
    
    fig = go.Figure()

    for idx, row in df_subset.iterrows():
        fig.add_trace(go.Scatter(x=row.index, y=row.values, mode='lines+markers', name=df.iloc[idx, 0]))
        
    if viz_type == 'Bar Graph':
        fig = go.Figure()
        for idx, row in df_subset.iterrows():
            fig.add_trace(go.Bar(x=row.index, y=row.values, name=df.iloc[idx, 0]))

    fig.update_layout(title=title, xaxis_title='Year', yaxis_title='Values')
    st.plotly_chart(fig)

    if is_cumulative:
        st.markdown(f"**Cumulative Target**: Represents the total cumulative values over the years, accumulating year by year starting from {start_year}.")
    else:
        st.markdown(f"**Independent Target**: Shows RUPTL targets for each individual year, without accumulation.")

    if viz_type == 'Raw Data':
        st.write(df_subset)


# ------------------- Main Function ------------------- #
def main():
    st.subheader("RUPTL Analysis")
    st.markdown("**RUPTL**, an acronym for **Rencana Umum Penyediaan Tenaga Listrik**, RUPTL translates to the **PLN’s Electricity Supply Business Plan**. This document outlines the projected electricity demands and ongoing projects spearheaded by Perusahaan Listrik Negara. Interestingly, Solar PV wasn't recognized as a promising technology until the 2010-2019 period. During this pivotal decade, solar energy was spotlighted for its: **(a) Bridging Capabilities**: Serving as an alternative to address the gap in the electrification ratio. **(b) Government Support**: Aligning with policies that focus on renewable energy development, which dovetail with the broader goals of environmental conservation and energy diversification. **(c) Community Empowerment**: Providing residents in Indonesia's remote and underdeveloped areas with essential electricity access. **(d) Regional Recognition**: Gaining acknowledgment as a primary energy source, especially in South Sulawesi. In the visualizations that follow, you'll encounter two distinct graphical representations: one illustrating the individual targets set for each RUPTL period and another highlighting the cumulative figures across various years.")

    df_ruptl, ruptl_years = load_data(RUPTL_PATH)
    
    # For Independent target
    start_year_ind, end_year_ind, viz_type_ind = select_options(df_ruptl, "RUPTL: Independent Target Options")
    plot_ruptl(df_ruptl, start_year_ind, end_year_ind, viz_type_ind, "Independent Target for RUPTL")
       
    # For Cumulative target
    start_year_cum, end_year_cum, viz_type_cum = select_options(df_ruptl, "RUPTL: Cumulative Target Options")
    plot_ruptl(df_ruptl, start_year_cum, end_year_cum, viz_type_cum, "Cumulative Target for RUPTL", is_cumulative=True)
    

# Entry Point
if __name__ == "__main__":
    main()


    
