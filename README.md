# Apple Music Library Manager

A companion application for **AMDL (Apple Music Downloader)** that helps manage failed downloads, retry songs, and analyze your Apple Music library.

---

## Features

- Retry One Failed Song
- Retry All Failed Songs
- Retry by Artist
- Retry by Failure Reason
- Failed Song Statistics
- Search Failed Songs
- Rich Terminal Interface
- Progress Bar for Bulk Retry

---

## Requirements

- Python 3.13+
- AMDL
- FFmpeg
- Docker (for Wrapper Mode)

---

## Installation

Clone the repository:

```bash
git clone https://github.com/bharath2151/AppleMusicLibraryManager.git
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Configuration

Copy:

```
config.example.json
```

to

```
config.json
```

Then edit the paths according to your system.

---

## Current Modules

- Retry Manager
- Statistics
- Search
- Configuration Manager

---

## Planned Features

- System Health
- Settings Manager
- Library Scanner
- Export Reports
- Download Manager Integration
- Automatic Update Checker

---

## License

This project is licensed under the MIT License.
