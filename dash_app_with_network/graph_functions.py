### Callbacks File

#### Initial Set Up ####

# Importing Libraries
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from dash.dependencies import Input, Output

from app import app

# Bringing in Data
collab_data = pd.read_csv("./data/US_Spotify_Data.csv")
collab_genres = pd.read_csv("./data/US_Spotify_Genre_Data.csv")
collab_features_data = pd.read_csv("./data/US_Spotify_Audio_Features_Working_Data.csv")

# Cleaning Up Some Columns
collab_data['Date'] = pd.to_datetime(collab_data['Date'])
collab_data['Album_release_dayweek'] = pd.Categorical(collab_data['Album_release_dayweek'],
                                                      categories=['Mon', 'Tue', 'Wed',
                                                                  'Thu', 'Fri', 'Sat', 'Sun'],
                                                      ordered=True)

# Setting Colors
colors = {
    'main_color': 'limegreen',
    'bg_color': 'limegreen',
    'alt_bg_color': 'black',
    'plot_bg_color': 'black',
    'txt_color1': 'white',
    'txt_color2': 'black',
    'palette': ['greenyellow', 'chartreuse', 'lawngreen', 'limegreen', 'lime'],
    'collabbarcolors': ['greenyellow', 'chartreuse', 'lawngreen', 'limegreen', 'lime',
                        'greenyellow', 'chartreuse', 'lawngreen', 'limegreen', 'lime',
                        'greenyellow']
}


#### Collaborator Box Plots ####
@app.callback(Output('collab_bar_chart', 'figure'),
              [Input('collab_data_source', 'value')])
def collab_bar_charts(data_source):
    if data_source == 'Count':
        count_collaborators = (
            collab_data.drop_duplicates("Track URI2")
                .groupby(["No. of Artists"])
                .count()
                .reset_index()
                .rename(columns={"Unnamed: 0": "Count of Tracks"})
                .sort_values(by="No. of Artists", ascending=True)
        )
        count_collaborators = px.bar(count_collaborators, x="No. of Artists", y="Count of Tracks",
                                     color_discrete_sequence=colors['collabbarcolors'],
                                     title='Count of Collaborations in Dataset')

        count_collaborators.update_layout(
            plot_bgcolor=colors['plot_bg_color'],
            paper_bgcolor=colors['plot_bg_color'],
            font_color=colors['txt_color1']
        )

        return count_collaborators

    elif data_source == 'Position':
        position_collaborators = (
            collab_data.drop_duplicates("Track Name")
                .groupby(["No. of Artists"])["Position"]
                .mean()
                .reset_index(name="Average Position")
                .sort_values(by="No. of Artists", ascending=True)
        )
        position_collaborators = px.bar(position_collaborators, x="No. of Artists", y="Average Position",
                                        color_discrete_sequence=colors['collabbarcolors'],
                                        title='Average Position Based On Number of Collaborators'
                                        )

        position_collaborators.update_layout(
            plot_bgcolor=colors['plot_bg_color'],
            paper_bgcolor=colors['plot_bg_color'],
            font_color=colors['txt_color1']
        )
        return position_collaborators

    elif data_source == 'Streams':
        streams_collaborators = (
            collab_data.drop_duplicates("Track Name")
                .groupby(["No. of Artists"])["Streams"]
                .mean()
                .reset_index(name="Streams")
                .sort_values(by="No. of Artists", ascending=True)
        )
        streams_collaborators = px.bar(streams_collaborators, x="No. of Artists", y="Streams",
                                       color_discrete_sequence=colors['collabbarcolors'],
                                       title='Average Streams Based On Number of Collaborators')

        streams_collaborators.update_layout(
            plot_bgcolor=colors['plot_bg_color'],
            paper_bgcolor=colors['plot_bg_color'],
            font_color=colors['txt_color1']
        )
        return streams_collaborators

    elif data_source == 'Revenue':
        revenue_collaborators = (
            collab_data.drop_duplicates("Track Name")
                .groupby(["No. of Artists"])["Revenue"]
                .mean()
                .reset_index(name="Revenue")
                .sort_values(by="No. of Artists", ascending=True)
        )

        revenue_collaborators = px.bar(revenue_collaborators, x="No. of Artists", y="Revenue",
                                       color_discrete_sequence=colors['collabbarcolors'],
                                       title='Average Revenue Based on Number of Collaborators')

        revenue_collaborators.update_layout(
            plot_bgcolor=colors['plot_bg_color'],
            paper_bgcolor=colors['plot_bg_color'],
            font_color=colors['txt_color1']
        )
        return revenue_collaborators


#### Genre Metric Plots ####
@app.callback(Output('genre_bar_chart', 'figure'),
              Input('genre_data_source', 'value'),
              Input('genre_selections', 'value'))
