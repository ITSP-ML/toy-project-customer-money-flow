# %%

# Change the working directory to the project root
%cd C:\Users\feress\Documents\myprojects\toy-project-customer-money-flow

# OPTIONAL: Load the "autoreload" extension so that code can change
%load_ext autoreload

# OPTIONAL: always reload modules so that as you change code in src, it gets loaded
%autoreload 2

# %%
import matplotlib.pyplot as plt
import numpy as np

from src.transform.acquisitions import group_affiliate_acquisitions_timeseries

def get_style(colname, emphasized, distinguishUnfocusedColors, unfocusedInLegend):
    if colname in emphasized.keys():
        color = emphasized.get(colname)
        linewidth = 5
    elif distinguishUnfocusedColors:
        color = None
        linewidth = 2
    else:
        color = 'grey'
        linewidth = 2
    #
    if color is None:
        style = {'linewidth': linewidth}
    else:
        style = {'color': color, 'linewidth': linewidth}
    if (not unfocusedInLegend) and (colname not in emphasized.keys()):
        style['label'] = '_no_legend_'
    return style

def get_last_common_day(dfTimeseries):
    lastCommonDay = dfTimeseries.isna().any(axis=0).where(lambda s: s == False, np.nan).last_valid_index()
    #  alternative: dfTimeseries.sum(axis=1, skipna=False).last_valid_index()
    return lastCommonDay

def compute_relative_scale_ts(dfTimeseries, commonDay = None):
    if commonDay is None:
        commonDay = get_last_common_day(dfTimeseries)
    return dfTimeseries.div(dfTimeseries.loc[:, commonDay], axis='index')

def plot_affs_ts(dfTimeseries, emphasizedAffiliates ={}, title='', cis=None, trim = False, distinguishUnfocusedColors = True, maxLegendSize=20):
    if trim:
        lastCommonDay = get_last_common_day(dfTimeseries)
        dfTimeseries = dfTimeseries.loc[:, :lastCommonDay]
    unfocusedInLegend = (len(dfTimeseries) <= maxLegendSize) and distinguishUnfocusedColors
    for aff in dfTimeseries.index:
        style = get_style(aff, emphasizedAffiliates, distinguishUnfocusedColors, unfocusedInLegend)
        ax = dfTimeseries.loc[aff,:].plot(**style, grid = True)
        if cis is not None:
            c = cis.loc[:lastCommonDay,:] if trim else cis
            ax.fill_between(c.columns, dfTimeseries.loc[aff,:]-c.loc[aff,:], dfTimeseries.loc[aff,:]+c.loc[aff,:], alpha = 0.1, **style)
    ncols = len(dfTimeseries.index)//10 + 1
    #
    ylimmin = dfTimeseries.min().min()
    ylimmax = dfTimeseries.max().max()
    tol = 0.05
    plt.axis([None, None, ylimmin-tol*(ylimmax-ylimmin),ylimmax+tol*(ylimmax-ylimmin)]) # set y-limit to fit the curves, but allow confidence intervals to overflow
    plt.legend(fontsize='small', ncol=ncols, handleheight=2.4, labelspacing=0.02)
    plt.title(title)
    plt.show()

def plot_multiple(plots, emphasizedAffiliates = {}, cis=None,
                  trim = False, distinguishUnfocusedColors = True, maxLegendSize=20):
    for title, ts in plots.items():
        plot_affs_ts(ts, emphasizedAffiliates=emphasizedAffiliates, title=title, cis=None if cis is None else cis.get(title),
                     trim=trim, distinguishUnfocusedColors=distinguishUnfocusedColors, maxLegendSize=maxLegendSize)

def plot_acquisitions(dfTimeseries, emphasizedAffiliates = {}, cis=None,
                      trim=False, distinguishUnfocusedColors=True, maxLegendSize=20):
    dfTimeseriesFocusedVsOthers = group_affiliate_acquisitions_timeseries(dfTimeseries, emphasizedAffiliates.keys())
    #
    plots = {
        'All affiliates': dfTimeseries,
        'Focused vs others': dfTimeseriesFocusedVsOthers,
        'All affiliates - relative': compute_relative_scale_ts(dfTimeseries),
        'Focused vs others - relative': compute_relative_scale_ts(dfTimeseriesFocusedVsOthers),
    }
    plot_multiple(plots, emphasizedAffiliates=emphasizedAffiliates, cis=cis,
                  trim=trim, distinguishUnfocusedColors=distinguishUnfocusedColors, maxLegendSize=maxLegendSize)

