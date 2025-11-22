#!/usr/bin/env python3
"""
Random Conversation Sampler with Stratification

Creates a stratified random sample of conversations based on:
- Time period (2023, 2024, 2025)
- Conversation depth (short, medium, long)
- Source (ChatGPT, Claude, Gemini)

Usage:
    python3 random_sampler.py --size 200 --output selected_conversations_random_200.json
    python3 random_sampler.py --size 50 --output quick_sample.json
"""

import json
import random
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import List, Dict, Any

# Sampling plan for 200 conversations (proportional stratification)
SAMPLING_PLAN_200 = {
    ('2023', 'short', 'chatgpt'): 6,
    ('2023', 'short', 'claude'): 4,
    ('2023', 'medium', 'chatgpt'): 10,
    ('2023', 'medium', 'claude'): 5,
    ('2023', 'long', 'chatgpt'): 10,
    ('2023', 'long', 'claude'): 5,
    ('2024', 'short', 'chatgpt'): 10,
    ('2024', 'short', 'claude'): 5,
    ('2024', 'medium', 'chatgpt'): 16,
    ('2024', 'medium', 'claude'): 9,
    ('2024', 'long', 'chatgpt'): 16,
    ('2024', 'long', 'claude'): 9,
    ('2025', 'short', 'chatgpt'): 13,
    ('2025', 'short', 'claude'): 7,
    ('2025', 'medium', 'chatgpt'): 22,
    ('2025', 'medium', 'claude'): 13,
    ('2025', 'long', 'chatgpt'): 26,
    ('2025', 'long', 'claude'): 14,
}

# Sampling plan for 50 conversations (quick validation)
SAMPLING_PLAN_50 = {
    ('2023', 'short', 'chatgpt'): 2,
    ('2023', 'short', 'claude'): 1,
    ('2023', 'medium', 'chatgpt'): 3,
    ('2023', 'medium', 'claude'): 2,
    ('2023', 'long', 'chatgpt'): 3,
    ('2023', 'long', 'claude'): 2,
    ('2024', 'short', 'chatgpt'): 3,
    ('2024', 'short', 'claude'): 2,
    ('2024', 'medium', 'chatgpt'): 4,
    ('2024', 'medium', 'claude'): 2,
    ('2024', 'long', 'chatgpt'): 4,
    ('2024', 'long', 'claude'): 2,
    ('2025', 'short', 'chatgpt'): 3,
    ('2025', 'short', 'claude'): 2,
    ('2025', 'medium', 'chatgpt'): 6,
    ('2025', 'medium', 'claude'): 3,
    ('2025', 'long', 'chatgpt'): 7,
    ('2025', 'long', 'claude'): 4,
}


def load_conversations(exported_dir: Path) -> List[Dict[str, Any]]:
    """Load all conversations from exported_conversations directory."""
    conversations = []

    for json_file in exported_dir.glob("*.json"):
        # Skip metadata files
        if "_metadata.md" in json_file.name:
            continue

        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                conv = json.load(f)
                conversations.append({
                    'filename': json_file.name,
                    'filepath': str(json_file),
                    'data': conv
                })
        except Exception as e:
            print(f"Warning: Could not load {json_file.name}: {e}")

    return conversations