def genre_bar_charts(data_source, genres):
    if genres == 'None' or genres == []:
        select_collab_genres = collab_genres.copy()
    else:
        select_collab_genres = collab_genres[collab_genres['Artist Genre'].isin(genres)]

    if data_source == 'Count':
        count_genres = (
            select_collab_genres
                .groupby(["Artist Genre"])
                .count()
                .reset_index()
                .rename(columns={"Unnamed: 0": "Count of Artists"})
                .sort_values(by="Count of Artists", ascending=False)
        )

        if genres == 'None' or genres == []:
            count_genres = count_genres.head(5)
        else:
            pass

        count_genres = px.bar(count_genres, x="Count of Artists", y="Artist Genre", orientation='h',
                              color_discrete_sequence=colors['genrebarcolors'],
                              title='Count of Artists For Each Genre')

        count_genres.update_layout(
            plot_bgcolor=colors['plot_bg_color'],
            paper_bgcolor=colors['plot_bg_color'],
            font_color=colors['txt_color1']
        )

        return count_genres

    elif data_source == 'Position':
        position_genres = (
            select_collab_genres
                .groupby(["Artist Genre"])["Position"]
                .mean()
                .reset_index(name="Average Position")
                .sort_values(by="Average Position", ascending=True)
        )

        if genres == 'None' or genres == []:
            position_genres = position_genres.head(5).sort_values(by="Average Position", ascending=False)
        else:
            pass

        position_genres = px.bar(position_genres, x="Average Position", y="Artist Genre", orientation='h',
                                 color_discrete_sequence=colors['genrebarcolors'],
                                 title='Average Position For Each Genre')

        position_genres.update_layout(
            plot_bgcolor=colors['plot_bg_color'],
            paper_bgcolor=colors['plot_bg_color'],
            font_color=colors['txt_color1']
        )
        return position_genres

    elif data_source == 'Streams':
        streams_genres = (
            select_collab_genres
                .groupby(["Artist Genre"])["Streams"]
                .mean()
                .reset_index(name="Average Streams")
                .sort_values(by="Average Streams", ascending=False)
        )

        if genres == 'None' or genres == []:
            streams_genres = streams_genres.head(5)
        else:
            pass

        streams_genres = px.bar(streams_genres, x="Average Streams", y="Artist Genre", orientation='h',
                                color_discrete_sequence=colors['genrebarcolors'],
                                title='Average Streams For Each Genre')

        streams_genres.update_layout(
            plot_bgcolor=colors['plot_bg_color'],
            paper_bgcolor=colors['plot_bg_color'],
            font_color=colors['txt_color1']
        )
        return streams_genres

    elif data_source == 'Revenue':
        revenue_genres = (
            select_collab_genres
                .groupby(["Artist Genre"])["Revenue"]
                .mean()
                .reset_index(name="Average Revenue")
                .sort_values(by="Average Revenue", ascending=False)
        )

        if genres == 'None' or genres == []:
            revenue_genres = revenue_genres.head(5)
        else:
            pass

        revenue_genres = px.bar(revenue_genres, x="Average Revenue", y="Artist Genre", orientation='h',
                                color_discrete_sequence=colors['genrebarcolors'],
                                title='Average Revenue For Each Genre')

        revenue_genres.update_layout(
            plot_bgcolor=colors['plot_bg_color'],
            paper_bgcolor=colors['plot_bg_color'],
            font_color=colors['txt_color1']
        )
        return revenue_genres


#### Position Metrics Plots - All Streams/ Average ####
@app.callback(Output('position_streams_bar_chart', 'figure'),
              [Input('position_streams_data_source', 'value')])
def position_streams_charts(data_source):
    if data_source == 'All Streams':
        streams_position = px.scatter(collab_data, x="Position", y="Streams",
                                      color_discrete_sequence=[colors['main_color']],
                                      title='All Streams Compared to Position')

        streams_position.update_layout(
            plot_bgcolor=colors['plot_bg_color'],
            paper_bgcolor=colors['plot_bg_color'],
            font_color=colors['txt_color1']
        )

        return streams_position

    elif data_source == 'Average Streams':
        average_streams_position = (
            collab_data.groupby(["Position"])["Streams"]
                .mean()
                .reset_index(name='Average Streams')
        )

        average_streams_position = px.scatter(average_streams_position, x="Position", y="Average Streams",
                                              color_discrete_sequence=[colors['main_color']],
                                              title='Average Streams Compared to Position')

        average_streams_position.update_layout(
            plot_bgcolor=colors['plot_bg_color'],
            paper_bgcolor=colors['plot_bg_color'],
            font_color=colors['txt_color1']
        )

        return average_streams_position


#### Position Metrics Plots - All Revenues/ Average ####
@app.callback(Output('position_revenue_bar_chart', 'figure'),
              [Input('position_revenue_data_source', 'value')])
def position_revenue_bar_charts(data_source):
    if data_source == 'All Revenues':
        revenue_position = px.scatter(collab_data, x="Position", y="Revenue",
                                      color_discrete_sequence=[colors['main_color']],
                                      title='All Revenues Compared to Position')

        revenue_position.update_layout(
            plot_bgcolor=colors['plot_bg_color'],
            paper_bgcolor=colors['plot_bg_color'],
            font_color=colors['txt_color1']
        )

        return revenue_position

    elif data_source == 'Average Revenues':
        average_revenue_position = (
            collab_data.groupby(["Position"])["Revenue"]
                .mean()
                .reset_index(name='Average Revenue')
        )

        average_revenue_position = px.scatter(average_revenue_position, x="Position", y="Average Revenue",
                                              color_discrete_sequence=[colors['main_color']],
                                              title='Average Revenue Compared to Position')

        average_revenue_position.update_layout(
            plot_bgcolor=colors['plot_bg_color'],
            paper_bgcolor=colors['plot_bg_color'],
            font_color=colors['txt_color1']
        )

        return average_revenue_position


#### Track Metric Plots ####
@app.callback(Output('track_bar_chart', 'figure'),
              Input('track_data_source', 'value'),
              Input('track_selections', 'value'))