def plot_amounts(dfTimeseries, dfTimeseriesFocusedVsOthers, cisTimeseries, cisTimeseriesFocusedVsOthers,
                 emphasizedAffiliates = {}, trim=False, distinguishUnfocusedColors=True, maxLegendSize=20):
    #
    plots = {
        'All affiliates': dfTimeseries,
        'Focused vs others': dfTimeseriesFocusedVsOthers,
        'Focused only': dfTimeseriesFocusedVsOthers.drop(index = 'Other'),
    }
    cis = {
        'All affiliates': cisTimeseries,
        'Focused vs others': cisTimeseriesFocusedVsOthers,
        'Focused only': cisTimeseriesFocusedVsOthers.drop(index = 'Other'),
    }
    plot_multiple(plots, emphasizedAffiliates=emphasizedAffiliates, cis=cis,
                  trim=trim, distinguishUnfocusedColors=distinguishUnfocusedColors, maxLegendSize=maxLegendSize)


# %%
import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np 


# %%
row_data = pd.read_csv("data_dump/row_equation_data_3.csv")
general_data = pd.read_csv("data_dump/customer_data_0.csv")
%matplotlib inline
row_data.head() 

# %%
def get_customer_data(customerID , table , all_columns , column_name = None ) : 
    if (all_columns) : 
        return table[table.customerID == customerID]
    else : 
        return table[table.customerID == customerID][column_name].values[0]


# %%
from datetime import date
dates = [date(1954, 7, 19), date(1959, 2, 3), date(1964, 2, 9), date(1965, 7, 25), date(1967, 6, 1), date(1969, 8, 15)]
min_date = date(np.min(dates).year - 2, np.min(dates).month, np.min(dates).day)
max_date = date(np.max(dates).year + 2, np.max(dates).month, np.max(dates).day)
 
labels = ['Elvis appears on\nthe Ed Sullivan Show', 'Buddy Holly dies', 'The Beatles appear\non the Ed Sullivan Show', 
          'Bob Dylan goes electric', 'The Beatles release\nSgt. Pepper', 'Woodstock']
# labels with associated dates
labels = ['{0:%d %b %Y}:\n{1}'.format(d, l) for l, d in zip (labels, dates)]
labels

# %%
general_data[general_data.customerID == 28774064].createdate.values[0]

# %%


def customer_timeline(customerID , data , data_g) : 
    customer_data = get_customer_data(customerID ,data , all_columns = True ) 
    create_date = get_customer_data(customerID ,data_g , all_columns=False , column_name=  'createdate')
    create_date = add_zero_padding(create_date)
    ## transfrom to date time
    create_date = change_to_datetime( create_date, date_format)
    plot_data = get_plot_data(customer_data , create_date) 
    balance_data = customer_data[customer_data.type =='balance' ]
    valid_to = []
    for i  in balance_data.reset_index().index : 
        if i < len(balance_data) -1 : 
            valid_to.append(balance_data.iloc[i+1].date)
        else : 
            valid_to.append(balance_data.iloc[-1].date +dt.timedelta(days = 2) )
    balance_data['valid_to'] = valid_to
    # return (customer_data , create_date)
    return plot_data , balance_data

    


# %%
valid_to = []
for i in bdata.reset_index().index: 
        print(i)
        if i < len(bdata) -1 : 
            valid_to.append(bdata.iloc[i+1].date)
        else : 
            valid_to.append(bdata.iloc[-1].date +dt.timedelta(days = 2) )
bdata['valid_to'] = valid_to
bdata

# %%
len(bdata)

