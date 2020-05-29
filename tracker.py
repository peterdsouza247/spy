from spy import df
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource

df["start_date_time"] = df["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
df["end_date_time"] = df["End"].dt.strftime("%Y-%m-%d %H:%M:%S")

cds = ColumnDataSource(df)

p = figure(x_axis_type = 'datetime', height = 64, width = 512, sizing_mode = "scale_width")
p.yaxis.minor_tick_line_color = None
p.title.text = "Motion Graph"
p.title.text_color = "grey"
p.xaxis.axis_label = "Time"
p.yaxis.axis_label = "Signal (1/0)"

hover = HoverTool(tooltips = [("Start", "@start_date_time"), ("End", "@end_date_time")])
p.add_tools(hover)

q = p.quad(left = "Start", right = "End", bottom = 0, top = 1, color = "green", source = cds)

output_file("Spy.html")
show(p)