def track_bar_charts(data_source, track_names):
    if track_names == 'None' or track_names == []:
        select_collab_tracks = collab_data.copy()
    else:
        select_collab_tracks = collab_data[collab_data['Track Name'].isin(track_names)]

    if data_source == 'Count':
        count_tracks = (
            select_collab_tracks
                .groupby(["Track Name"])
                .count()
                .reset_index()
                .rename(columns={"Unnamed: 0": "Count"})
                .sort_values(by="Count", ascending=False)
        )

        if track_names == 'None' or track_names == []:
            count_tracks = count_tracks.head(5)
        else:
            pass

        count_tracks = px.bar(count_tracks, x="Count", y="Track Name", orientation='h',
                               color_discrete_sequence=colors['genrebarcolors'],
                               title='Count of Tracks In The Dataset')

        count_tracks.update_layout(
            plot_bgcolor=colors['plot_bg_color'],
            paper_bgcolor=colors['plot_bg_color'],
            font_color=colors['txt_color1']
        )

        return count_tracks

    elif data_source == 'Position':
        position_tracks = (
            select_collab_tracks
                .groupby(["Track Name"])["Position"]
                .mean()
                .reset_index(name="Average Position")
                .sort_values(by="Average Position", ascending=True)
        )

        if track_names == 'None' or track_names == []:
            position_tracks = position_tracks.head(5).sort_values(by="Average Position", ascending=False)
        else:
            pass

        position_tracks = px.bar(position_tracks, x="Average Position", y="Track Name", orientation='h',
                                  color_discrete_sequence=colors['genrebarcolors'],
                                  title='Average Position For Each Track')

        position_tracks.update_layout(
            plot_bgcolor=colors['plot_bg_color'],
            paper_bgcolor=colors['plot_bg_color'],
            font_color=colors['txt_color1']
        )
        return position_tracks

    elif data_source == 'Streams':
        streams_tracks = (
            select_collab_tracks
                .groupby(["Track Name"])["Streams"]
                .mean()
                .reset_index(name="Average Streams")
                .sort_values(by="Average Streams", ascending=True)
        )

        if track_names == 'None' or track_names == []:
            streams_tracks = streams_tracks.head(5).sort_values(by="Average Streams", ascending=False)
        else:
            pass

        streams_tracks = px.bar(streams_tracks, x="Average Streams", y="Track Name", orientation='h',
                                 color_discrete_sequence=colors['genrebarcolors'],
                                 title='Average Streams For Each Track')

        streams_tracks.update_layout(
            plot_bgcolor=colors['plot_bg_color'],
            paper_bgcolor=colors['plot_bg_color'],
            font_color=colors['txt_color1']
        )
        return streams_tracks

    elif data_source == 'Revenue':
        revenue_tracks = (
            select_collab_tracks
                .groupby(["Track Name"])["Revenue"]
                .mean()
                .reset_index(name="Average Revenue")
                .sort_values(by="Average Revenue", ascending=True)
        )

        if track_names == 'None' or track_names == []:
            revenue_tracks = revenue_tracks.head(5).sort_values(by="Average Revenue", ascending=False)
        else:
            pass

        revenue_tracks = px.bar(revenue_tracks, x="Average Revenue", y="Track Name", orientation='h',
                                 color_discrete_sequence=colors['genrebarcolors'],
                                 title='Average Revenue For Each Artist')

        revenue_tracks.update_layout(
            plot_bgcolor=colors['plot_bg_color'],
            paper_bgcolor=colors['plot_bg_color'],
            font_color=colors['txt_color1']
        )
        return revenue_tracks


#### Track Revenue Over Time ####
# Timeline selector is not necessary... should be implicitly in figure...
@app.callback(Output('track_revenue_over_time_plot', 'figure'),
              Output('top_revenue', 'value'),
              Input('track_revenue_selection', 'value'))
def track_revenue_over_time(tracks):
    if tracks == 'None' or tracks == []:
        revenue_top_tracks = (
            collab_data.groupby(['Track Name'])['Revenue']
                .mean()
                .reset_index(name='Average Revenue')
                .sort_values(by='Average Revenue', ascending=False)
                .head(15)
        )

    else:
        revenue_top_tracks = collab_data[collab_data['Track Name'].isin(tracks)]

    track_revenue_overtime = (
        collab_data[collab_data['Track Name'].isin(list(revenue_top_tracks['Track Name']))]
            .groupby(['Track Name', 'Date'])['Revenue']
            .mean()
            .reset_index(name='Average Revenue')
    )

    top_revenue = track_revenue_overtime[track_revenue_overtime['Average Revenue'].max()]

    track_revenue_plot = px.line(track_revenue_overtime, x="Date", y="Average Revenue", color='Track Name',
                                 color_discrete_sequence=colors['collabbarcolors'],
                                 title='Top Tracks Over Time Based on Revenue')

    track_revenue_plot.update_layout(
        plot_bgcolor=colors['plot_bg_color'],
        paper_bgcolor=colors['plot_bg_color'],
        font_color=colors['txt_color1'],
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label="1 Month",
                         step="month",
                         stepmode="backward"),
                    dict(count=6,
                         label="6 Months",
                         step="month",
                         stepmode="backward"),
                    dict(count=1,
                         label="1 Year",
                         step="year",
                         stepmode="backward"),
                    dict(label="All",
                         step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date",
        )
    )

    return track_revenue_plot, top_revenue


#### Top Tracks Over Time ####
@app.callback(Output('top_tracks_over_time_plot', 'figure'),
              Output('top_metric', 'value'),
              Input('top_tracks_data_source', 'value'),
              Input('top_tracks_track_selection', 'value'))