# %%
def add_zero_padding(str_date) : 
    if len(str_date.split('.') ) > 1: 

        reste_of_date , micro_seconds = str_date.split('.')
        nb_of_degits = len(micro_seconds)
        if nb_of_degits < 6  : 
            micro_seconds = '0'*(6-nb_of_degits) + micro_seconds

        return reste_of_date +'.'+ micro_seconds
    else : 
        return str_date
    
def change_to_datetime(str_date , format ) : 
    if len(str_date.split())> 1 :
        if len(str_date.split('.')) > 1 :  
            return dt.datetime.strptime( str_date, format)
        else : 
            format_without_second = format.split('.')[0]
            return dt.datetime.strptime( str_date, format_without_second)
    else : 
        ## for only date without houres
        format_without_houres = format.split()[0]
        return dt.datetime.strptime( str_date, format_without_houres)

# %%
import datetime as dt 
def get_new_types(type , value) : 
    print(type , value)
    if type == 'bets' : 
        if value >= 0 : 
            return 'wins'
        else : 
            return 'loses'
    elif type in ["widthrow" , "chargeback" , "refund"] : 
        return 'pay_out'
    elif type == 'balance' : 
        return 'balance'
    else : 
        return 'pay_in'
date_format = "%Y-%m-%d %H:%M:%S.%f"
def get_plot_data(df , create_date) :
    df.date = df.date.apply(lambda x : add_zero_padding(x))
    ## transfrom to date time
    df.date = df.date.apply(lambda x : change_to_datetime(x , date_format))
    df[df.type == 'bets'].type =df[df.type == 'bets'].value.apply(lambda x : 'wins' if x>=0  else 'loses')
    final_result = pd.DataFrame(columns = ['date','type',"value" ,'balance','balance_nb' , 'from_date' ])
    balances = df[df.type == "balance"].sort_values(by= "date")
    prevous_calcul = 0
    previous_nb_transactions = 0 
    valid_from = create_date - dt.timedelta(days= 2 )
    i = 0
    for index , row in balances.iterrows():
        
        ## get for each bets, bonus, payement 
        date = row.date
        new_df = df[(df.date> valid_from) & (df.date <=  date) ]
        #others = new_df [new_df.type != "balance"]
        new_df["balance_nb"] = i
        new_df["balance"] = row.value 
        new_df['from_date'] = valid_from
        final_result =pd.concat([final_result,new_df[['date','type',"value" ,'balance','balance_nb','from_date'  ]]])
        
        valid_from = date
        i = i +1
    final_result.apply(get_new_types(final_result['type'] , final_result['value']))
    final_result['diif_balance'] = final_result.balance + final_result.value    
    return final_result

# %%
data.apply(get_new_types(data['type'] , data['value']) , axis = 1)

# %%
customer_data = get_customer_data(28774064 ,row_data , all_columns = True ) 
create_date = get_customer_data(28774064 ,general_data , all_columns=False , column_name=  'createdate')

# %%
## test  28774064
data , bdata = customer_timeline(28774064 , row_data , general_data)
data

# %%
bdata

# %%
row_data.iloc[0].date

# %%
df_office = pd.read_csv("https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-03-17/office_ratings.csv")
df_office.head()

# %%
df_office_avg = df_office.sort_values(["season", "episode"])
df_office_avg["episode_id"] = np.arange(len(df_office_avg)) + 1
df_office_avg["episode_mod"] =  df_office_avg["episode_id"] + (9 * df_office_avg["season"])
df_office_avg = df_office_avg.assign(
    avg = df_office_avg.groupby("season")["imdb_rating"].transform("mean"),
    mid = df_office_avg.groupby("season")["episode_mod"].transform("mean")
)
df_office_avg

# %%
import numpy as np
import pandas as pd
import matplotlib.colors as mc
import matplotlib.image as image
import matplotlib.pyplot as plt

from matplotlib.cm import ScalarMappable
from matplotlib.lines import Line2D
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from palettable import cartocolors

# %%
# Credit: https://stackoverflow.com/a/49601444/12266277
# This function takes a color and adjusts its lightness
# Values below 1 make it darker, values above 1 make it lighter.
def adjust_lightness(color, amount=0.5):
    import matplotlib.colors as mc
    import colorsys
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1])), c[2])

