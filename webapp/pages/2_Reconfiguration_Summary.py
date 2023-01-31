import streamlit as st
import matplotlib.pyplot as plt
import numpy as np


st.set_page_config(layout="wide", page_title="Reconfiguration Summary", page_icon=":satellite:")

st.sidebar.title("About")
st.sidebar.info(
    """
    GitHub repository: <https://github.com/AntoineMellerio/natixis_challenge>
    """ 
)

st.title('Server Reconfiguration')

data = {
    "count_cpu_downgrade": 864, 
    "count_cpu_stay": 1043, 
    "count_cpu_upgrade": 419, 
    "count_ram_downgrade": 993,
    "count_ram_stay": 1187, 
    "count_ram_upgrade": 146
}

fig, ax = plt.subplots(figsize=[12, 6])

ax.barh(
    y=["CPU", "RAM"],
    width=[data[f"count_cpu_downgrade"], data[f"count_ram_downgrade"]],
    label="Downgraded",
    color="yellowgreen"
)
left = np.array([data[f"count_cpu_downgrade"], data[f"count_ram_downgrade"]])
ax.barh(
    y=["CPU", "RAM"],
    width=[data[f"count_cpu_stay"], data[f"count_ram_stay"]],
    left=left,
    label="Unchanged",
    color="grey"
)
left += np.array([data[f"count_cpu_stay"], data[f"count_ram_stay"]])
ax.barh(
    y=["CPU", "RAM"],
    width=[data[f"count_cpu_upgrade"], data[f"count_ram_upgrade"]],
    left=left,
    label="Upgraded",
    color="indianred"
)

cpu_x_annotation =  [864/2, 864+1043/2, 864+1043+419/2]
ram_x_annotation = [993/2, 993+1187/2, 993+1187+146/2]

i = 0
x_iterator = cpu_x_annotation
for y in [0.01, 1]:
    for x in x_iterator:
        ax.text(
            x=x,
            y=y,
            s=list(data.values())[i],
            ha="center",
            va="center",
            color="white",
            fontsize=16
        )
        i += 1
    x_iterator = ram_x_annotation

ax.legend(loc="lower right")
ax.xaxis.set_visible(False)
ax.spines[['right', 'bottom', 'top']].set_visible(False)
ax.tick_params(axis='both', which='major', labelsize=16)

st.pyplot(fig)

data = {
    "costs": {
        "before": 6_500_000,
        "after": 3_400_000
    },
    "ghg_emissions": {
        "before": 6_500_000,
        "after": 3_400_000
    }
}

fig, [[ax1, ax2], [ax3, ax4]] = plt.subplots(nrows=2, ncols=2, figsize=[12, 6])

circle1 = plt.Circle((1, 0.5), 0.45, color='rebeccapurple')
ax1.set_xlim(left=0, right=2)
ax1.get_xaxis().set_visible(False)
ax1.get_yaxis().set_visible(False)
ax1.spines[['left', 'right', 'bottom', 'top']].set_visible(False)
ax1.add_patch(circle1)
ax1.text(
    x= 1,
    y=0.5,
    s="6,500,000",
    color="white",
    ha="center",
    va="center",
    fontsize=14
)
ax1.set_title(
    label="Costs before (€)",
    fontsize=16
)


circle2 = plt.Circle((1, 0.5), 0.35, color='rebeccapurple')
ax2.set_xlim(left=0, right=2)
ax2.get_xaxis().set_visible(False)
ax2.get_yaxis().set_visible(False)
ax2.spines[['left', 'right', 'bottom', 'top']].set_visible(False)
ax2.add_patch(circle2)
ax2.text(
    x= 1,
    y=0.5,
    s="3,400,000",
    color="white",
    ha="center",
    va="center",
    fontsize=14
)
ax2.set_title(
    label="Costs after (€)",
    fontsize=16
)

circle3 = plt.Circle((1, 0.5), 0.45, color='mediumturquoise')
ax3.set_xlim(left=0, right=2)
ax3.get_xaxis().set_visible(False)
ax3.get_yaxis().set_visible(False)
ax3.spines[['left', 'right', 'bottom', 'top']].set_visible(False)
ax3.add_patch(circle3)
ax3.text(
    x= 1,
    y=0.5,
    s="2,400",
    color="white",
    ha="center",
    va="center",
    fontsize=14
)
ax3.set_title(
    label="GHG Emissions before (TeqCO2)",
    fontsize=16
)


circle4 = plt.Circle((1, 0.5), 0.30, color='mediumturquoise')
ax4.set_xlim(left=0, right=2)
ax4.get_xaxis().set_visible(False)
ax4.get_yaxis().set_visible(False)
ax4.spines[['left', 'right', 'bottom', 'top']].set_visible(False)
ax4.add_patch(circle4)
ax4.text(
    x= 1,
    y=0.5,
    s="1,600",
    color="white",
    ha="center",
    va="center",
    fontsize=14
)
ax4.set_title(
    label="GHG Emissions after (TeqCO2)",
    fontsize=16
)

st.pyplot(fig)