def extract_metadata(conv: Dict[str, Any]) -> Dict[str, Any]:
    """Extract metadata from conversation."""
    data = conv['data']
    filename = conv['filename']

    # Extract basic info - handles both old and new export formats
    title = data.get('title', 'Untitled')

    # Try new format first (messages array)
    if 'messages' in data and isinstance(data['messages'], list):
        message_count = data.get('message_count', len(data['messages']))
        source = data.get('source', 'unknown')

        # Get date from created_at or filename
        created_at = data.get('created_at', '')
        if created_at:
            try:
                year = int(created_at.split('-')[0])
            except:
                year = None
        else:
            try:
                date_str = filename.split('_')[0]
                year = int(date_str.split('-')[0])
            except:
                year = None

        create_time = data.get('updated_at', created_at)

    # Fall back to old format (mapping)
    else:
        create_time = data.get('create_time', 0)
        mapping = data.get('mapping', {})
        messages = [m for m in mapping.values() if m.get('message')]
        message_count = len(messages)

        # Determine source from filename
        if 'chatgpt' in filename.lower():
            source = 'chatgpt'
        elif 'claude' in filename.lower():
            source = 'claude'
        elif 'gemini' in filename.lower():
            source = 'gemini'
        else:
            source = 'unknown'

        # Extract date from filename or create_time
        try:
            date_str = filename.split('_')[0]
            year = int(date_str.split('-')[0])
        except:
            if create_time:
                dt = datetime.fromtimestamp(create_time)
                year = dt.year
            else:
                year = None

    # Determine depth tier
    if message_count <= 14:
        depth = 'short'
    elif message_count <= 100:
        depth = 'medium'
    else:
        depth = 'long'

    return {
        'filename': filename,
        'filepath': conv['filepath'],
        'title': title,
        'year': year,
        'message_count': message_count,
        'source': source,
        'depth': depth,
        'create_time': create_time
    }


def stratify_conversations(conversations: List[Dict[str, Any]]) -> Dict[tuple, List[Dict[str, Any]]]:
    """Stratify conversations by year, depth, and source."""
    strata = defaultdict(list)

    for conv in conversations:
        meta = extract_metadata(conv)

        # Create stratum key
        year = str(meta['year']) if meta['year'] else 'unknown'
        depth = meta['depth']
        source = meta['source']

        stratum_key = (year, depth, source)
        strata[stratum_key].append(meta)

    return strata


def sample_conversations(strata: Dict[tuple, List[Dict[str, Any]]],
                        sampling_plan: Dict[tuple, int],
                        seed: int = None) -> List[Dict[str, Any]]:
    """Sample conversations according to stratification plan."""
    if seed is not None:
        random.seed(seed)

    sample = []
    stats = {
        'requested': {},
        'available': {},
        'sampled': {}
    }

    for stratum_key, target_count in sampling_plan.items():
        year, depth, source = stratum_key
        stratum_conversations = strata.get(stratum_key, [])
        available_count = len(stratum_conversations)

        stats['requested'][stratum_key] = target_count
        stats['available'][stratum_key] = available_count

        if available_count == 0:
            print(f"Warning: No conversations in stratum {stratum_key}")
            stats['sampled'][stratum_key] = 0
            continue

        if available_count < target_count:
            print(f"Warning: Only {available_count} available in stratum {stratum_key}, requested {target_count}")
            sampled = stratum_conversations  # Take all available
            stats['sampled'][stratum_key] = available_count
        else:
            sampled = random.sample(stratum_conversations, target_count)
            stats['sampled'][stratum_key] = target_count

        sample.extend(sampled)

    return sample, stats


def print_statistics(stats: Dict[str, Dict], total_conversations: int):
    """Print sampling statistics."""
    print("\n" + "="*80)
    print("SAMPLING STATISTICS")
    print("="*80)

    print(f"\nTotal conversations available: {total_conversations}")
    print(f"Total sampled: {sum(stats['sampled'].values())}")
    print(f"Coverage: {sum(stats['sampled'].values()) / total_conversations * 100:.1f}%")

    print("\nBreakdown by stratum:")
    print(f"{'Year':<6} {'Depth':<8} {'Source':<10} {'Requested':<12} {'Available':<12} {'Sampled':<10}")
    print("-" * 80)

    for stratum_key in sorted(stats['requested'].keys()):
        year, depth, source = stratum_key
        requested = stats['requested'][stratum_key]
        available = stats['available'][stratum_key]
        sampled = stats['sampled'][stratum_key]
        print(f"{year:<6} {depth:<8} {source:<10} {requested:<12} {available:<12} {sampled:<10}")

    print("\nSummary by year:")
    year_summary = defaultdict(int)
    for stratum_key, count in stats['sampled'].items():
        year_summary[stratum_key[0]] += count
    for year in sorted(year_summary.keys()):
        print(f"  {year}: {year_summary[year]} conversations")

    print("\nSummary by depth:")
    depth_summary = defaultdict(int)
    for stratum_key, count in stats['sampled'].items():
        depth_summary[stratum_key[1]] += count
    for depth in ['short', 'medium', 'long']:
        print(f"  {depth}: {depth_summary[depth]} conversations")

    print("\nSummary by source:")
    source_summary = defaultdict(int)
    for stratum_key, count in stats['sampled'].items():
        source_summary[stratum_key[2]] += count
    for source in sorted(source_summary.keys()):
        print(f"  {source}: {source_summary[source]} conversations")

    print("="*80 + "\n")


