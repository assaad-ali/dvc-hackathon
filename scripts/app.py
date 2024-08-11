import streamlit as st
import pandas as pd
import plotly.graph_objs as go

def load_data():
    return pd.read_csv('../data/analysis-data/dashboard.csv')

# Main function
def main():
    df = load_data()

    # sidebar for filtering options
    st.sidebar.header('Filter Options')

    # category filter
    selected_category = st.sidebar.selectbox('Select Category:', df['Category'].unique())
    df_filtered = df[df['Category'] == selected_category]

    # rating filter
    rating_filter = st.sidebar.slider(
        'Filter by Rating:', 
        float(df['Rating'].min()), 
        float(df['Rating'].max()), 
        float(df['Rating'].median())
    )
    df_filtered = df_filtered[df_filtered['Rating'] <= rating_filter]

    # price filter
    price_filter = st.sidebar.slider(
        'Filter by Price:', 
        float(df['Price'].min()), 
        float(df['Price'].max()), 
        float(df['Price'].median())
    )
    df_filtered = df_filtered[df_filtered['Price'] <= price_filter]

    # year added filter
    year_added_filter = st.sidebar.slider(
        'Filter by Year Added:', 
        int(df['year_added'].min()), 
        int(df['year_added'].max()), 
        int(df['year_added'].median())
    )
    df_filtered = df_filtered[df_filtered['year_added'] <= year_added_filter]

    # variable selection for pie chart
    st.sidebar.header('Select Variable for Pie Chart')
    pie_chart_variable = st.sidebar.selectbox(
        'Select variable for the pie chart:',
        options=['Rating', 'Price', 'year_added']
    )

    # variable selection for bar chart
    st.sidebar.header('Select Variable for Bar Chart')
    bar_chart_variable = st.sidebar.selectbox(
        'Select variable for the bar chart:',
        options=['Rating', 'Price', 'year_added']
    )

    # diplay table data
    columns_to_display = ['App', 'Category', 'Rating', 'Price', 'year_added']
    df_display = df_filtered[columns_to_display]
    st.write(f"Showing data for category: {selected_category} with selected filters")
    st.dataframe(df_display)


    pie_variable_counts = df_filtered[pie_chart_variable].value_counts().sort_index()

    # plotly pie chart
    fig_pie = go.Figure(data=[go.Pie(
        labels=pie_variable_counts.index,
        values=pie_variable_counts.values,
        hoverinfo='label+value+percent'
    )])

    fig_pie.update_layout(title_text=f'Distribution of Apps by {pie_chart_variable} within Selected Category')
    st.plotly_chart(fig_pie)

    # plotly bar chart
    bar_variable_counts = df_filtered[bar_chart_variable].value_counts().sort_index()
    fig_bar = go.Figure(data=[go.Bar(
        x=bar_variable_counts.index,
        y=bar_variable_counts.values
    )])

    fig_bar.update_layout(title_text=f'Number of Apps by {bar_chart_variable}', xaxis_title=bar_chart_variable, yaxis_title='Number of Apps')
    st.plotly_chart(fig_bar)

if __name__ == "__main__":
    main()
