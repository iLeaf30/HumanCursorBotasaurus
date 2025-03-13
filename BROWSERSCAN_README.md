# BrowserScan Bot Detection Tests

This directory contains scripts to test the HumanCursor-Botasaurus library against BrowserScan's bot detection mechanisms.

## Overview

[BrowserScan](https://www.browserscan.net/bot-detection) is a website that tests various aspects of browser behavior to detect if the visitor is a bot or a human. These scripts demonstrate how our HumanCursor-Botasaurus library can help automate web interactions while mimicking human-like mouse movements and behaviors to avoid detection.

## Scripts

### 1. Basic Test (`browserscan_test.py`)

This script performs basic human-like interactions with the BrowserScan website:
- Navigates to the BrowserScan bot detection page
- Moves the mouse in human-like curves to different elements
- Hovers over headings and links
- Performs natural scrolling
- Takes a screenshot of the results

```bash
python browserscan_test.py
```

### 2. Advanced Test (`browserscan_advanced_test.py`)

This script performs more sophisticated interactions specifically targeting the bot detection tests:
- Performs complex mouse movements with natural acceleration and deceleration
- Simulates human-like scrolling behavior
- Interacts with buttons and form elements
- Simulates text selection by dragging
- Types text with variable timing between keystrokes
- Takes a screenshot of the results

```bash
python browserscan_advanced_test.py
```

## How It Works

These scripts use the HumanCursor-Botasaurus library to:

1. **Generate Human-Like Mouse Movements**: Uses Bezier curves to create natural, non-linear mouse paths
2. **Randomize Timing**: Adds random delays between actions to mimic human unpredictability
3. **Natural Interactions**: Performs scrolling, clicking, and typing in ways that resemble human behavior
4. **Avoid Detection Patterns**: Varies movement speeds and patterns to avoid consistent behaviors that might trigger bot detection

## Results

After running either script, a screenshot will be saved showing the results of the bot detection tests. You can analyze these results to see how well the HumanCursor-Botasaurus library performs against modern bot detection mechanisms.

## Requirements

- Python 3.6+
- Botasaurus Driver
- HumanCursor-Botasaurus library
- numpy
- pytweening

## Notes

- These scripts are for educational and testing purposes only
- The effectiveness may vary as bot detection technologies evolve
- Some websites may use additional detection methods beyond mouse movement analysis 