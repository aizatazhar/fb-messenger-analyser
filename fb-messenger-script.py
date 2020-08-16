import os, json
import datetime
from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool, WheelZoomTool, PanTool, BoxZoomTool, ResetTool, TapTool,        SaveTool, FixedTicker, ColumnDataSource, LabelSet
import itertools

# Reads all the json files in the directory and returns a dictionary of the participants and combined messages
def readFiles():
    # Get all json files in the directory
    working_directory = os.getcwd()
    json_files = [file for file in os.listdir(working_directory) if file.endswith('.json')]

    # get the participants, assuming that user uses script correctly, the participants should be identical
    first_file = json_files[0]
    with open(first_file) as f:
        participants = json.load(f)["participants"]

    # combine all the messages into a single array
    messages = []
    for file in json_files:
        with open(file) as f:
            curr_file = json.load(f)
            messages += curr_file["messages"]

    result = {"participants": participants, "messages": messages}
    return result

# Returns a dictionary of participants in the messages and relevant information
def analyseData(data):
    # Get all participants of the conversation and initialise variables
    participants = {}
    for p in data["participants"]:
        participants[p["name"]] = {
            "total_per_day": {
                "Monday": 0,
                "Tuesday": 0,
                "Wednesday": 0,
                "Thursday": 0,
                "Friday": 0,
                "Saturday": 0,
                "Sunday": 0
            },
            "total_per_month": {
                "January": 0,
                "February": 0,
                "March": 0,
                "April": 0,
                "May": 0,
                "June": 0,
                "July": 0,
                "August": 0,
                "September": 0,
                "October": 0,
                "November": 0,
                "December": 0,
            },
            "total_per_year": {},
            "total_all_time": 0
        }

    # Count messages sent
    for message in data["messages"]:
        if message["sender_name"] not in participants:
            continue # defensive code

        # Increment total count per participant
        sender = participants[message["sender_name"]]
        sender["total_all_time"] += 1

        date = datetime.date.fromtimestamp(message["timestamp_ms"]/1000.0)

        # Increment day count per participant
        day = date.weekday() # 0-6 inclusive
        if day == 0:
            sender["total_per_day"]["Sunday"] += 1
        elif day == 1:
            sender["total_per_day"]["Monday"] += 1
        elif day == 2:
            sender["total_per_day"]["Tuesday"] += 1
        elif day == 3:
            sender["total_per_day"]["Wednesday"] += 1
        elif day == 4:
            sender["total_per_day"]["Thursday"] += 1
        elif day == 5:
            sender["total_per_day"]["Friday"] += 1
        elif day == 6:
            sender["total_per_day"]["Saturday"] += 1
        else:
            print("Error day")

        # Increment day count per participant
        month = date.month # 1-12 inclusive
        if month == 1:
            sender["total_per_month"]["January"] += 1
        elif month == 2:
            sender["total_per_month"]["February"] += 1
        elif month == 3:
            sender["total_per_month"]["March"] += 1
        elif month == 4:
            sender["total_per_month"]["April"] += 1
        elif month == 5:
            sender["total_per_month"]["May"] += 1
        elif month == 6:
            sender["total_per_month"]["June"] += 1
        elif month == 7:
            sender["total_per_month"]["July"] += 1
        elif month == 8:
            sender["total_per_month"]["August"] += 1
        elif month == 9:
            sender["total_per_month"]["September"] += 1
        elif month == 10:
            sender["total_per_month"]["October"] += 1
        elif month == 11:
            sender["total_per_month"]["November"] += 1
        elif month == 12:
            sender["total_per_month"]["December"] += 1
        else:
            print("Error month")

        # Increment year count per participant
        year = date.year
        if year in sender["total_per_year"]:
            sender["total_per_year"][year] += 1
        else:
            sender["total_per_year"][year] = 1

    return participants

# Wrapper method to standardise basic aspects of the figure
def build_standard_fig(**kwargs):
    tools = [WheelZoomTool(), PanTool(), BoxZoomTool(), ResetTool(), SaveTool()]
    tools.append(kwargs.get("hover")) if kwargs.get("hover") is not None else None

    fig = figure(
        plot_width = 1000,
        plot_height = 400,
        title = kwargs.get("title"),
        sizing_mode = "scale_both",
        x_axis_label = 'X',
        x_range = kwargs.get("x_range"),
        background_fill_color = "beige",
        background_fill_alpha = 0.25,
        tools = tools,
        toolbar_location = "below",
        toolbar_sticky = False,
    )

    # title styling
    fig.title.align = "center"
    fig.title.text_font_size = "14pt"

    # y-axis styling
    fig.yaxis.axis_label = kwargs.get("y_axis_label")
    fig.yaxis.axis_label_text_font_size = "12pt"
    fig.yaxis.axis_label_text_font_style= "bold"

    # x axis styling
    fig.xaxis.axis_label = kwargs.get("x_axis_label")
    fig.xaxis.axis_label_text_font_size = "12pt"
    fig.xaxis.axis_label_text_font_style = "bold"

    return fig

def plot_total_per_day(result):
    x = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    colors = itertools.cycle(["#EF476F", "#FFD166", "#06D6A0", "#118AB2", "#073B4C"])

    fig = build_standard_fig(
        x_range = x,
        y_axis_label = "Count",
        x_axis_label = "Day",
        title = "Total messages per day",
        hover = HoverTool(tooltips = [("Count", "$y{0}")], names = ["circles"],)
    )

    for participant, value, color in zip(result.keys(), result.values(), colors):
        daily = value["total_per_day"]
        y = []
        for day, count in daily.items():
            y.append(count)

        # plot the data
        fig.line(x, y, line_width = 3, color = color, alpha = 1, muted_color = color,
        muted_alpha = 0.2, legend_label = participant)
        fig.circle(x, y, size = 8, color = color, alpha = 0.9, muted_color = color, muted_alpha = 0.2, legend_label = participant, name = "circles")

    # legend styling
    fig.legend.click_policy = "mute"
    fig.legend.location = "top_left"

    output_file("total_per_day.html")
    return fig

