import pandas as pd
import plotly.express as px
from preprocess import get_law_data, sum_laws

df = get_law_data()
#print(df)

df_sums = sum_laws(df)
print(df_sums)

fig = px.choropleth(df_sums, locations='COUNTRY',
                    locationmode='country names', color="Sum",
                    color_continuous_scale='Viridis',
                    range_color=(0, 20),
                    scope="europe",
                    )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.update_geos(
    scope="europe",
    resolution=50
)
fig.show()