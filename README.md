<div id="top"></div>


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">Urban Traffic Control</h3>

  <p align="center">
    Bachelor thesis project: connecting automated planning with SUMO simulator
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

<!-- Img: [![Product Name Screen Shot][product-screenshot]](https://example.com) -->

Project description.

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

* [gcc]()
* [g++]()
* [python3.9]()
* [Cmake]() (for planner installation)
* [Make]() (for planner installation)

Python libraries: (version can be found in requirements.txt file)
* [pip](https://pypi.org/project/pip/)
* [wheel](https://pypi.org/project/wheel/)
* [setuptools](https://pypi.org/project/setuptools/)
* [numpy](https://numpy.org/)
* [matplotlib](https://matplotlib.org/)
* [prompt_toolkit](https://python-prompt-toolkit.readthedocs.io/en/master/)
* [traci](https://pypi.org/project/traci/)
* [sumolib](https://pypi.org/project/sumolib/)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites


1) [osmfilter.c](https://wiki.openstreetmap.org/wiki/Osmfilter) (located in Project/Converter/OSMfilter) has to be compiled
  ```sh
  gcc osmfilter.c -O3 -o osmfilter
  ```
2) [SUMO](https://www.eclipse.org/sumo/) has to be downloaded
3) [Planners](https://ipc2018-classical.bitbucket.io/#description) 
used in this project: [MERWIN](https://bitbucket.org/ipc2018-classical/team14/src/ipc-2018-seq-agl/), 
[Cerberus](https://bitbucket.org/ipc2018-classical/team15/src/ipc-2018-seq-agl/) (agile)

### Installation

Below is an example of how you can instruct your audience on installing and setting up your app. This template doesn't rely on any external dependencies or services._

1. Clone the repo
   ```sh
   git clone https://github.com/Matyxus/UTC
   ```
2. In project root (.../UTC) execute:
   ```sh
   pip install -e UTC
   ```
3. Install requirements
   ```sh
   pip install -r requirements.txt
   ```
4. Install planners

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Usage description.

1. Downloading maps from [OpenStreetMap](https://www.openstreetmap.org/)
save them in /UTC/Project/Maps/osm/original
2. Convert downloaded maps into '.net.xml' format.
   ```sh
   python converter.py map_name1 map_name2 ...
   ```
   Or run converter.py and enter input dynamically, for command type 'convert',
   fill argument 'file_name' with name of the map (.osm suffix not needed).
   ```sh
   python converter.py
   ```
   ![converter example](Images/converter_input_example.PNG)

<p align="right">(<a href="#top">back to top</a>)</p>










