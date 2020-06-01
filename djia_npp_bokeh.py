'''
-------------------------------------------------------------------------------
This script creates a normalized peak plot of the Dow Jones Industrial Average
for each of the last 15 recessions from the current 2020 COVID-19 recession to
the Great Depression of 1929, using Bokeh.

This script imports the following module(s):
    get_djia_data.py
-------------------------------------------------------------------------------
'''
# Import packages
import numpy as np
import datetime as dt
import os
import get_djia_data as getdjia
from bokeh.io import output_file
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, Title, Legend, HoverTool
# from bokeh.models import Label
from bokeh.palettes import Category20

'''
-------------------------------------------------------------------------------
Create normalized peak plot bokeh image
-------------------------------------------------------------------------------
'''

# Create directory if images directory does not already exist
cur_path = os.path.split(os.path.abspath(__file__))[0]
image_fldr = 'images'
image_dir = os.path.join(cur_path, image_fldr)
if not os.access(image_dir, os.F_OK):
    os.makedirs(image_dir)

# Get the data
DJIA_end_date_today = False
download_from_internet = True

if DJIA_end_date_today:
    end_date = dt.date.today()  # Go through today
else:
    end_year = 2020
    end_month = 5
    end_day = 29
    end_date = dt.date(end_year, end_month, end_day)

end_date_str = end_date.strftime('%Y-%m-%d')
end_date_str2 = end_date.strftime('%-m/%-d/%y')

# Set main window and total data limits for monthly plot
frwd_mths_main = int(5)
bkwd_mths_main = int(1)
frwd_days_main = int(np.round(frwd_mths_main * 364.25 / 12))
bkwd_days_main = int(np.round(bkwd_mths_main * 364.25 / 12))
frwd_mths_max = int(12)
bkwd_mths_max = int(3)
frwd_days_max = int(np.round(frwd_mths_max * 364.25 / 12))
bkwd_days_max = int(np.round(bkwd_mths_max * 364.25 / 12))

(djia_close_pk, peak_vals, peak_dates, rec_label_yr_lst,
    rec_label_yrmth_lst, rec_beg_yrmth_lst, maxdate_rng_lst) = \
    getdjia.get_djia_data(frwd_days_max, bkwd_days_max, end_date_str,
                          download_from_internet)

rec_cds_list = []
min_main_val_lst = []
max_main_val_lst = []
for i in range(15):
    djia_close_pk_rec = \
        djia_close_pk[['days_frm_peak', f'Date{i}', f'Close{i}',
                       f'close_dv_pk{i}']].dropna()
    djia_close_pk_rec.rename(
            columns={f'Date{i}': 'Date', f'Close{i}': 'Close',
                     f'close_dv_pk{i}': 'close_dv_pk'}, inplace=True)
    rec_cds_list.append(ColumnDataSource(djia_close_pk_rec))
    # Find minimum and maximum close_dv_pk values as inputs to main plot frame
    # size
    min_main_val_lst.append(
        djia_close_pk_rec['close_dv_pk'][(djia_close_pk_rec['days_frm_peak'] >=
                                          -bkwd_days_main) &
                                         (djia_close_pk_rec['days_frm_peak'] <=
                                          frwd_days_main)].min())
    max_main_val_lst.append(
        djia_close_pk_rec['close_dv_pk'][(djia_close_pk_rec['days_frm_peak'] >=
                                          -bkwd_days_main) &
                                         (djia_close_pk_rec['days_frm_peak'] <=
                                          frwd_days_main)].max())

# Create Bokeh plot of DJIA normalized peak plot figure
fig_title = 'Progression of DJIA in last 15 recessions'
filename = ('images/DJIA_NPP_mth_' + end_date_str + '.html')
output_file(filename, title=fig_title)

# Format the tooltip
tooltips = [('Date', '@Date{%F}'),
            ('Days from peak', '$x{0.}'),
            ('Closing value', '@Close{0,0.00}'),
            ('Fraction of peak', '@close_dv_pk{0.0 %}')]

