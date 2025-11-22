#!/bin/bash

# Week 1 Scattershot Analysis
# Processes 50 random conversations to discover themes

# Check if API key is provided
if [ -z "$1" ]; then
    echo "Usage: ./run_week1.sh YOUR_ANTHROPIC_API_KEY"
    echo ""
    echo "This will process 50 random conversations in scattershot mode"
    echo "Estimated cost: ~$25"
    echo "Estimated time: ~15-20 minutes"
    exit 1
fi

API_KEY="$1"

echo "================================================================================"
echo "WEEK 1: SCATTERSHOT THEME DISCOVERY"
echo "================================================================================"
echo "Mode: 100% random sampling across all 3,517 conversations"
echo "Goal: Discover recurring themes, projects, people, patterns"
echo "Batch: 50 conversations"
echo "Cost: ~$25"
echo "================================================================================"
echo ""

# Run batch processor
python3 batch_processor.py "$API_KEY" 1 50 scattershot

echo ""
echo "================================================================================"
echo "WEEK 1 COMPLETE!"
echo "================================================================================"
echo ""
echo "Next steps:"
echo "1. Review: cat analysis_batches/batch_001/REPORT.md"
echo "2. Check themes: cat analysis_batches/tag_aliases.json"
echo "3. See book material: cat analysis_batches/batch_001/results.json | jq '.book_material'"
echo ""