def top_tracks_over_time(data_source, tracks):
    if data_source == 'Position':
        if tracks == 'None' or tracks == []:
            top_tracks = (
                collab_data.groupby(['Track Name'])['Position']
                    .mean()
                    .reset_index(name='Average Position')
                    .sort_values(by='Average Position', ascending=True)
                    .head(15)
            )

        else:
            top_tracks = collab_data[collab_data['Track Name'].isin(tracks)]

        track_position_overtime = (
            collab_data[collab_data['Track Name'].isin(list(top_tracks['Track Name']))]
                .groupby(['Track Name', 'Date'])['Position']
                .mean()
                .reset_index(name='Average Position')
        )

        top_position = track_position_overtime[track_position_overtime['Average Position'].min()]

        track_position_plot = px.line(track_position_overtime, x="Date", y="Average Position",
                                      title='Top Tracks Over Time Based on Position',
                                      color_discrete_sequence=colors['collabbarcolors'], color='Track Name')

        track_position_plot.update_layout(
            plot_bgcolor=colors['plot_bg_color'],
            paper_bgcolor=colors['plot_bg_color'],
            font_color=colors['txt_color1'],
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                             label="1 Month",
                             step="month",
                             stepmode="backward"),
                        dict(count=6,
                             label="6 Months",
                             step="month",
                             stepmode="backward"),
                        dict(count=1,
                             label="1 Year",
                             step="year",
                             stepmode="backward"),
                        dict(label="All",
                             step="all")
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type="date",
            )
        )

        return track_position_plot, top_position

    if data_source == 'Streams':
        if tracks == 'None' or tracks == []:
            top_tracks = (
                collab_data.groupby(['Track Name'])['Streams']
                    .mean()
                    .reset_index(name='Average Streams')
                    .sort_values(by='Average Streams', ascending=True)
                    .head(15)
            )

        else:
            top_tracks = collab_data[collab_data['Track Name'].isin(tracks)]

        track_streams_overtime = (
            collab_data[collab_data['Track Name'].isin(list(top_tracks['Track Name']))]
                .groupby(['Track Name', 'Date'])['Streams']
                .mean()
                .reset_index(name='Average Streams')
        )

        top_streams = track_streams_overtime[track_streams_overtime['Average Streams'].max()]

        track_streams_plot = px.line(track_streams_overtime, x="Date", y="Average Streams",
                                     title='Top Tracks Over Time Based on Streams',
                                     color_discrete_sequence=colors['collabbarcolors'], color='Track Name')

        track_streams_plot.update_layout(
            plot_bgcolor=colors['plot_bg_color'],
            paper_bgcolor=colors['plot_bg_color'],
            font_color=colors['txt_color1'],
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                             label="1 Month",
                             step="month",
                             stepmode="backward"),
                        dict(count=6,
                             label="6 Months",
                             step="month",
                             stepmode="backward"),
                        dict(count=1,
                             label="1 Year",
                             step="year",
                             stepmode="backward"),
                        dict(label="All",
                             step="all")
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type="date",
            )
        )

        return track_streams_plot, top_streams


#### Artist Metric Plots ####
@app.callback(Output('artist_bar_chart', 'figure'),
              Input('artist_data_source', 'value'),
              Input('artist_selections', 'value'))
def artist_bar_charts(data_source, artist_names):
    if artist_names == 'None' or artist_names == []:
        select_collab_artists = collab_data.copy()
    else:
        select_collab_artists = collab_data[collab_data['Artist Name'].isin(artist_names)]

    if data_source == 'Count':
        count_artists = (
            select_collab_artists
                .groupby(["Artist Name"])
                .count()
                .reset_index()
                .rename(columns={"Unnamed: 0": "Count"})
                .sort_values(by="Count", ascending=False)
        )

        if artist_names == 'None' or artist_names == []:
            count_artists = count_artists.head(5)
        else:
            pass

        count_artists = px.bar(count_artists, x="Count", y="Artist Name", orientation='h',
                               color_discrete_sequence=colors['genrebarcolors'],
                               title='Count of Artist Occurences In The Dataset')

        count_artists.update_layout(
            plot_bgcolor=colors['plot_bg_color'],
            paper_bgcolor=colors['plot_bg_color'],
            font_color=colors['txt_color1']
        )

        return count_artists

    elif data_source == 'Position':
        position_artists = (
            select_collab_artists
                .groupby(["Artist Name"])["Position"]
                .mean()
                .reset_index(name="Average Position")
                .sort_values(by="Average Position", ascending=True)
        )

        if artist_names == 'None' or artist_names == []:
            position_artists = position_artists.head(5).sort_values(by="Average Position", ascending=False)
        else:
            pass

        position_artists = px.bar(position_artists, x="Average Position", y="Artist Name", orientation='h',
                                  color_discrete_sequence=colors['genrebarcolors'],
                                  title='Average Position For Each Artist')

        position_artists.update_layout(
            plot_bgcolor=colors['plot_bg_color'],
            paper_bgcolor=colors['plot_bg_color'],
            font_color=colors['txt_color1']
        )
        return position_artists

    elif data_source == 'Streams':
        streams_artists = (
            select_collab_artists
                .groupby(["Artist Name"])["Streams"]
                .mean()
                .reset_index(name="Average Streams")
                .sort_values(by="Average Streams", ascending=True)
        )

        if artist_names == 'None' or artist_names == []:
            streams_artists = streams_artists.head(5).sort_values(by="Average Streams", ascending=False)
        else:
            pass

        streams_artists = px.bar(streams_artists, x="Average Streams", y="Artist Name", orientation='h',
                                 color_discrete_sequence=colors['genrebarcolors'],
                                 title='Average Streams For Each Artist')

        streams_artists.update_layout(
            plot_bgcolor=colors['plot_bg_color'],
            paper_bgcolor=colors['plot_bg_color'],
            font_color=colors['txt_color1']
        )
        return streams_artists

    elif data_source == 'Revenue':
        revenue_artists = (
            select_collab_artists
                .groupby(["Artist Name"])["Revenue"]
                .mean()
                .reset_index(name="Average Revenue")
                .sort_values(by="Average Revenue", ascending=True)
        )

        if artist_names == 'None' or artist_names == []:
            revenue_artists = revenue_artists.head(5).sort_values(by="Average Revenue", ascending=False)
        else:
            pass

        revenue_artists = px.bar(revenue_artists, x="Average Revenue", y="Artist Name", orientation='h',
                                 color_discrete_sequence=colors['genrebarcolors'],
                                 title='Average Revenue For Each Artist')

        revenue_artists.update_layout(
            plot_bgcolor=colors['plot_bg_color'],
            paper_bgcolor=colors['plot_bg_color'],
            font_color=colors['txt_color1']
        )
        return revenue_artists


#### Track Metrics By Length Of Time ####
@app.callback(Output('tracks_on_chart_plot', 'figure'),
              Input('tracks_on_chart_avg_or_max', 'value'),
              Input('tracks_on_chart_data_source', 'value'))