# %%
# Misc colors
GREY82 = "#d1d1d1"
GREY70 = "#B3B3B3"
GREY40 = "#666666"
GREY30 = "#4d4d4d"
BG_WHITE = "#fafaf5"

# These colors (and their dark and light variant) are assigned to each of the 9 seasons
COLORS = ["#486090", "#D7BFA6", "#6078A8", "#9CCCCC", "#7890A8","#C7B0C1", "#B5C9C9", "#90A8C0", "#A8A890"]
COLORS_DARK = [adjust_lightness(color, 0.8) for color in COLORS]
COLORS_LIGHT = [adjust_lightness(color, 1.2) for color in COLORS]

# Three colormaps with three variants
cmap_regular = mc.LinearSegmentedColormap.from_list("regular", COLORS)
cmap_dark = mc.LinearSegmentedColormap.from_list("dark", COLORS_DARK)
cmap_light = mc.LinearSegmentedColormap.from_list("light", COLORS_LIGHT)
# Function used to normalize season values into 0-1 scale.
normalize = mc.Normalize(vmin=1, vmax=9)

# The Office logo
#IMAGE = image.imread("the-office.png")

# Horizontal lines
HLINES = [6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10]


# %%
def scale_to_interval(x, low=15, high=150):
    return ((x - VOTES_MIN) / (VOTES_MAX - VOTES_MIN)) * (high - low) + low

# %%

customer_HLINES = list(np.linspace(np.abs(customer_data.value.min()) , np.abs(customer_data.value.max()) , 8).astype(int))
for h in customer_HLINES:
    plt.axhline(h, color=GREY82, zorder=0)

# %%
fig, ax = plt.subplots(figsize = (15, 10))


# Some layout stuff ----------------------------------------------
# Background color
fig.patch.set_facecolor(BG_WHITE)
ax.set_facecolor(BG_WHITE)

# First, horizontal lines that are used as scale reference
# zorder=0 to keep them in the background
customer_HLINES = list(np.linspace(data.value.min() , data.value.max() , 8).astype(int))
for h in customer_HLINES:
    plt.axhline(h, color=GREY82, zorder=0)

     
# Add vertical segments ------------------------------------------
# Vertical segments. 
# These represent the deviation of episode's rating from the mean rating of 
# the season they appeared.
plt.vlines(
    x="date", 
    ymin="diif_balance", 
    ymax="balance",
    color='g',
    data = data[data.type.isin(['deposit' , 'bonus' , 'wins'])]
)
plt.vlines(
    x="date", 
    ymin="diif_balance", 
    ymax="balance",
    color='r',
    data = data[data.type.isin(['widthdraw' ,  'chargeback' ,'refund' , 'loses'])]
)
# plt.plot("x", "y", "-", color=GREY40, data=df_lines)

# These represent the mean rating per season. 
# for index , row in bdata.iterrows():
plt.hlines(
    y="value", 
    xmin="from_date", 
    xmax="date",
    color=cmap_light(normalize(data[data.type == 'balance'].reset_index().index)),
    data = data[data.type == 'balance'] ) 
    



# %%
data

# %%
data[data.type == 'balance'].from_date[]

# %%
data , bdata

# %%
row_data[row_data.customerID == 28774064  ].sort_values(by = 'date')

# %%
plt.vlines(
    x="episode_mod", 
    ymin="imdb_rating", 
    ymax="avg",
    color=cmap_light(normalize(df_office_avg["season"])),
    data = df_office_avg
)

# %%
row_data[row_data.customerID == '']

# %%
fig, ax = plt.subplots(figsize = (15, 10))


# Some layout stuff ----------------------------------------------
# Background color
fig.patch.set_facecolor(BG_WHITE)
ax.set_facecolor(BG_WHITE)

# First, horizontal lines that are used as scale reference
# zorder=0 to keep them in the background
for h in HLINES:
    plt.axhline(h, color=GREY82, zorder=0)

     
# Add vertical segments ------------------------------------------
# Vertical segments. 
# These represent the deviation of episode's rating from the mean rating of 
# the season they appeared.
plt.vlines(
    x="episode_mod", 
    ymin="imdb_rating", 
    ymax="avg",
    color=cmap_light(normalize(df_office_avg["season"])),
    data = df_office_avg
)



