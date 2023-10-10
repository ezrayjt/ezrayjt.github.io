let state_name;
let aus_data;

async function init(){
  const aus_url = 'https://ta21-2023-s2.azurewebsites.net/api/get_data';
  const response = await fetch(aus_url);
  aus_data = await response.json();
}

init();

let all_paths = document.querySelectorAll(".paths");
all_paths.forEach(path => {
  path.addEventListener("mouseover", e => {
    const divElement = document.getElementById("aus-map");
    const rect = divElement.getBoundingClientRect();
    
    let x = e.clientX - rect.left; // Calculate x relative to the div
    let y = e.clientY - rect.top;
    
    let maptip_style = document.getElementById("map-tip").style;
    maptip_style.display = "block";
    maptip_style.top = y - 120 + "px";
    maptip_style.left = x - 120 + "px";
    // A 1ms delay is enough to ensure the fade-in animation happens - otherwise it doesn't
    setTimeout(() => {
      maptip_style.opacity = "0.7";  
    }, 1);

    document.getElementById("state-name").innerHTML = path.id;
  });

  path.addEventListener("mouseleave", () => {
    let maptip_style = document.getElementById("map-tip").style;
    maptip_style.opacity = "0";
    // Wait for the animation to finish before hiding the box
    setTimeout(() => {
      // Bug fix: If the cursor has moved to a different state then we shouldn't remove the box
      if (maptip_style.opacity == "0"){  
        maptip_style.display = "none";
      }
    }, 500);
  });
  
  path.addEventListener("click", () => {
    path.classList.toggle("selected");
    all_paths.forEach(region => {
      if (region != path && region.classList.contains("selected")) {
        region.classList.remove("selected");
      }
    })
    state_name = path.id;
    updateChart();
    document.getElementById("suggestion").style.opacity = "0";
  });
  });

async function getData(){
    const xs = [];
    const ys = [];
    const pieDataNonRenew = [];
    const pieDataRenew = [];

    const regionName = state_name;
    const regionData = aus_data.filter(entry => entry.region === regionName);

    const financialYears = regionData.map(entry => entry["financial year"]);
    xs.push(...financialYears);

    const electricityUsage = regionData.map(entry => entry["electricity_usage"]);
    ys.push(...electricityUsage);

    const nonRenewElectricityGenerated = regionData.map(entry => entry["non_renewable_source_electricity_generated"]);
    pieDataNonRenew.push(...nonRenewElectricityGenerated);

    const renewElectricityGenerated = regionData.map(entry => entry["renewable_source_electricity_generated"]);
    pieDataRenew.push(...renewElectricityGenerated);

    return {xs, ys, pieDataNonRenew, pieDataRenew};
}

const ctx = document.getElementById('chart1');

const myChart = new Chart(ctx, {
type: 'line',
data: {
    labels: [],
    datasets: [{
    label: 'Electricity Consumption',
    data: [],
    fill: false,
    bordercolor: 'rgb(24, 38, 40)',
    tension: 0.1
    }]
},
options: {
    scales: {
    y: {
        beginAtZero: false,
        ticks: {
          callback: function(value, index, values) {
            return value + ' MWh';
          }
        }
    }
    }
}
});

const ctx2 = document.getElementById('chart2');

const myChart2 = new Chart(ctx2, {
type: 'doughnut',
data :{
  labels: [
    'Non-renewable sources',
    'Renewable sources'
  ],
  datasets: [{
    label: '',
    data: [],
    backgroundColor: [
      'rgb(165, 42, 42)',
      'rgb(0, 128, 0)'
    ],
    hoverOffset: 4
  }]
}
});

// let data = {
//   labels: [],
//     datasets: [{
//     label: state_name,
//     data: [],
//     borderWidth: 1
//     }]
// };

// let config = {
//   type: 'bar',
//   data,
//   options: {
//       scales: {
//       y: {
//           beginAtZero: true
//       }
//       }
//   }
// };

// const myChart= new Chart(
//   document.getElementById('chart1'),
//   config
// );

async function updateChart(){
  const ausData = await getData();
  myChart.config.data.datasets[0].data = ausData.ys;
  myChart.config.data.labels = ausData.xs;
  myChart.update();

  let nonRenew = ausData.pieDataNonRenew;
  let renew = ausData.pieDataRenew;

  myChart2.config.data.datasets[0].data = [nonRenew[nonRenew.length - 1], renew[renew.length - 1]];
  myChart2.update();
}