def track_on_chart(avg_or_max, data_source):
    if avg_or_max == 'Average':
        if data_source == 'Position':
            average_position_trackdays = (
                collab_data.groupby(["Song_days_onchart"])["Position"]
                    .mean()
                    .reset_index()
            )

            average_position_trackdays = px.scatter(average_position_trackdays, x="Song_days_onchart", y="Position",
                                                    color_discrete_sequence=[colors['main_color']],
                                                    title='Average Chart Position Compared to Length of Time on The Chart'
                                                    )

            average_position_trackdays.update_layout(
                plot_bgcolor=colors['plot_bg_color'],
                paper_bgcolor=colors['plot_bg_color'],
                font_color=colors['txt_color1'],
                xaxis_title="Length of Time on Chart (days)"
            )

            return average_position_trackdays

        elif data_source == 'Streams':
            average_streams_trackdays = (
                collab_data.groupby(["Song_days_onchart"])["Streams"]
                    .mean()
                    .reset_index()
            )

            average_streams_trackdays = px.scatter(average_streams_trackdays, x="Song_days_onchart", y="Streams",
                                                   color_discrete_sequence=[colors['main_color']],
                                                   title='Average Streams Compared to Length of Time on The Chart'
                                                   )

            average_streams_trackdays.update_layout(
                plot_bgcolor=colors['plot_bg_color'],
                paper_bgcolor=colors['plot_bg_color'],
                font_color=colors['txt_color1'],
                xaxis_title="Length of Time on Chart (days)"
            )

            return average_streams_trackdays

        elif data_source == 'Revenue':
            average_revenue_trackdays = (
                collab_data.groupby(["Song_days_onchart"])["Revenue"]
                    .mean()
                    .reset_index()
            )

            average_revenue_trackdays = px.scatter(average_revenue_trackdays, x="Song_days_onchart", y="Revenue",
                                                   color_discrete_sequence=[colors['main_color']],
                                                   title='Average Revenue Compared to Length of Time on The Chart'
                                                   )

            average_revenue_trackdays.update_layout(
                plot_bgcolor=colors['plot_bg_color'],
                paper_bgcolor=colors['plot_bg_color'],
                font_color=colors['txt_color1'],
                xaxis_title="Length of Time on Chart (days)"
            )

            return average_revenue_trackdays

    elif avg_or_max == 'Max':
        if data_source == 'Position':
            max_position_trackdays = (
                collab_data.groupby(["Song_days_onchart"])["Position"]
                    .min()
                    .reset_index()
            )

            max_position_trackdays = px.scatter(max_position_trackdays, x="Song_days_onchart", y="Position",
                                                color_discrete_sequence=[colors['main_color']],
                                                title='Highest Chart Position Compared to Length of Time on The Chart'
                                                )

            max_position_trackdays.update_layout(
                plot_bgcolor=colors['plot_bg_color'],
                paper_bgcolor=colors['plot_bg_color'],
                font_color=colors['txt_color1'],
                xaxis_title="Length of Time on Chart (days)"
            )

            return max_position_trackdays

        elif data_source == 'Streams':
            max_streams_trackdays = (
                collab_data.groupby(["Song_days_onchart"])["Streams"]
                    .max()
                    .reset_index()
            )

            max_streams_trackdays = px.scatter(max_streams_trackdays, x="Song_days_onchart", y="Streams",
                                               color_discrete_sequence=[colors['main_color']],
                                               title='Max Number of Streams Compared to Length of Time on The Chart'
                                               )

            max_streams_trackdays.update_layout(
                plot_bgcolor=colors['plot_bg_color'],
                paper_bgcolor=colors['plot_bg_color'],
                font_color=colors['txt_color1'],
                xaxis_title="Length of Time on Chart (days)"
            )

            return max_streams_trackdays

        elif data_source == 'Revenue':
            max_revenue_trackdays = (
                collab_data.groupby(["Song_days_onchart"])["Revenue"]
                    .max()
                    .reset_index()
            )

            max_revenue_trackdays = px.scatter(max_revenue_trackdays, x="Song_days_onchart", y="Revenue",
                                               color_discrete_sequence=[colors['main_color']],
                                               title='Max Revenue Compared to Length of Time on The Chart'
                                               )

            max_revenue_trackdays.update_layout(
                plot_bgcolor=colors['plot_bg_color'],
                paper_bgcolor=colors['plot_bg_color'],
                font_color=colors['txt_color1'],
                xaxis_title="Length of Time on Chart (days)"
            )

            return max_revenue_trackdays


#### Artist Metrics By Length Of Time ####
@app.callback(Output('artist_on_chart_plot', 'figure'),
              Input('artist_on_chart_avg_or_max', 'value'),
              Input('artist_on_chart_data_source', 'value'))
