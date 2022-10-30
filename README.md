<div id="readme-top"></div>

# Team Ez2Type

<div align="center">
  <!-- <a href="https://github.com/KirillTregubov/csc302">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a> -->

  <h2 align="center">Team Ez2Type</h2>
  <p align="center">
    A group project that uses the Spotify Million Playlist Dataset to display interesting and meaningful results.
    <!-- <br />
    <a href="https://github.com/KirillTregubov/csc302"><strong>Explore the docs »</strong></a> -->
    <div>
      <a href="https://github.com/KirillTregubov/csc302/tree/main/docs">Meeting Notes</a>
      ·
      <a href="#top">Documentation</a>
      ·
      <a href="https://github.com/users/KirillTregubov/projects/1">Roadmap</a>
    </div>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
## Table of Contents
- [Assignment 2](#assignment-2)
- [Features](#features)
- [Planned Features](#planned-features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
  - [Linux](#linux)
  - [macOS](#macos)
  - [Windows](#windows)
  - [Troubleshooting](#troubleshooting)
- [Usage](#usage) (build & test)
  - [Linux](#linux-1)
  - [macOS and Windows](#macos--windows-wsl)
  - [Troubleshooting](#troubleshooting-1)
  - [Other Scripts](#other-scripts)
- [License](#license)
- [Maintainers](#maintainers)


<div id="top"></div>

## Assignment 2

All detailed information related to Assignment 2 not covered on this page can be found in [Assignment 2]().

## Features

- **Get recommended tracks**: Get recommended tracks based on an ML model.

## Planned Features

Our [Roadmap](https://github.com/users/KirillTregubov/projects/1/) shows all our tasks labelled by status (complete, in progress, not started), assignee, and milestone.

## Tech Stack

[Tech Stack](https://github.com/KirillTregubov/csc302/blob/main/docs/TechStack.md) contains detailed information about the technologies we are using including Pros, Cons and Alternatives.

### Dataset

The [Spotify Million Playlist Dataset](https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge) and the [Spotify Web API](https://developer.spotify.com/documentation/web-api/).

### Database

[![SQLITE](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/index.html)

### Frontend

[![TypeScript](https://img.shields.io/badge/TypeScript-FaF9F8?logo=typescript&logoColor=3178C6)](https://www.typescriptlang.org/)
[![Vite](https://img.shields.io/badge/Vite-646CFF?logo=vite&logoColor=white)](https://vitejs.dev/)
[![React](https://img.shields.io/badge/React-20232A?logo=react&logoColor=61DAFB)](https://reactjs.org/)

### Backend

[![Python](https://img.shields.io/badge/python-3670A0?logo=python&logoColor=ffdd54)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-%23000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)

### Container

[![Docker](https://img.shields.io/badge/Docker-%230db7ed?logo=docker&logoColor=white)](https://www.docker.com/)

### CI

[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-%232671E5?logo=github-actions&logoColor=white)]()

## A2 Deliverable

Here is the [document](https://github.com/KirillTregubov/csc302/blob/main/docs/A2Deliverable.md) containing a description of what we planned to implement in A2 as well as the progress report on our milestones.

Please consult the links above for our meeting notes, tech stack, and roadmap. Meeting notes for A2 are weeks 5-8. Roadmap and tech stack are the same as from A1.

## Installation

### Linux

Install the development environment by executing the following command in a shell:

```sh
sudo bash run-install.sh
```

### macOS

Install the development environment by executing the following command in a shell:

```sh
bash run-install.sh
```

### Windows

On Windows, install the development environment by executing:

```sh
run-install.bat
```

### Troubleshooting

If the script fails to run on your machine, please [install Docker Desktop](https://docs.docker.com/desktop/) yourself.

## Usage

### Linux

To build our application and run it in development mode, execute the following command:

```sh
sudo bash run-build.sh
```

To run tests for the application, execute:

```sh
sudo bash run-tests.sh
```

### macOS & Windows (WSL)

To build our application and run it in development mode, execute the following command:

```sh
bash run-build.sh
```

To run tests for the application, execute:

```sh
bash run-tests.sh
```

### Troubleshooting

If you run into issues related to permissions for running the scripts, execute the following command replacing `<script>` with the script name:

```sh
sudo chmod 755 ./<script>.sh
```

### Other Scripts

To add a package to the backend, execute the following helper script:

```sh
bash ./backend/install-pkg.sh
```

## License

Distributed under the GNU GPLv3. See [`LICENSE.txt`](https://github.com/KirillTregubov/csc302/blob/main/LICENSE) for more information.

## Maintainers

- [Kirill Tregubov](https://github.com/KirillTregubov)
- [Eddie Shao](https://github.com/EddieShao)
- [Burt Lau](https://github.com/burtlau)
- [Roger Liu](https://github.com/pvtstaticvoid)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
