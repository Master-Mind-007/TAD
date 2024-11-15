const ctx = document.getElementById("myChart");
const sharkGray = "rgb(152,161,170)";
const cloudyGray = "rgb(208,211,216)";
const today = new Date();
const currMonth = parseInt(today.getMonth());
const currYear = parseInt(today.getFullYear());
const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
const monthLabels = [...months.slice(currMonth + 1), ...months.slice(0, currMonth + 1)];
const data = {
  labels: monthLabels,
  datasets: [{
      label: 'online sales',
      type: 'bar',
      data: [45, 53, 50, 48, 39, 60, 54, 47, 41, 32, 46, 39],
      borderColor: "rgba(83,172,223,1)",
      backgroundColor: "rgba(83,172,223,.3)",
      hoverBackgroundColor: "rgba(83,172,223,.6)",
      borderWidth: 1,
      stack: 'Stack 0',
    },
    {
      type: 'bar',
      label: 'in store-sales',
      data: [33, 36, 45, 39, 43, 51, 41, 29, 39, 25, 37, 31],
      borderColor: "rgba(80,208,131,1)",
      backgroundColor: "rgba(80,208,131,.3)",
      hoverBackgroundColor: "rgba(80,208,131,.6)",
      borderWidth: 1,
      stack: 'Stack 0',
    },
    {
      type: 'bar',
      label: 'expenses',
      data: [25, 29, 21, 15, 18, 33, 34, 37, 41, 49, 43, 22],
      borderColor: "rgba(236,107,106,1)",
      backgroundColor: "rgba(236,107,106,.3)",
      hoverBackgroundColor: "rgba(236,107,106,.6)",
      borderWidth: 1,
    },
    {
      type: 'line',
      label: 'profit',
      data: [53, 60, 74, 72, 64, 78, 61, 39, 39, 8, 40, 48],
      pointStyle: 'rectRot',
      pointRadius: 7,
      pointHoverRadius: 9,
      borderColor: "rgb(241,186,58, 1)",
      backgroundColor: "rgba(241,186,58, .3)",
      hoverBackgroundColor: "rgb(241,186,58, .6)",
      tension: 0.2,
      borderWidth: 1,
    },
    {
      type: 'line',
      label: 'profit goal',
      data: [55, 63, 70, 68, 69, 67, 65, 42, 35, 12, 44, 46],
      pointStyle: 'circle',
      pointRadius: 4,
      pointHoverRadius: 7,
      borderColor: sharkGray,
      backgroundColor: cloudyGray,
      hoverBackgroundColor: sharkGray,
      tension: 0.2,
      borderWidth: 1,
      fill: '-1'
    },
  ]
};
/*********************************
 PLUGINS
**********************************/
const legendPlugin = {
  afterUpdate(chart) {
    const items = chart.options.plugins.legend.labels.generateLabels(chart);
    const legend = document.getElementById("chart-legend");
    // Remove old legend items
    while (legend.firstChild) {
      legend.firstChild.remove();
    }
    // Create legend items
    items.map((item, index) => {
      const li = document.createElement("li");
      li.classList.add("chart-legend-item");
      li.onclick = (e) => {
        chart.setDatasetVisibility(item.datasetIndex, !chart.isDatasetVisible(item.datasetIndex));
        chart.update();
      };
      //legend item box
      const box = document.createElement("div");
      box.classList.add("chart-legend-item-box");
      if (data.datasets[item.datasetIndex].label === 'profit') {
        box.classList.add("chart-legend-item-rhombus");
      } else if (data.datasets[item.datasetIndex].label === 'profit goal') {
        box.classList.add("chart-legend-item-circle");
      } else {
        box.classList.add("chart-legend-item-rect");
      }
      if (item.hidden) {
        box.style.background = cloudyGray;
        box.style.borderColor = sharkGray;
        box.style.setProperty("--hoverColor", sharkGray);
      } else {
        box.style.background = item.fillStyle;
        box.style.borderColor = item.strokeStyle;
        box.style.setProperty(
          "--hoverColor",
          data.datasets[index].hoverBackgroundColor
        );
      }
      // legend item label
      const label = document.createElement("p");
      label.classList.add("chart-legend-item-label");
      label.style.textDecoration = item.hidden ? "line-through" : "none";
      const text = document.createTextNode(item.text);
      label.appendChild(text);
      li.appendChild(box);
      li.appendChild(label);
      legend.appendChild(li);
    });
  }
};
const tooltipPlugin = {
  usePointStyle: true,
  titleAlign: 'center',
  bodyFont: {
    size: 15
  },
  titleFont: {
    size: 18,
  },
  callbacks: {
    title: function(context) {
      return months[context[0].label];
    },
    labelPointStyle: function(context) {
      let style = 'rect';
      let rotationVal = 0;
      if (context.datasetIndex === 4) style = 'circle';
      if (context.datasetIndex === 3) {
        style = 'rectRot';
        rotationVal = 90;
      };
      return {
        pointStyle: style,
        rotation: rotationVal,
      }
    },
    label: function(context) {
      return context.dataset.label;
    },
    afterLabel: function(context) {
      return '$' + context.formattedValue + ' mil';
    },
  }
}
const headerPlugin = {
  beforeInit() {
    const title = document.getElementById('chart-title');
    const prevYear = parseInt(currYear) - 1;
    title.innerHTML = `Sales and Expenses - ${prevYear}/${currYear}`;
    const date = document.getElementById('currDate');
    date.innerHTML = `${months[currMonth].substring(0,3)}. ${today.getDate()}, ${today.getFullYear()}`;
  }
}
const config = {
  type: 'bar',
  data: data,
  options: {
    plugins: {
      title: {
        display: false,
        text: 'Sales and Expenses - Last 12 Months'
      },
      legend: {
        display: false
      },
      tooltip: tooltipPlugin,
    },
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      y: {
        title: {
          display: true,
          text: '$ dollars',
          beginAtZero: true
        },
        ticks: {
          callback: function(value, index, ticks) {
            return '$' + value + ' mil';
          }
        }
      },
    },
  },
  plugins: [legendPlugin, headerPlugin]
};
Chart.defaults.font.family = "'Montserrat'";
new Chart("myChart", config);