def artist_on_chart(avg_or_max, data_source):
    if avg_or_max == 'Average':
        if data_source == 'Position':
            average_position_artistdays = (
                collab_data.groupby(["Artist_days_onchart"])["Position"]
                    .mean()
                    .reset_index()
            )

            average_position_artistdays = px.scatter(average_position_artistdays, x="Artist_days_onchart", y="Position",
                                                     color_discrete_sequence=[colors['main_color']],
                                                     title='Average Artist Chart Position Compared to Length of Time on The Chart'
                                                     )

            average_position_artistdays.update_layout(
                plot_bgcolor=colors['plot_bg_color'],
                paper_bgcolor=colors['plot_bg_color'],
                font_color=colors['txt_color1'],
                xaxis_title="Length of Time on Chart (days)"
            )

            return average_position_artistdays

        elif data_source == 'Streams':
            average_streams_artistdays = (
                collab_data.groupby(["Artist_days_onchart"])["Streams"]
                    .mean()
                    .reset_index()
            )

            average_streams_artistdays = px.scatter(average_streams_artistdays, x="Artist_days_onchart", y="Streams",
                                                    color_discrete_sequence=[colors['main_color']],
                                                    title='Average Artist Streams Compared to Length of Time on The Chart'
                                                    )

            average_streams_artistdays.update_layout(
                plot_bgcolor=colors['plot_bg_color'],
                paper_bgcolor=colors['plot_bg_color'],
                font_color=colors['txt_color1'],
                xaxis_title="Length of Time on Chart (days)"
            )

            return average_streams_artistdays

        elif data_source == 'Revenue':
            average_revenue_artistdays = (
                collab_data.groupby(["Artist_days_onchart"])["Revenue"]
                    .mean()
                    .reset_index()
            )

            average_revenue_artistdays = px.scatter(average_revenue_artistdays, x="Artist_days_onchart", y="Revenue",
                                                    color_discrete_sequence=[colors['main_color']],
                                                    title='Average Artist Revenue Compared to Length of Time on The Chart'
                                                    )

            average_revenue_artistdays.update_layout(
                plot_bgcolor=colors['plot_bg_color'],
                paper_bgcolor=colors['plot_bg_color'],
                font_color=colors['txt_color1'],
                xaxis_title="Length of Time on Chart (days)"
            )

            return average_revenue_artistdays

    elif avg_or_max == 'Max':
        if data_source == 'Position':
            max_position_artistdays = (
                collab_data.groupby(["Artist_days_onchart"])["Position"]
                    .min()
                    .reset_index()
            )

            max_position_artistdays = px.scatter(max_position_artistdays, x="Artist_days_onchart", y="Position",
                                                 color_discrete_sequence=[colors['main_color']],
                                                 title='Highest Artist Chart Position Compared to Length of Time on The Chart'
                                                 )

            max_position_artistdays.update_layout(
                plot_bgcolor=colors['plot_bg_color'],
                paper_bgcolor=colors['plot_bg_color'],
                font_color=colors['txt_color1'],
                xaxis_title="Length of Time on Chart (days)"
            )

            return max_position_artistdays

        elif data_source == 'Streams':
            max_streams_artistdays = (
                collab_data.groupby(["Artist_days_onchart"])["Streams"]
                    .max()
                    .reset_index()
            )

            max_streams_artistdays = px.scatter(max_streams_artistdays, x="Artist_days_onchart", y="Streams",
                                                color_discrete_sequence=[colors['main_color']],
                                                title='Max Number of Streams for Artists Compared to Length of Time on The Chart'
                                                )

            max_streams_artistdays.update_layout(
                plot_bgcolor=colors['plot_bg_color'],
                paper_bgcolor=colors['plot_bg_color'],
                font_color=colors['txt_color1'],
                xaxis_title="Length of Time on Chart (days)"
            )

            return max_streams_artistdays

        elif data_source == 'Revenue':
            max_revenue_artistdays = (
                collab_data.groupby(["Artist_days_onchart"])["Revenue"]
                    .max()
                    .reset_index()
            )

            max_revenue_artistdays = px.scatter(max_revenue_artistdays, x="Artist_days_onchart", y="Revenue",
                                                color_discrete_sequence=[colors['main_color']],
                                                title='Max Revenue for Artists Compared to Length of Time on The Chart'
                                                )

            max_revenue_artistdays.update_layout(
                plot_bgcolor=colors['plot_bg_color'],
                paper_bgcolor=colors['plot_bg_color'],
                font_color=colors['txt_color1'],
                xaxis_title="Length of Time on Chart (days)"
            )

            return max_revenue_artistdays


#### Collab Artist Metrics By Length Of Time ####
@app.callback(Output('collab_artist_on_chart_plot', 'figure'),
              Input('collab_artist_on_chart_avg_or_max', 'value'),
              Input('collab_artist_on_chart_data_source', 'value'))