# Solve for minimum and maximum DJIA/Peak values in monthly main display window
# in order to set the appropriate xrange and yrange
min_main_val = min(min_main_val_lst)
max_main_val = max(max_main_val_lst)

datarange_main_vals = max_main_val - min_main_val
datarange_main_days = int(np.round((frwd_mths_main + bkwd_mths_main) *
                                   364.25 / 12))
fig_buffer_pct = 0.07
fig = figure(plot_height=450,
             plot_width=800,
             x_axis_label='Months from Peak',
             y_axis_label='DJIA as fraction of Peak',
             y_range=(min_main_val - fig_buffer_pct * datarange_main_vals,
                      max_main_val + fig_buffer_pct * datarange_main_vals),
             x_range=((-np.round(bkwd_mths_main * 364.25 / 12) -
                       fig_buffer_pct * datarange_main_days),
                      (np.round(frwd_mths_main * 364.25 / 12) +
                       fig_buffer_pct * datarange_main_days)),
             tools=['save', 'zoom_in', 'zoom_out', 'box_zoom',
                    'pan', 'undo', 'redo', 'reset', 'hover', 'help'],
             toolbar_location='left')
fig.title.text_font_size = '18pt'
fig.toolbar.logo = None
l0 = fig.line(x='days_frm_peak', y='close_dv_pk', source=rec_cds_list[0],
              color='blue', line_width=5, alpha=0.7, muted_alpha=0.15)
l1 = fig.line(x='days_frm_peak', y='close_dv_pk', source=rec_cds_list[1],
              color=Category20[13][0], line_width=2, alpha=0.7,
              muted_alpha=0.15)
l2 = fig.line(x='days_frm_peak', y='close_dv_pk', source=rec_cds_list[2],
              color=Category20[13][1], line_width=2, alpha=0.7,
              muted_alpha=0.15)
l3 = fig.line(x='days_frm_peak', y='close_dv_pk', source=rec_cds_list[3],
              color=Category20[13][2], line_width=2,
              alpha=0.7, muted_alpha=0.15)
l4 = fig.line(x='days_frm_peak', y='close_dv_pk', source=rec_cds_list[4],
              color=Category20[13][3], line_width=2, alpha=0.7,
              muted_alpha=0.15)
l5 = fig.line(x='days_frm_peak', y='close_dv_pk', source=rec_cds_list[5],
              color=Category20[13][4], line_width=2, alpha=0.7,
              muted_alpha=0.15)
l6 = fig.line(x='days_frm_peak', y='close_dv_pk', source=rec_cds_list[6],
              color=Category20[13][5], line_width=2, alpha=0.7,
              muted_alpha=0.15)
l7 = fig.line(x='days_frm_peak', y='close_dv_pk', source=rec_cds_list[7],
              color=Category20[13][6], line_width=2, alpha=0.7,
              muted_alpha=0.15)
l8 = fig.line(x='days_frm_peak', y='close_dv_pk', source=rec_cds_list[8],
              color=Category20[13][7], line_width=2, alpha=0.7,
              muted_alpha=0.15)
l9 = fig.line(x='days_frm_peak', y='close_dv_pk', source=rec_cds_list[9],
              color=Category20[13][8], line_width=2, alpha=0.7,
              muted_alpha=0.15)
l10 = fig.line(x='days_frm_peak', y='close_dv_pk', source=rec_cds_list[10],
               color=Category20[13][9], line_width=2, alpha=0.7,
               muted_alpha=0.15)
l11 = fig.line(x='days_frm_peak', y='close_dv_pk', source=rec_cds_list[11],
               color=Category20[13][10], line_width=2, alpha=0.7,
               muted_alpha=0.15)
l12 = fig.line(x='days_frm_peak', y='close_dv_pk', source=rec_cds_list[12],
               color=Category20[13][11], line_width=2, alpha=0.7,
               muted_alpha=0.15)
