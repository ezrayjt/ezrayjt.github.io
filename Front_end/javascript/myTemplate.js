class cssFiles extends HTMLElement {
  connectedCallback() {
    this.innerHTML = `
        <!-- google fonts -->
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
        <link
            href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@10..48,800&family=Lilita+One&family=Quicksand:wght@300;500;600&display=swap"
            rel="stylesheet" />
    
        <!-- use bootstrap for some icons -->
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css">
    
        <!-- css files to stylise the page -->
        <link rel="stylesheet" href="Front_end/CSS/button.css" />
        <link rel="stylesheet" href="Front_end/CSS/map.css" />
        <link rel="stylesheet" href="Front_end/CSS/navbar.css" />
        <link rel="stylesheet" href="Front_end/CSS/section.css" />
        <link rel="stylesheet" href="Front_end/CSS/lights.css" />
        <link rel="stylesheet" href="Front_end/CSS/waste.css" />
        <link rel="stylesheet" href="Front_end/CSS/wasteInfo.css" />
        `;
  }
}

customElements.define("css-files", cssFiles);

class jsFiles extends HTMLElement {
  connectedCallback() {
    for (let source of ["navbar", "map", "chart", "lights"]) {
      let script = document.createElement('script');
      script.src = `Front_end/javascript/${source}.js`;
      document.head.appendChild(script);
    }
  }
}

customElements.define("js-files", jsFiles);

class navbar extends HTMLElement {
  connectedCallback() {
    this.innerHTML = `
        <header>
        <a href="index.html" class="logo"><img src="Front_end/images/Logo1.png"></a>

        <nav>
          <a href="home.html">Home</a>

          <div class="dropdown-container">
              <a href="lights.html" class="dropdown1">Lights</a>
              <div class="sub">
                  <a href="lights.html">Assess Room's Lighting</a>
                  <a href="lightbulb.html">Lightbulb Types</a>
              </div>
          </div>

          <a href="appliances.html">Appliances</a>
          
          <a href="waste.html">Waste</a>
          
          <a href="DIY.html">DIY</a>
      </nav>
    </header>
        `;
  }
}

customElements.define("nav-bar", navbar);

class dropdown extends HTMLElement {
  connectedCallback() {
    this.innerHTML = `
        <header>
        <a href="index.html" class="logo"><img src="Front_end/images/logo.png"></a>

        <nav>
        <a href="index.html#home">Home</a>
        <a href="index.html#article">Issues</a>
        <a href="index.html#interactive-map">Electricity Usage</a>
        <a href="lights.html">Assess Room's Lighting</a>
        <a href="lightbulb.html">Lightbulb Types</a>
        <a href="waste.html">Waste</a>
        </nav>

    </header>
        `;
  }
}

customElements.define("drop-down", dropdown);