def collab_artist_on_chart(avg_or_max, data_source):
    if avg_or_max == 'Average':
        if data_source == 'Position':
            average_position_collab_artistdays = (
                collab_data.drop_duplicates('Track URI2')
                    .groupby(["Collab_avg_days_onchart"])["Position"]
                    .mean()
                    .reset_index()
            )

            average_position_collab_artistdays = px.scatter(average_position_collab_artistdays,
                                                            x="Collab_avg_days_onchart", y="Position",
                                                            color_discrete_sequence=[colors['main_color']],
                                                            title='Artist Collab Average Position Compared to Length of Time on The Chart'
                                                            )

            average_position_collab_artistdays.update_layout(
                plot_bgcolor=colors['plot_bg_color'],
                paper_bgcolor=colors['plot_bg_color'],
                font_color=colors['txt_color1'],
                xaxis_title="Length of Time on Chart (days)"
            )

            return average_position_collab_artistdays

        elif data_source == 'Streams':
            average_streams_collab_artistdays = (
                collab_data.drop_duplicates('Track URI2')
                    .groupby(["Collab_avg_days_onchart"])["Streams"]
                    .mean()
                    .reset_index()
            )

            average_streams_collab_artistdays = px.scatter(average_streams_collab_artistdays,
                                                           x="Collab_avg_days_onchart", y="Streams",
                                                           color_discrete_sequence=[colors['main_color']],
                                                           title='Artist Collab Average Streams Compared to Length of Time on The Chart'
                                                           )

            average_streams_collab_artistdays.update_layout(
                plot_bgcolor=colors['plot_bg_color'],
                paper_bgcolor=colors['plot_bg_color'],
                font_color=colors['txt_color1'],
                xaxis_title="Length of Time on Chart (days)"
            )

            return average_streams_collab_artistdays

        elif data_source == 'Revenue':
            average_revenue_collab_artistdays = (
                collab_data.drop_duplicates('Track URI2')
                    .groupby(["Collab_avg_days_onchart"])["Revenue"]
                    .mean()
                    .reset_index()
            )

            average_revenue_collab_artistdays = px.scatter(average_revenue_collab_artistdays,
                                                           x="Collab_avg_days_onchart", y="Revenue",
                                                           color_discrete_sequence=[colors['main_color']],
                                                           title='Artist Collab Average Revenue Compared to Length of Time on The Chart'
                                                           )

            average_revenue_collab_artistdays.update_layout(
                plot_bgcolor=colors['plot_bg_color'],
                paper_bgcolor=colors['plot_bg_color'],
                font_color=colors['txt_color1'],
                xaxis_title="Length of Time on Chart (days)"
            )

            return average_revenue_collab_artistdays

    elif avg_or_max == 'Max':
        if data_source == 'Position':
            max_position_collab_artistdays = (
                collab_data.drop_duplicates('Track URI2')
                    .groupby(["Collab_avg_days_onchart"])["Position"]
                    .min()
                    .reset_index()
            )

            max_position_collab_artistdays = px.scatter(max_position_collab_artistdays, x="Collab_avg_days_onchart",
                                                        y="Position",
                                                        color_discrete_sequence=[colors['main_color']],
                                                        title='Artist Collab Highest Chart Position Compared to Length of Time on The Chart'
                                                        )

            max_position_collab_artistdays.update_layout(
                plot_bgcolor=colors['plot_bg_color'],
                paper_bgcolor=colors['plot_bg_color'],
                font_color=colors['txt_color1'],
                xaxis_title="Length of Time on Chart (days)"
            )

            return max_position_collab_artistdays

        elif data_source == 'Streams':
            max_streams_collab_artistdays = (
                collab_data.drop_duplicates('Track URI2')
                    .groupby(["Collab_avg_days_onchart"])["Streams"]
                    .max()
                    .reset_index()
            )

            max_streams_collab_artistdays = px.scatter(max_streams_collab_artistdays, x="Collab_avg_days_onchart",
                                                       y="Streams",
                                                       color_discrete_sequence=[colors['main_color']],
                                                       title='Artist Collab Max Streams Compared to Length of Time on The Chart'
                                                       )

            max_streams_collab_artistdays.update_layout(
                plot_bgcolor=colors['plot_bg_color'],
                paper_bgcolor=colors['plot_bg_color'],
                font_color=colors['txt_color1'],
                xaxis_title="Length of Time on Chart (days)"
            )

            return max_streams_collab_artistdays

        elif data_source == 'Revenue':
            max_revenue_collab_artistdays = (
                collab_data.drop_duplicates('Track URI2')
                    .groupby(["Collab_avg_days_onchart"])["Revenue"]
                    .max()
                    .reset_index()
            )

            max_revenue_collab_artistdays = px.scatter(max_revenue_collab_artistdays, x="Collab_avg_days_onchart",
                                                       y="Revenue",
                                                       color_discrete_sequence=[colors['main_color']],
                                                       title='Artist Collab Max Revenue Compared to Length of Time on The Chart'
                                                       )

            max_revenue_collab_artistdays.update_layout(
                plot_bgcolor=colors['plot_bg_color'],
                paper_bgcolor=colors['plot_bg_color'],
                font_color=colors['txt_color1'],
                xaxis_title="Length of Time on Chart (days)"
            )

            return max_revenue_collab_artistdays


#### Month/Day of Week Bar Charts ####
@app.callback(Output('month_day_plot', 'figure'),
              Input('month_day_value', 'value'),
              Input('month_day_data_source', 'value'))