l13 = fig.line(x='days_frm_peak', y='close_dv_pk', source=rec_cds_list[13],
               color=Category20[13][12], line_width=2, alpha=0.7,
               muted_alpha=0.15)
l14 = fig.line(x='days_frm_peak', y='close_dv_pk', source=rec_cds_list[14],
               color='black', line_width=5, alpha=0.7, muted_alpha=0.15)

lpeak = fig.line(x=[0.0, 0.0], y=[-0.5, 2.0], color='black',
                 line_width=2, line_dash='dashed', alpha=0.5)
lhoriz = fig.line(x=[-np.round(bkwd_mths_max * 364.25 / 12),
                     np.round(frwd_mths_max * 364.25 / 12)],
                  y=[1.0, 1.0], color='black', line_width=2,
                  line_dash='dashed', alpha=0.5)

# Create the tick marks for the x-axis and set x-axis labels
days_frm_pk_mth = []
mths_frm_pk = []
for i in range(-bkwd_mths_max, frwd_mths_max + 1):
    days_frm_pk_mth.append(int(np.round(i * 364.25 / 12)))
    if i < 0:
        mths_frm_pk.append(str(i) + 'mth')
    elif i == 0:
        mths_frm_pk.append('peak')
    elif i > 0:
        mths_frm_pk.append('+' + str(i) + 'mth')

mth_label_dict = dict(zip(days_frm_pk_mth, mths_frm_pk))
fig.xaxis.ticker = days_frm_pk_mth
fig.xaxis.major_label_overrides = mth_label_dict

# Add legend
legend = Legend(items=[(rec_label_yrmth_lst[0], [l0]),
                       (rec_label_yrmth_lst[1], [l1]),
                       (rec_label_yrmth_lst[2], [l2]),
                       (rec_label_yrmth_lst[3], [l3]),
                       (rec_label_yrmth_lst[4], [l4]),
                       (rec_label_yrmth_lst[5], [l5]),
                       (rec_label_yrmth_lst[6], [l6]),
                       (rec_label_yrmth_lst[7], [l7]),
                       (rec_label_yrmth_lst[8], [l8]),
                       (rec_label_yrmth_lst[9], [l9]),
                       (rec_label_yrmth_lst[10], [l10]),
                       (rec_label_yrmth_lst[11], [l11]),
                       (rec_label_yrmth_lst[12], [l12]),
                       (rec_label_yrmth_lst[13], [l13]),
                       (rec_label_yrmth_lst[14], [l14])],
                location='center')
fig.add_layout(legend, 'right')

# # Add label to current recession low point
# fig.text(x=[12, 12, 12, 12], y=[0.63, 0.60, 0.57, 0.54],
#          text=['2020-03-23', 'DJIA: 18,591.93', '63.3% of peak',
#                '39 days from peak'],
#          text_font_size='8pt', angle=0)

# label_text = ('Recent low \n 2020-03-23 \n DJIA: 18,591.93 \n '
#               '63\% of peak \n 39 days from peak')
# fig.add_layout(Label(x=10, y=0.65, x_units='screen', text=label_text,
#                      render_mode='css', border_line_color='black',
#                      border_line_alpha=1.0, background_fill_color='white',
#                      background_fill_alpha=1.0))

# Add title and subtitle to the plot
fig.add_layout(Title(text=fig_title, text_font_style='bold',
                     text_font_size='16pt', align='center'), 'above')

# Add source text below figure
fig.add_layout(Title(text='Source: Richard W. Evans (@RickEcon), ' +
                          'historical DJIA data from Stooq.com, ' +
                          'updated May 29, 2020.',
                     align='left',
                     text_font_size='3mm',
                     text_font_style='italic'),
               'below')
fig.legend.click_policy = 'mute'

# Add the HoverTool to the figure
fig.add_tools(HoverTool(tooltips=tooltips, toggleable=False,
                        formatters={'@Date': 'datetime'}))

show(fig)
