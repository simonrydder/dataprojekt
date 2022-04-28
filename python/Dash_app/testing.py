
import pandas as pd
from ast import literal_eval

import plotly.graph_objects as go
def find_next_line(x,y,L):
    for idx,((x1,y1),(x2,y2)) in enumerate(L):
        if (x1,y1) == (x,y):
            return ((x1,y1),(x2,y2),idx)

            
L = [((1,2),(2,2)),((2,2),(2,3)),((2,3),(3,3)),((3,3),(3,2)),((3,2),(3,1)),
((3,1),(2,1)),((2,1),(1,1)),((1,1),(1,2))]



def find_true_lines(L):
    final = []
    while True:
        (x1_old,y1_old),(x2_old,y2_old) = L.pop(0)
        
        try:
            ((_,_),(x2_new,y2_new),idx) = find_next_line(x2_old,y2_old,L)
        except TypeError:
            L.append(((x1_old,y1_old),(x2_old,y2_old)))
            break

        if x1_old != x2_new and y1_old != y2_new:
            final.append(((x1_old,y1_old),(x2_old,y2_old)))
        elif x1_old == x2_new or y1_old == y2_new:
            new_line = ((x1_old,y1_old),(x2_new,y2_new))
            L.pop(idx)
            L.append(new_line)

    return L+final

find_true_lines(L)


    

df = pd.read_csv("C:\\Users\\alexk\Desktop\\Git\\dataprojekt\\data\\sliceresults\\dataframes\\GTvsDL&brainstem&Tolerance0.csv")

df["LinesModel"] = df["LinesModel"].replace(["set()"],["[]"])
df["LinesModel"] = df["LinesModel"].apply(literal_eval)

lines = df["LinesModel"][85]
lines = list(lines)

lines_test = find_true_lines(lines)


fig3 = go.Figure()
for (x0,y0),(x1,y1) in lines_test:
                x = [x0,x1]
                y = [y0,y1]
                fig3.add_trace(
                    go.Scatter(x = x, 
                                y = y, 
                                mode = "lines",
                                line = dict(dash = "dot"),showlegend = False, marker = dict(color = "darkcyan")))


fig3.show()








