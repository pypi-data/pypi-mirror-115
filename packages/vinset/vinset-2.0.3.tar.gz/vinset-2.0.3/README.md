# VINSET
Video inset function

This toolbox provides a commandline function that will insert a graph (defined in a CSV file) into a video 
________________________
# Installation requirements and guide
## Step 1: Python 3.9
If your base python interpreter is version 3.9, you can skip this step.
If not, please create the virtual environment as follow:

If you are using anaconda, please open the `Anaconda Powershell Prompt` and then
```
conda create -n your-environment-name python=3.9
```
```
conda activate your-environment-name
```
If not, please

(FOR LINUX/MAC)

install venv 
```
sudo apt-get install python3.9-venv
```
create virtual my_env_name
```
python3 -m venv my_env_name
```
activate virtual my_env_name
```
source my_env_name/bin/activate
```

(FOR WINDOWS)

install venv
```
py -m pip install --user virtualenv
```
create virtual my_env_name
```
py -m venv my_env_name
```
activate virtual my_env_name
```
.\my_env_name\Scripts\activate
```

## Step 2: Opencv-python
If your base python interpreter is version 3.9,
```
pip install opencv-python --upgrade
```
if not, activate your virtual environment that your created with python version 3.9 and
```
pip install opencv-python --upgrade
```
## Step 3: Install
If it is the first time installation,
```
pip install vinset
```
If it has been installed before,
```
pip install vinset --upgrade
```
_________________________________
# User guide
## Example usage

```
vinset -i input_video.mp4 -o output_video.mp4 -c config.json 
```
## CSV file format
The configuration file will reference ```data.csv``` which will have format:

```
DataID, CurrentTime, Height, Velocity
1, 0, 0.123, 0.566
1, 0.1, 0.146, 0.232
2, 0.2, 0.157, 0.447
2, 0.3, 0.170, 0.677

...

5, 10.4, 2.321, 0.2442
5, 10.5, 2.324, 0.679
```
DataID column is optional but it can be filter by given config file.


## Example configuration file

```
{"csv_data" : "data.csv",
  "display": "True",
  "axes" : [ {  "name" : "main",
                "box_title": "Left",
                "box_title_font_scale": 0.8,
                "box_color": "red",
                "box_thickness": "2",
                "background" : { "fill":"black", "opacity" : 0.1 },
                "position" :  { "x" : 100, "y" : 100, "width" : 500, "height" : 250 } } ],
  "series" : [ { "name"  : "displacement",
                "parent_axes" : "main",
                "line_color": "green",
                "line_thickness": 2,
                "zero_line_display": "True",
                "zero_line_thickness": 1,
                "display_type": "pen",
                "t_label"     : "CurrentTime",
                "y_label"     : "D / V",
                "label_thickness": 1,
                "label_font_scale": 0.6,
                "t_data": "record_timestamp",
                "y_data": "y_nom",
                "filter": "FaLSE",
                "filterBy" : "DataID=2",
                "pointer_value": {"Enabled": "True", "Color": "red", "Radius": 4},
                "y-limit" : { "type" : "fixed", "limits" : { "lower" : -1, "upper" : 2 } },
                "t-limit" : { "type" : "time",  "width" : 10 }},
                { "name"  : "velocity",
                "parent_axes" : "main",
                  "line_color": "magenta",
                  "line_thickness": 1,
                  "zero_line_display": "True",
                "zero_line_thickness": 1,
                "display_type": "refresh",
                "t_label"     : "CurrentTime",
                "y_label"     : "D / V",
                  "label_thickness": 1,
                  "label_font_scale": 0.6,
                  "t_data": "record_timestamp",
                "y_data": "y_value",
                  "filter": "False",
                "filterBy" : "DataID=5",
                  "pointer_value": {"Enabled": "True", "Color": "red", "Radius": 4},
                "y-limit" : { "type" : "fixed", "limits" : { "lower" : -100, "upper" : 100 } },
                "t-limit" : { "type" : "time",  "width" : 10 }}]}
```
## Configuration format explanation
### csv_data = input csv file.

### display = video will be displayed during producing video if it is true.

### axes = the information of graph boxes.

1.  name = the name of the axes that will be checked from series information.
2.  box_title = the name of the graph box.
3.  box_title_font_scale = the font scale of tile
4.  box_color = the color of the box.
5.  box_thickess = the thickness of line of box.
6.  background = the color and opacity of background rectangle box.
7.  position = x, y coordinates, width and height information of the box.

### series = the information of labels and lines.

1.  name = the name or type of line.
2.  parent_axes = the name of parent axes to be called.
3.  line_color = the color of data line.
4.  line_thickness = the color of data line thickess.
5.  zero_line_display = the zero level line will be displayed if it is true and it is actually within lower and upper limit.
6.  zero_line_thickess = the thickess of zero line
7.  display_type = the display type of line. It can be "pen" or "refresh". If it is "pen", it will be drawn with time. If it is "refresh", the whole line will be displayed within time scale and refresh to another display page.
8.  t_label = the label name for time/x axis.
9.  y_label = the label name of y axis.
10.  label_thickess = the thickess of label.
11.  label_font_scale = the font scale of label.
12.  t_data = the column name of csv file for time/ x axis data.
13.  y_data = the column name of csv file for y axis data
14.  filter = it will filter "DataID" column if it is true.
15.  filterBy = the column name of csv file and the value to be used to filter. eg. "DataID=4"
16.  pointer_value = the color and radius information of pointer whether it is enabled or not.
17.  y-limit = type and limits of y axis
18.  t-limit = type and width of time/x axis

### Note: 
1.  Color information can be tuple string eg. "(0,0,255)" or 6 hex color code eg. "#ffffff" or basic color strings which are "red", "green", "blue", "yellow", "black", "white" and "magenta".
2.  Zero line will be displayed if it is enabled and it is actually can be drawn according to the lower limit and upper limit. eg. If lower limit is 1 and upper limit is 2, zero line cannot be drawn.
