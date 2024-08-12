import streamlit as st
import pandas as pd
import plotly.graph_objs as go

def load_data():
    return pd.read_csv('../data/analysis-data/dashboard.csv')

# Main function
def main():
    df = load_data()
    df_unique = df.drop_duplicates(subset='App').copy()

    st.sidebar.header('Bar Chart Customization')
    
    # User selects the variable to display on the bar chart
    bar_chart_type = st.sidebar.selectbox(
        "Select Bar Chart Type",
        options=[
            "Number of Apps",
            "Average Rating",
            "Distribution of Installs"
        ]
    )
    
    # User selects whether to group by Category or Genre
    group_by_option = st.sidebar.radio(
        "Group by:",
        options=["Category", "Genres"]
    )
    
    # User selects the year or range of years
    min_year = int(df_unique['year'].min())
    max_year = int(df_unique['year'].max())
    
    selected_years = st.sidebar.slider(
        'Select Year Range:',
        min_year,
        max_year,
        (min_year, max_year)
    )
    
    # Filter data by the selected year range
    df_filtered = df_unique[(df_unique['year'] >= selected_years[0]) & (df_unique['year'] <= selected_years[1])]

    # Grouping the filtered data
    df_grouped = df_filtered.groupby(group_by_option).agg({
        'App': 'count',
        'Rating': 'mean',
        'Installs': 'sum'
    }).reset_index()
    
    # Calculate total number of apps
    total_apps = df_grouped['App'].sum()
    
    # Creating the appropriate bar chart based on user selection
    if bar_chart_type == "Number of Apps":
        fig = go.Figure(data=[go.Bar(
            x=df_grouped[group_by_option],
            y=df_grouped['App'],
            marker_color='indianred'
        )])
        fig.update_layout(
            title=f'Number of Apps by {group_by_option} ({selected_years[0]} - {selected_years[1]})<br>Total Number of Apps: {total_apps}',
            xaxis_title=group_by_option,
            yaxis_title='Number of Apps'
        )
    elif bar_chart_type == "Average Rating":
        fig = go.Figure(data=[go.Bar(
            x=df_grouped[group_by_option],
            y=df_grouped['Rating'],
            marker_color='lightsalmon'
        )])
        fig.update_layout(
            title=f'Average Rating by {group_by_option} ({selected_years[0]} - {selected_years[1]})<br>Total Number of Apps: {total_apps}',
            xaxis_title=group_by_option,
            yaxis_title='Average Rating'
        )
    elif bar_chart_type == "Distribution of Installs":
        fig = go.Figure(data=[go.Bar(
            x=df_grouped[group_by_option],
            y=df_grouped['Installs'],
            marker_color='lightblue'
        )])
        fig.update_layout(
            title=f'Distribution of Installs by {group_by_option} ({selected_years[0]} - {selected_years[1]})<br>Total Number of Apps: {total_apps}',
            xaxis_title=group_by_option,
            yaxis_title='Total Installs'
        )
    
    # Displaying the bar chart
    st.write(f"{bar_chart_type} ({selected_years[0]} - {selected_years[1]})")
    st.plotly_chart(fig)
    
    # Displaying the table with the grouped data
    st.write("Table Data")
    st.dataframe(df_grouped)

    
    # Sidebar for Bar Chart Filters
    st.sidebar.header('Bar Chart Filters')
    bar_chart_category = st.sidebar.selectbox('Select Category for Bar Chart:', df['Category'].unique(), index=0)

    # Filtering the dataset by the selected category before setting sliders
    df_bar_filtered_category = df_unique[df_unique['Category'] == bar_chart_category]

    # Setting default slider values to avoid errors
    min_rating = df_bar_filtered_category['Rating'].min()
    max_rating = df_bar_filtered_category['Rating'].max()
    if min_rating == max_rating:
        min_rating = max_rating - 1

    min_price = df_bar_filtered_category['Price'].min()
    max_price = df_bar_filtered_category['Price'].max()
    if min_price == max_price:
        min_price = max_price - 1

    min_year = int(df_bar_filtered_category['year'].min())
    max_year = int(df_bar_filtered_category['year'].max())
    if min_year == max_year:
        min_year = max_year - 1

    bar_chart_rating_filter = st.sidebar.slider(
        'Filter by Rating for Bar Chart:',
        min_rating,
        max_rating,
        df_bar_filtered_category['Rating'].mean()
    )
    bar_chart_price_filter = st.sidebar.slider(
        'Filter by Price for Bar Chart:',
        min_price,
        max_price,
        df_bar_filtered_category['Price'].mean()
    )
    bar_chart_year_filter = st.sidebar.slider(
        'Filter by Year Added for Bar Chart:',
        min_year,
        max_year,
        int(df_bar_filtered_category['year'].mean())
    )

    df_bar_filtered = df_bar_filtered_category[
        (df_bar_filtered_category['Rating'] <= bar_chart_rating_filter) &
        (df_bar_filtered_category['Price'] <= bar_chart_price_filter) &
        (df_bar_filtered_category['year'] <= bar_chart_year_filter)
    ]

    # Plotly Bar Chart
    bar_chart_variable = st.sidebar.selectbox(
        "Bar Chart Variable",
        options=['Rating', 'Price', 'year']
    )
    bar_variable_counts = df_bar_filtered[bar_chart_variable].value_counts().sort_index()
    fig_bar = go.Figure(data=[go.Bar(
        x=bar_variable_counts.index,
        y=bar_variable_counts.values
    )])
    fig_bar.update_layout(title_text=f'Number of Apps by {bar_chart_variable}', xaxis_title=bar_chart_variable, yaxis_title='Number of Apps')
    st.write("Bar Chart")
    st.plotly_chart(fig_bar)

    # Display Bar Chart Table
    columns_to_display_bar = ['App', 'Category', 'Rating', 'Price', 'year']
    df_display_bar = df_bar_filtered[columns_to_display_bar].reset_index(drop=True)
    df_display_bar['year'] = df_display_bar['year'].astype(str)
    st.write("Bar Chart Data")
    st.dataframe(df_display_bar)

    # Sidebar for Pie Chart Filters
    st.sidebar.header('Pie Chart Filters')
    pie_chart_category = st.sidebar.selectbox('Select Category for Pie Chart:', df['Category'].unique(), index=0)

    # Filtering the dataset by the selected category before setting sliders
    df_pie_filtered_category = df_unique[df_unique['Category'] == pie_chart_category]

    # Setting default slider values to avoid errors
    min_rating = df_pie_filtered_category['Rating'].min()
    max_rating = df_pie_filtered_category['Rating'].max()
    if min_rating == max_rating:
        min_rating = max_rating - 1

    min_price = df_pie_filtered_category['Price'].min()
    max_price = df_pie_filtered_category['Price'].max()
    if min_price == max_price:
        min_price = max_price - 1

    min_year = int(df_pie_filtered_category['year'].min())
    max_year = int(df_pie_filtered_category['year'].max())
    if min_year == max_year:
        min_year = max_year - 1

    pie_chart_rating_filter = st.sidebar.slider(
        'Filter by Rating for Pie Chart:',
        min_rating,
        max_rating,
        df_pie_filtered_category['Rating'].mean()
    )
    pie_chart_price_filter = st.sidebar.slider(
        'Filter by Price for Pie Chart:',
        min_price,
        max_price,
        df_pie_filtered_category['Price'].mean()
    )
    pie_chart_year_filter = st.sidebar.slider(
        'Filter by Year Added for Pie Chart:',
        min_year,
        max_year,
        int(df_pie_filtered_category['year'].mean())
    )

    df_pie_filtered = df_pie_filtered_category[
        (df_pie_filtered_category['Rating'] <= pie_chart_rating_filter) &
        (df_pie_filtered_category['Price'] <= pie_chart_price_filter) &
        (df_pie_filtered_category['year'] <= pie_chart_year_filter)
    ]

    # Plotly Pie Chart
    pie_chart_variable = st.sidebar.selectbox(
        "Pie Chart Variable",
        options=['Rating', 'Price', 'year']
    )
    pie_variable_counts = df_pie_filtered[pie_chart_variable].value_counts().sort_index()
    fig_pie = go.Figure(data=[go.Pie(
        labels=pie_variable_counts.index,
        values=pie_variable_counts.values,
        hoverinfo='label+value+percent'
    )])
    fig_pie.update_layout(title_text=f'Distribution of Apps by {pie_chart_variable} within {pie_chart_category}')
    st.write("Pie Chart")
    st.plotly_chart(fig_pie)

    # Display Pie Chart Table
    columns_to_display_pie = ['App', 'Category', 'Rating', 'Price', 'year']
    df_display_pie = df_pie_filtered[columns_to_display_pie].reset_index(drop=True)
    df_display_pie['year'] = df_display_pie['year'].astype(str)
    st.write("Pie Chart Data")
    st.dataframe(df_display_pie)

if __name__ == "__main__":
    main()