def month_week_bar_charts(month_day, data_source):
    if month_day == 'Months':
        if data_source == 'Count':
            count_month = (
                collab_data.drop_duplicates('Track Name')
                    .groupby(['Album_release_month'])
                    .count()
                    .reset_index()
                    .rename(columns={'Track URI2': 'Count'})
                    .sort_values(by='Album_release_month', ascending=True)
            )

            count_month = px.bar(count_month, x="Album_release_month", y="Count",
                                 color_discrete_sequence=colors['collabbarcolors'],
                                 title="Release Month and Count in Dataset")

            count_month.update_layout(
                plot_bgcolor=colors['plot_bg_color'],
                paper_bgcolor=colors['plot_bg_color'],
                font_color=colors['txt_color1'],
                xaxis_title="Month",
                xaxis=dict(dtick=1)
            )

            return count_month

        elif data_source == 'Position':
            position_month = (
                collab_data.drop_duplicates('Track Name')
                    .groupby(['Album_release_month'])['Position']
                    .mean()
                    .reset_index()
                    .sort_values(by='Album_release_month', ascending=True)
            )

            position_month = px.bar(position_month, x="Album_release_month", y="Position",
                                    color_discrete_sequence=colors['collabbarcolors'],
                                    title="Release Month and Average Chart Position")

            position_month.update_layout(
                plot_bgcolor=colors['plot_bg_color'],
                paper_bgcolor=colors['plot_bg_color'],
                font_color=colors['txt_color1'],
                xaxis_title="Month",
                xaxis=dict(dtick=1)
            )

            return position_month

        elif data_source == 'Streams':
            streams_month = (
                collab_data.drop_duplicates('Track Name')
                    .groupby(['Album_release_month'])['Streams']
                    .mean()
                    .reset_index()
                    .sort_values(by='Album_release_month', ascending=True)
            )

            streams_month = px.bar(streams_month, x="Album_release_month", y="Streams",
                                   color_discrete_sequence=colors['collabbarcolors'],
                                   title="Release Month and Average Streams")

            streams_month.update_layout(
                plot_bgcolor=colors['plot_bg_color'],
                paper_bgcolor=colors['plot_bg_color'],
                font_color=colors['txt_color1'],
                xaxis_title="Month",
                xaxis=dict(dtick=1)
            )

            return streams_month

        elif data_source == 'Revenue':
            revenue_month = (
                collab_data.drop_duplicates('Track Name')
                    .groupby(['Album_release_month'])['Revenue']
                    .mean()
                    .reset_index()
                    .sort_values(by='Album_release_month', ascending=True)
            )

            revenue_month = px.bar(revenue_month, x="Album_release_month", y="Revenue",
                                   color_discrete_sequence=colors['collabbarcolors'],
                                   title="Release Month and Average Revenue")

            revenue_month.update_layout(
                plot_bgcolor=colors['plot_bg_color'],
                paper_bgcolor=colors['plot_bg_color'],
                font_color=colors['txt_color1'],
                xaxis_title="Month",
                xaxis=dict(dtick=1)
            )

            return revenue_month

    elif month_day == "Days":
        if data_source == 'Count':
            count_days = (
                collab_data.drop_duplicates('Track Name')
                    .groupby(['Album_release_dayweek'])
                    .count()
                    .reset_index()
                    .rename(columns={'Track URI2': 'Count'})
                    .sort_values(by='Album_release_dayweek', ascending=True)
            )

            count_days = px.bar(count_days, x='Album_release_dayweek', y='Count',
                                color_discrete_sequence=colors['collabbarcolors'],
                                title="Release Day and Count in Dataset")

            count_days.update_layout(
                plot_bgcolor=colors['plot_bg_color'],
                paper_bgcolor=colors['plot_bg_color'],
                font_color=colors['txt_color1'],
                xaxis_title="Day Of The Week",
                xaxis=dict(dtick=1)
            )

            return count_days

        elif data_source == 'Position':
            position_days = (
                collab_data.drop_duplicates('Track Name')
                    .groupby(['Album_release_dayweek'])['Position']
                    .mean()
                    .reset_index()
                    .sort_values(by='Album_release_dayweek', ascending=True)
            )

            position_days = px.bar(position_days, x='Album_release_dayweek', y="Position",
                                   color_discrete_sequence=colors['collabbarcolors'],
                                   title="Release Day and Average Chart Position")

            position_days.update_layout(
                plot_bgcolor=colors['plot_bg_color'],
                paper_bgcolor=colors['plot_bg_color'],
                font_color=colors['txt_color1'],
                xaxis_title="Day Of The Week",
                xaxis=dict(dtick=1)
            )

            return position_days

        elif data_source == 'Streams':
            streams_days = (
                collab_data.drop_duplicates('Track Name')
                    .groupby(['Album_release_dayweek'])['Streams']
                    .mean()
                    .reset_index()
                    .sort_values(by='Album_release_dayweek', ascending=True)
            )

            streams_days = px.bar(streams_days, x='Album_release_dayweek', y="Streams",
                                  color_discrete_sequence=colors['collabbarcolors'],
                                  title="Release Day and Average Streams")

            streams_days.update_layout(
                plot_bgcolor=colors['plot_bg_color'],
                paper_bgcolor=colors['plot_bg_color'],
                font_color=colors['txt_color1'],
                xaxis_title="Day Of The Week",
                xaxis=dict(dtick=1)
            )

            return streams_days

        elif data_source == 'Revenue':
            revenue_days = (
                collab_data.drop_duplicates('Track Name')
                    .groupby(['Album_release_dayweek'])['Revenue']
                    .mean()
                    .reset_index()
                    .sort_values(by='Album_release_dayweek', ascending=True)
            )

            revenue_days = px.bar(revenue_days, x='Album_release_dayweek', y="Revenue",
                                  color_discrete_sequence=colors['collabbarcolors'],
                                  title="Release Day and Average Revenue")

            revenue_days.update_layout(
                plot_bgcolor=colors['plot_bg_color'],
                paper_bgcolor=colors['plot_bg_color'],
                font_color=colors['txt_color1'],
                xaxis_title="Day Of The Week",
                xaxis=dict(dtick=1)
            )

            return revenue_days


#### Artist Radar Graphs ####
@app.callback(Output('artist_radar_graph', 'figure'),
              Input('artist_selections', 'value'))
def audio_radial_graph(artist_names):
    if artist_names == 'None' or artist_names == []:
        select_audio_features = collab_features_data[collab_features_data['Artist Name'].isin(
            ['Drake', 'Post Malone', 'Travis Scott', 'Khalid', 'Juice WRLD'])]
    else:
        select_audio_features = collab_features_data[collab_features_data['Artist Name'].isin(artist_names)]

    radar_graph = go.Figure()

    for i in select_audio_features['Artist Name'].unique():
        radar_graph.add_trace(go.Scatterpolar(
            r=select_audio_features[select_audio_features['Artist Name'] == i]['value'],
            theta=select_audio_features[select_audio_features['Artist Name'] == i]['variable'],
            fill='toself',
            name=i))

    radar_graph.update_layout(
        polar=dict(
            bgcolor=colors['plot_bg_color'],
            radialaxis=dict(
                visible=True,
                range=[0, 1])),
        title='Audio Features For Selected Artists',
        paper_bgcolor=colors['plot_bg_color'],
        font_color=colors['txt_color1'])

    return radar_graph


#### Count Metrics By Time ####
@app.callback(Output('count_time_plot', 'figure'),
              Input('track_artist', 'value'))
def count_days(track_artist):
    if track_artist == 'Artists':
        count_artistdays = (
            collab_data
                .groupby(['Artist_days_onchart'])
                .count()
                .reset_index()
                .rename(columns={"Artist Name": "Count"})
        )

        count_artistdays = px.scatter(count_artistdays, x="Artist_days_onchart", y="Count",
                                  color_discrete_sequence=[colors['main_color']],
                                  title='Count of Artists in the Dataset By Length of Time on The Chart'
                                  )

        count_artistdays.update_layout(
            plot_bgcolor=colors['plot_bg_color'],
            paper_bgcolor=colors['plot_bg_color'],
            font_color=colors['txt_color1'],
            xaxis_title="Length of Time on Chart (days)"
        )

        return count_artistdays

    elif track_artist == 'Tracks':
        count_trackdays = (
            collab_data
                .groupby(['Song_days_onchart'])
                .count()
                .reset_index()
                .rename(columns={"Track URI2": "Count"})
        )

        count_trackdays = px.scatter(count_trackdays, x="Song_days_onchart", y="Count",
                                     color_discrete_sequence=[colors['main_color']],
                                     title='Count of Tracks By Length of Time on The Chart'
                                     )

        count_trackdays.update_layout(
            plot_bgcolor=colors['plot_bg_color'],
            paper_bgcolor=colors['plot_bg_color'],
            font_color=colors['txt_color1'],
            xaxis_title="Length of Time on Chart (days)"
        )

        return count_trackdays