def plot_total_per_month(result):
    x = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
            "October", "November", "December"]
    colors = itertools.cycle(["#EF476F", "#FFD166", "#06D6A0", "#118AB2", "#073B4C"])

    fig = build_standard_fig(
        x_range = x,
        y_axis_label = "Count",
        x_axis_label = "Month",
        title = "Total messages per month",
        hover = HoverTool(tooltips = [("Count", "$y{0}")], names = ["circles"],)
    )

    for participant, value, color in zip(result.keys(), result.values(), colors):
        monthly = value["total_per_month"]
        y = []
        for month, count in monthly.items():
            y.append(count)

        # plot the data
        fig.line(x, y, line_width = 3, color = color, alpha = 1, muted_color = color,
        muted_alpha = 0.2, legend_label = participant)
        fig.circle(x, y, size = 8, color = color, alpha = 0.9, muted_color = color, muted_alpha = 0.2, legend_label = participant, name = "circles")

    # legend styling
    fig.legend.click_policy = "mute"
    fig.legend.location = "top_left"

    output_file("total_per_month.html")
    return fig

def plot_total_per_year(result):
    x = []
    # gets all the years
    for value in result.values():
        year_values = value["total_per_year"]
        for v in year_values.keys():
            if v not in x: x.append(v)

    colors = itertools.cycle(["#EF476F", "#FFD166", "#06D6A0", "#118AB2", "#073B4C"])

    fig = build_standard_fig(
        title = "Total messages per year",
        hover = HoverTool(tooltips = [("Count", "$y{0}")], names = ["circles"],)
    )

    for participant, value, color in zip(result.keys(), result.values(), colors):
        yearly = value["total_per_year"]
        y = []
        for year, count in yearly.items():
            y.append(count)
        # plot the data
        fig.line(x, y, line_width = 3, color = color, alpha = 1, muted_color = color,
        muted_alpha = 0.2, legend_label = participant)
        fig.circle(x, y, size = 8, color = color, alpha = 0.9, muted_color = color, muted_alpha = 0.2, legend_label = participant, name = "circles")

    # title styling
    fig.title.align = "center"
    fig.title.text_font_size = "14pt"

    # y-axis styling
    fig.yaxis.axis_label = "Count"
    fig.yaxis.axis_label_text_font_size = "12pt"
    fig.yaxis.axis_label_text_font_style= "bold"

    # x axis styling
    fig.xaxis.axis_label = "Year"
    fig.xaxis.axis_label_text_font_size = "12pt"
    fig.xaxis.axis_label_text_font_style = "bold"

    # legend styling
    fig.legend.click_policy = "mute"
    fig.legend.location = "top_left"

    # sets the x-axis labels to be the years
    fig.xaxis[0].ticker = FixedTicker(ticks = x)

    output_file("total_per_year.html")
    return fig

def plot_total_all_time(result):
    color_palette = ["#EF476F", "#FFD166", "#06D6A0", "#118AB2", "#073B4C"]

    x = []
    y = []
    colors = []
    for participant, value, color in zip(result.keys(), result.values(), color_palette):
        x.append(participant)
        y.append(value["total_all_time"])
        colors.append(color)

    tools = [WheelZoomTool(), PanTool(), BoxZoomTool(), ResetTool(), SaveTool()]
    fig = figure(
        x_range = x,
        plot_height = 300,
        plot_width = 300,
        sizing_mode = "scale_height",
        title = "Total messages sent",
        toolbar_location = "below",
        tools = tools,
        toolbar_sticky = False,
        background_fill_color = "beige",
        background_fill_alpha = 0.25,
    )

    data = {"x_values": x, "y_values": y, "color_values": colors}
    source = ColumnDataSource(data = data)
    fig.vbar(
        x = "x_values",
        top = "y_values",
        width = 0.8,
        color = "color_values",
        legend_field = "x_values",
        source = source
    )

    # adds the count above the bar chart
    labels = LabelSet(x='x_values', y='y_values', text='y_values', level='glyph',
            x_offset=-13.5, y_offset=0, source=source, render_mode='canvas')
    fig.add_layout(labels)

    # title styling
    fig.title.align = "center"
    fig.title.text_font_size = "14pt"

    # y-axis styling
    fig.yaxis.axis_label = "Count"
    fig.yaxis.axis_label_text_font_size = "12pt"
    fig.yaxis.axis_label_text_font_style= "bold"
    fig.y_range.start = 0

    # x axis styling
    fig.xaxis.axis_label = "Sender"
    fig.xaxis.axis_label_text_font_size = "12pt"
    fig.xaxis.axis_label_text_font_style = "bold"

    # legend styling
    fig.legend.location = "top_left"

    # shows the actual numerical value instead of scientific
    fig.left[0].formatter.use_scientific = False

    output_file("total_messages_sent.html")
    return fig

def main():
    print("Reading files...")
    data = readFiles()

    print("Analysing data...")
    result = analyseData(data)

    print("Generating plots...")
    print("Generating total per day...")
    fig1 = plot_total_per_day(result)
    show(fig1)
    print("Success!")

    print("Generating total per month...")
    fig2 = plot_total_per_month(result)
    show(fig2)
    print("Success!")

    print("Generating total per year...")
    fig3 = plot_total_per_year(result)
    show(fig3)
    print("Success!")

    print("Generating total messages sent")
    fig4 = plot_total_all_time(result)
    show(fig4)
    print("Success!")

    print("All tasks completed successfully!")

main()
