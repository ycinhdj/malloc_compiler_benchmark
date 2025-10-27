import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os

def abbreviate_number(number, abbreviation_type = "Normal"):
    number = int(number)
    if abbreviation_type == "Bytes":
        abbreviations = ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei"]
        base = 1024
    elif abbreviation_type == "Normal":
        abbreviations = ["", "K", "M", "B"]
        base = 1000
    else:
        return "Invalid abbreviation type."

    magnitude = 0
    while abs(number) >= base and magnitude < len(abbreviations) - 1:
        number /= base
        magnitude += 1

    #print(number)
    return f"{number:.0f}{abbreviations[magnitude]}"

bnw =['lightgray','dimgray','darkgray','black']

# Read the CSV file into a DataFrame
df = pd.read_csv('performance_results.csv')

# Group by Test Name, Compiler, and Size of Data, and calculate the mean Speed
grouped = df.groupby(['Test Name', 'Compiler', 'Size of Data'])['Speed'].mean().reset_index()

#drop all rows where Size of Data is 0
grouped = grouped[grouped['Size of Data'] != 0]

test_names = grouped['Test Name'].unique()
compiler_names = grouped['Compiler'].unique()
memory_sizes = grouped['Size of Data'].unique()

for test_name in test_names:

    df = grouped[(grouped['Test Name'] == test_name)]
    df = df[['Compiler', 'Size of Data', 'Speed']]
    df = df.pivot(index='Size of Data', columns='Compiler', values='Speed')

    #remove last 2 rows
    df = df.iloc[:-2]

    fig, axes = plt.subplots(nrows=2, gridspec_kw=dict(height_ratios=[3,1]))
    df.plot(ax = axes[0], kind='bar', use_index = True, width=.8, color=bnw)


    plt.suptitle(test_name, size = 10)
    axes[0].legend(loc = "best", fontsize="xx-small", ncol=3)
    
    axes[0].tick_params(axis='both', which='major', labelsize=6)
    axes[0].set_ylabel("Time (s)", fontsize=6)
    axes[0].set_xlabel("Memory Size", fontsize=6)
    
    #ticks_loc = [round(x, 2) for x in axes[0].get_yticks()]
    #axes[0].yaxis.set_major_locator(mticker.FixedLocator(ticks_loc))
    #y_labels = [abbreviate_number(int(x)) for x in ticks_loc]
    #axes[0].set_yticklabels(y_labels)

    x_labels = [abbreviate_number(int(x.get_text()), "Bytes") for x in axes[0].get_xticklabels()]
    axes[0].set_xticklabels(x_labels)


    #table
    rowslabels = df.columns.tolist()
    colslabels = ['min', 'mean', 'max']
    tabledata = []
    for i in rowslabels:
        data = [x for x in [df[i].min(), df[i].mean(), df[i].max()]]
        try:
            data = [abbreviate_number(int(x)) for x in data]
        except BaseException:
            pass
        tabledata.append(data)
    axes[1].axis('off')
    axes[1] = plt.table(
        cellText=tabledata,
        rowLabels=rowslabels,
        colLabels=colslabels,
        loc='center',
        cellLoc='center',
        colWidths=[.12 for x in colslabels])
    axes[1].scale(1,1.7)    
    axes[1].auto_set_font_size(False)
    axes[1].set_fontsize(5)
    

    fig.set_size_inches(3.2, 2.5)
    fig.tight_layout(h_pad=0, w_pad=0)

    #make the figure as compact as possible
    fig.subplots_adjust(top=.9, bottom=.08)


    #save figure in svg format in folder "plots" and create folder if it doesn't exist
    
    if not os.path.exists("plots"):
        os.makedirs("plots")
    plt.savefig("plots/" + test_name + ".pdf", format="pdf")
    plt.savefig("plots/" + test_name + ".svg", format="svg")

    #plt.show()