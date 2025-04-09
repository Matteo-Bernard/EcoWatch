import tempfile
import matplotlib.pyplot as plt
import seaborn as sns

def BC(data, show=True):

    plt.figure(figsize=(12, 8))
    # Scatter plot with hue for years
    sns.scatterplot(
        x='Unemployment Rate',
        y='Job Openings Rate', 
        hue=data.index.year, 
        palette='plasma', 
        data=data, 
        legend='full',
        s=25
    )

    # Add a second-degree polynomial regression line
    sns.regplot(
        x='Unemployment Rate',
        y='Job Openings Rate',
        data=data,
        scatter=False,
        color='black',
        order=2,
        line_kws={'linewidth': 1, 'linestyle':'--'},
        ci=None
    )

    # Highlight the last point
    last_point = data.iloc[-1]
    plt.scatter(
        last_point['Unemployment Rate'], 
        last_point['Job Openings Rate'], 
        color='black', 
        s=25,
        edgecolor='white',
        zorder=5,
    )

    # Annotate the last point
    date_str = last_point.name.strftime('%m/%Y')  # Format the date as MM/YYYY
    plt.text(
        last_point['Unemployment Rate'], 
        last_point['Job Openings Rate'], 
        date_str, 
        fontsize=10, 
        ha='left',
        va='bottom'
    )

    # Customize plot
    plt.title('Beveridge Curve')
    plt.legend(title='Year', bbox_to_anchor=(1, 1), loc='upper left')

    if show:
        plt.show()
    else:
        bc_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        plt.savefig(bc_file.name, format='png', bbox_inches='tight')
        plt.close()
        return bc_file
