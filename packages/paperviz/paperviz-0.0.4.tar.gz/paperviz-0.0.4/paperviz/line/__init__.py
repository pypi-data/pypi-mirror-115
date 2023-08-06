from line import line
line=line()
read_data=line.read_file(file='Line\museum_visitors_line.csv')
line.plot(file=read_data, x_col_name=['Avila_Adobe','Firehouse_Museum','Chinese_American_Museum','America_Tropical_Interpretive_Center'], 
            y_col_name=['iter'], x_label=['Avila_Adobe','Firehouse_Museum','Chinese_American_Museum','America_Tropical_Interpretive_Center'], 
            y_label=['iter'], legend_label=['Avila_Adobe','Firehouse_Museum','Chinese_American_Museum','America_Tropical_Interpretive_Center'],
             paper_type='csv')