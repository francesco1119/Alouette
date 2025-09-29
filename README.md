# Alouette
Alouette is a simple Python script that allows you to scrap all images from a website stored on the Wayback Machine.

## Prerequisites

- Python 3.x
- Ruby and RubyGems
- `wayback_machine_downloader_straw` gem

## Installation

1. **Install the wayback_machine_downloader_straw gem:**
   ```bash
   gem install wayback_machine_downloader_straw
   ```

2. **Clone this repository:**
   ```bash
   git clone https://github.com/francesco1119/Alouette.git
   cd Alouette
   ```

## Usage

Run the script with a domain name:

```bash
python Alouette.py <domain>
```

**Example:**
```bash
python Alouette.py jeeja.biz
```

## How It Works

1. The script checks if the required `wayback_machine_downloader_straw` gem is installed
2. Generates a JSON file containing all archived image URLs from the Wayback Machine for the specified domain
3. Downloads all images to a folder named after the domain
4. Skips already downloaded images on subsequent runs
5. Implements retry logic for failed downloads with automatic delays