def save_sample(sample: List[Dict[str, Any]], output_path: Path, stats: Dict):
    """Save sampled conversations to JSON file."""
    # Convert tuple keys to strings for JSON serialization
    stats_serializable = {}
    for key, value in stats.items():
        if isinstance(value, dict):
            stats_serializable[key] = {str(k): v for k, v in value.items()}
        else:
            stats_serializable[key] = value

    output_data = {
        'metadata': {
            'sample_size': len(sample),
            'created': datetime.now().isoformat(),
            'method': 'stratified_random_sampling',
            'statistics': stats_serializable
        },
        'conversations': sample
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"Sample saved to: {output_path}")
    print(f"Total conversations in sample: {len(sample)}")


def main():
    parser = argparse.ArgumentParser(description='Random conversation sampler with stratification')
    parser.add_argument('--size', type=int, default=200,
                       help='Sample size (50, 200, 500, etc.)')
    parser.add_argument('--output', type=str, default='selected_conversations_random.json',
                       help='Output JSON file path')
    parser.add_argument('--exported-dir', type=str, default='exported_conversations',
                       help='Directory containing exported conversations')
    parser.add_argument('--seed', type=int, default=None,
                       help='Random seed for reproducibility')
    parser.add_argument('--list-only', action='store_true',
                       help='Only list available strata, do not sample')

    args = parser.parse_args()

    # Determine sampling plan
    if args.size == 50:
        sampling_plan = SAMPLING_PLAN_50
    elif args.size == 200:
        sampling_plan = SAMPLING_PLAN_200
    else:
        print(f"Error: No predefined sampling plan for size {args.size}")
        print("Available sizes: 50, 200")
        print("You can modify the script to add more sampling plans.")
        return

    # Load conversations
    exported_dir = Path(args.exported_dir)
    if not exported_dir.exists():
        print(f"Error: Directory not found: {exported_dir}")
        return

    print(f"Loading conversations from {exported_dir}...")
    conversations = load_conversations(exported_dir)
    print(f"Loaded {len(conversations)} conversations")

    # Stratify conversations
    print("Stratifying conversations...")
    strata = stratify_conversations(conversations)

    if args.list_only:
        print("\nAvailable strata:")
        print(f"{'Year':<6} {'Depth':<8} {'Source':<10} {'Count':<10}")
        print("-" * 40)
        for stratum_key in sorted(strata.keys()):
            year, depth, source = stratum_key
            count = len(strata[stratum_key])
            print(f"{year:<6} {depth:<8} {source:<10} {count:<10}")
        return

    # Sample conversations
    print(f"Sampling {args.size} conversations...")
    sample, stats = sample_conversations(strata, sampling_plan, seed=args.seed)

    # Print statistics
    print_statistics(stats, len(conversations))

    # Save sample
    output_path = Path(args.output)
    save_sample(sample, output_path, stats)

    print("\n✅ Sampling complete!")
    print(f"\nNext steps:")
    print(f"1. Review the sample: cat {output_path}")
    print(f"2. Organize conversations: python3 organize_conversations.py --sample {output_path}")
    print(f"3. Extract voice: python3 extract_your_voice.py --sample {output_path}")
    print(f"4. Run LLM analysis: python3 batch_processor.py YOUR_API_KEY --sample {output_path}")


if __name__ == '__main__':
    main()