# Add horizontal segments ----------------------------------------
# A grey line that connects mean values
# The third argument is the format string, either empty or "-"
plt.plot("x", "y", "-", color=GREY40, data=df_lines)

# These represent the mean rating per season. 
for season in df_lines["season"].unique():
    d = df_lines[df_lines["season"] == season]
    plt.plot("x_group", "y", "", color=cmap_dark(normalize(season)), lw=5, data=d, solid_capstyle="butt")

    
# Add dots ------------------------------------------------------- 
# The dots indicate each episode's rating, with its size given by the 
# number of votes.
plt.scatter(
    "episode_mod", 
    "imdb_rating",
    s = scale_to_interval(df_office_avg["total_votes"]),
    color=cmap_regular(normalize(df_office_avg["season"])), 
    data=df_office_avg,
    zorder=3
)


# Add labels -----------------------------------------------------
# They indicate the season and free us from using a legend.
midpoints = df_office_avg["mid"].unique()
for season, mid in enumerate(midpoints):
    color = cmap_dark(normalize(season + 1))
    plt.text(
        mid, 10.12, f" Season {season + 1} ", 
        color=color,
        weight="bold",
        ha="center",
        va="center",
        fontname="Special Elite",
        fontsize=11,
        bbox=dict(
            facecolor="none", 
            edgecolor=color, 
            linewidth=1,
            boxstyle="round", 
            pad=0.2
        )
    )


# Customize layout -----------------------------------------------
    
# Hide spines
ax.spines["right"].set_color("none")
ax.spines["top"].set_color("none")
ax.spines["bottom"].set_color("none")
ax.spines["left"].set_color("none")

# Customize y ticks
# * Remove y axis ticks 
# * Put labels on both right and left sides
plt.tick_params(axis="y", labelright=True, length=0)
plt.yticks(HLINES, fontname="Roboto Mono", fontsize=11, color=GREY30)
plt.ylim(0.98 * 6.5, 10.2 * 1.02)

# Remove ticks and legends
plt.xticks([], "")

# Y label
plt.ylabel("IMDb Rating", fontname="Roboto Mono", fontsize=14)

# Add caption
plt.text(
    0.5, -0.03, "Visualization by Cédric Scherer  •  Data by IMDb via data.world  •  Fanart Logo by ArieS", 
    fontname="Special Elite", 
    fontsize=11, 
    color=GREY70,
    ha="center", 
    va="center", 
    transform=ax.transAxes # so coordinates are in terms of the axis.
)

# Create annotation box to place image.
# It will be added at (1, 6.75) in data coordinates.
ab = AnnotationBbox(
    OffsetImage(IMAGE, zoom=0.2), 
    (1, 6.75), 
    xycoords="data", 
    box_alignment=(0, 0.5),
    pad=0, 
    frameon=False
)

# Add the annotation box into the axis
ax.add_artist(ab)


# Add custom legend ----------------------------------------------

# We create a horizontal legend from scratch so this plot looks as 
# much as possible like the original.

# Horizontal position for the dots and their labels
x_pos = [0.44, 0.48, 0.52, 0.56]
votes = [2000, 4000, 6000, 8000]

# Dots are in term of the (0, 1) coordinate system of the axis.
plt.scatter(
    x_pos, 
    [0.065] * 4, 
    s=scale_to_interval(np.array(votes)), 
    color="black",
    transform=ax.transAxes
)

# Add title to our custom legend
plt.text(0.5, 0.0875, "Votes per Episode", fontname="Roboto Mono", fontsize=10, ha="center", transform=ax.transAxes)

# Place legends below the legend markers
for (xpos, vote) in zip(x_pos, votes):
    plt.text(xpos, 0.035,  f"{vote}", fontname="Roboto Mono", fontsize=9, ha="center", transform=ax.transAxes)

# Now save the plot!
plt.savefig(
    "the-office-lollipop.png", 
    dpi=300,
    bbox_inches="tight",
    pad_inches=0.3
)


# %%
def customer_timeline(customerID= )