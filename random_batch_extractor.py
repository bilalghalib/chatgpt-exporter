#!/usr/bin/env python3
"""
Random Batch Conversation Extractor
Randomly selects conversations from the dataset and processes them
"""

import json
import os
import random
from pathlib import Path
from datetime import datetime

# Configuration
EXPORTED_CONVERSATIONS_DIR = './exported_conversations'
CONVERSATIONS_DIR = './conversations'
BATCH_SIZE = 10  # Number of random conversations to extract

def load_analyzed_conversations():
    """Load list of already analyzed conversations"""
    analyzed = set()

    # Check conversations directory for existing metadata
    conv_dir = Path(CONVERSATIONS_DIR)
    if conv_dir.exists():
        for item in conv_dir.iterdir():
            if item.is_dir():
                analyzed.add(item.name)

    return analyzed

def load_all_conversations():
    """Load all available conversation files"""
    export_dir = Path(EXPORTED_CONVERSATIONS_DIR)
    conversations = []

    for json_file in export_dir.glob('*.json'):
        # Skip metadata files
        if '_metadata' in json_file.name:
            continue

        # Extract conversation ID from filename
        conv_id = json_file.stem
        conversations.append({
            'id': conv_id,
            'filename': json_file.name,
            'path': str(json_file)
        })

    return conversations

def select_random_batch(conversations, analyzed, batch_size=10):
    """Select random conversations that haven't been analyzed yet"""
    # Filter out already analyzed
    unanalyzed = [c for c in conversations if c['id'] not in analyzed]

    print(f"📊 Total conversations: {len(conversations)}")
    print(f"✅ Already analyzed: {len(analyzed)}")
    print(f"⏳ Unanalyzed: {len(unanalyzed)}")

    # Randomly select
    if len(unanalyzed) < batch_size:
        batch_size = len(unanalyzed)
        print(f"⚠️  Only {batch_size} unanalyzed conversations available")

    selected = random.sample(unanalyzed, batch_size)

    return selected

def main():
    print("🎲 Random Batch Conversation Extractor")
    print("=" * 60)

    # Load analyzed conversations
    analyzed = load_analyzed_conversations()

    # Load all conversations
    conversations = load_all_conversations()

    # Select random batch
    selected = select_random_batch(conversations, analyzed, BATCH_SIZE)

    print(f"\n🎯 Selected {len(selected)} random conversations:")
    print("=" * 60)

    for i, conv in enumerate(selected, 1):
        print(f"{i}. {conv['filename']}")

    # Save selection to file
    selection_file = f"random_batch_selection_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(selection_file, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'batch_size': len(selected),
            'total_conversations': len(conversations),
            'already_analyzed': len(analyzed),
            'selected_conversations': selected
        }, f, indent=2)

    print(f"\n💾 Selection saved to: {selection_file}")

    # Create file list for batch processor
    file_list = 'random_batch_files.txt'
    with open(file_list, 'w') as f:
        for conv in selected:
            f.write(f"{conv['path']}\n")

    print(f"📝 File list saved to: {file_list}")
    print(f"\nNext step: Run batch processor on these files")

if __name__ == '__main__':
    main()
