#!/usr/bin/env python3
"""
Comprehensive Theme Analysis for Exported Conversations
Analyzes 3,517 ChatGPT/Claude conversations to identify patterns and themes
"""

import json
import os
from collections import defaultdict, Counter
from datetime import datetime
import re
from pathlib import Path

# Theme categories with keyword patterns
THEME_CATEGORIES = {
    "Entrepreneurship & Business": [
        r"\bentrepreneur",
        r"\bbusiness",
        r"\bstartup",
        r"\bcompany",
        r"\bventure",
        r"\bbloom",
        r"\bgemsi",
        r"\bsocial enterprise",
        r"\borganization",
        r"\bfounder",
    ],
    "Technology & Development": [
        r"\bcode",
        r"\bprogramming",
        r"\bpython",
        r"\bjavascript",
        r"\bapi",
        r"\bdocker",
        r"\breact",
        r"\bnode",
        r"\bdebug",
        r"\berror",
        r"\bgit",
        r"\bdatabase",
    ],
    "Personal Development & Psychology": [
        r"\bwellbeing",
        r"\bwell-being",
        r"\bpermah",
        r"\bstrength",
        r"\bemotional",
        r"\bpsychology",
        r"\bmindfulness",
        r"\bcharacter",
        r"\bhabit",
        r"\bgrowth",
    ],
    "Education & Learning": [
        r"\bteaching",
        r"\blearning",
        r"\beducation",
        r"\btraining",
        r"\bworkshop",
        r"\bcurriculum",
        r"\bstudent",
        r"\bmentor",
        r"\baccelerator",
        r"\bcourse",
    ],
    "AI & Machine Learning": [
        r"\bai",
        r"\bartificial intelligence",
        r"\bmachine learning",
        r"\bgpt",
        r"\bclaude",
        r"\bprompt",
        r"\bllm",
        r"\bmodel",
        r"\bchatgpt",
    ],
    "Making & Hardware": [
        r"\b3d print",
        r"\barduino",
        r"\brobot",
        r"\bmaker",
        r"\bfab lab",
        r"\bhardware",
        r"\biot",
        r"\belectronics",
        r"\bprototype",
    ],
    "MENA & Lebanon": [
        r"\blebanon",
        r"\bmena",
        r"\biraq",
        r"\barab",
        r"\begypt",
        r"\bbeirut",
        r"\bmiddle east",
    ],
    "Career & Immigration": [
        r"\bvisa",
        r"\bresume",
        r"\bcv",
        r"\bjob",
        r"\bcareer",
        r"\bhiring",
        r"\binterview",
        r"\buk visa",
        r"\bimmigration",
    ],
    "Writing & Content": [
        r"\bwriting",
        r"\bblog",
        r"\barticle",
        r"\bpaper",
        r"\bresearch",
        r"\bgrant",
        r"\bproposal",
        r"\breport",
    ],
    "Creative & Art": [
        r"\bart",
        r"\bdesign",
        r"\bcreative",
        r"\bmidjourney",
        r"\bimage",
        r"\billustration",
        r"\bmusic",
        r"\bdance",
    ],
    "Islamic & Spiritual": [
        r"\bislam",
        r"\bquran",
        r"\bprayer",
        r"\bramadan",
        r"\bfasting",
        r"\ballah",
        r"\bspiritual",
    ],
    "Health & Wellness": [
        r"\bhealth",
        r"\bfitness",
        r"\bnutrition",
        r"\bexercise",
        r"\bdiet",
        r"\bmedical",
        r"\bwellness",
    ],
    "Social Impact": [
        r"\bimpact",
        r"\bngo",
        r"\bnonprofit",
        r"\bdevelopment",
        r"\bcommunity",
        r"\bsocial good",
        r"\bsdg",
    ],
    "Communication & Language": [
        r"\btranslat",
        r"\barabic",
        r"\benglish",
        r"\blanguage",
        r"\bcommunication",
    ],
    "Data & Analysis": [
        r"\bdata",
        r"\banalysis",
        r"\bvisualization",
        r"\bd3\.js",
        r"\bchart",
        r"\bmetric",
        r"\bstatistic",
    ],
    "Food & Cooking": [
        r"\bfood",
        r"\brecipe",
        r"\bcooking",
        r"\bfarm",
        r"\bagri",
    ],
}


def extract_metadata(filepath):
    """Extract basic metadata from conversation JSON"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        filename = os.path.basename(filepath)
        parts = filename.split("_")

        # Parse filename: YYYY-MM-DD_source_title_hash.json
        date_str = parts[0]
        source = parts[1] if len(parts) > 1 else "unknown"
        title = " ".join(parts[2:-1]) if len(parts) > 2 else "untitled"
        title = title.replace("__", ": ").replace("_", " ")

        # Get actual title and dates from JSON if available
        json_title = data.get("title", title)
        created_at = data.get("created_at") or data.get("create_time")
        updated_at = data.get("updated_at") or data.get("update_time")

        # Message count
        message_count = 0
        if "messages" in data:
            message_count = len(data["messages"])
        elif "mapping" in data:
            message_count = len(
                [
                    m
                    for m in data["mapping"].values()
                    if m.get("message") and m["message"].get("author", {}).get("role") in ["user", "assistant"]
                ]
            )

        return {
            "filename": filename,
            "filepath": filepath,
            "date": date_str,
            "source": source,
            "title": json_title,
            "created_at": created_at,
            "updated_at": updated_at,
            "message_count": message_count,
            "file_size": os.path.getsize(filepath),
        }
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return None


def categorize_by_themes(metadata_list):
    """Categorize conversations by themes based on title analysis"""
    theme_matches = defaultdict(list)

    for meta in metadata_list:
        title_lower = meta["title"].lower()
        matched_themes = set()

        for theme, patterns in THEME_CATEGORIES.items():
            for pattern in patterns:
                if re.search(pattern, title_lower):
                    matched_themes.add(theme)
                    break

        if not matched_themes:
            matched_themes.add("Uncategorized")

        for theme in matched_themes:
            theme_matches[theme].append(meta)

    return theme_matches


def analyze_temporal_patterns(metadata_list):
    """Analyze conversation patterns over time"""
    by_year_month = defaultdict(int)
    by_year = defaultdict(int)

    for meta in metadata_list:
        try:
            date_str = meta["date"]
            year = date_str[:4]
            year_month = date_str[:7]
            by_year[year] += 1
            by_year_month[year_month] += 1
        except:
            pass

    return {"by_year": dict(sorted(by_year.items())), "by_month": dict(sorted(by_year_month.items()))}


def extract_all_titles(metadata_list):
    """Get all unique title words for word cloud analysis"""
    all_words = []
    stop_words = {
        "the",
        "a",
        "an",
        "and",
        "or",
        "but",
        "in",
        "on",
        "at",
        "to",
        "for",
        "of",
        "with",
        "by",
        "from",
        "as",
        "is",
        "was",
        "are",
        "be",
        "been",
        "being",
        "new",
        "chat",
    }

    for meta in metadata_list:
        words = re.findall(r"\b\w+\b", meta["title"].lower())
        all_words.extend([w for w in words if w not in stop_words and len(w) > 3])

    return Counter(all_words)


def main():
    export_dir = Path("/home/user/chatgpt-exporter/exported_conversations")
    print(f"🔍 Analyzing conversations in: {export_dir}")

    # Extract all metadata
    print("\n📊 Extracting metadata from all conversations...")
    all_metadata = []
    json_files = list(export_dir.glob("*.json"))
    total = len(json_files)

    for i, filepath in enumerate(json_files, 1):
        if i % 100 == 0:
            print(f"   Progress: {i}/{total} ({i*100//total}%)")
        meta = extract_metadata(filepath)
        if meta:
            all_metadata.append(meta)

    print(f"✓ Processed {len(all_metadata)} conversations\n")

    # Basic statistics
    chatgpt_count = sum(1 for m in all_metadata if m["source"] == "chatgpt")
    claude_count = sum(1 for m in all_metadata if m["source"] == "claude")
    total_messages = sum(m["message_count"] for m in all_metadata)

    print("=" * 80)
    print("CONVERSATION EXPORT SUMMARY")
    print("=" * 80)
    print(f"\n📈 BASIC STATISTICS")
    print(f"   Total conversations: {len(all_metadata):,}")
    print(f"   ChatGPT: {chatgpt_count:,} ({chatgpt_count*100//len(all_metadata)}%)")
    print(f"   Claude: {claude_count:,} ({claude_count*100//len(all_metadata)}%)")
    print(f"   Total messages: {total_messages:,}")
    print(f"   Average messages per conversation: {total_messages // len(all_metadata)}")

    # Temporal analysis
    print(f"\n📅 TEMPORAL PATTERNS")
    temporal = analyze_temporal_patterns(all_metadata)
    print(f"   Date range: {min(temporal['by_year'].keys())} - {max(temporal['by_year'].keys())}")
    print(f"\n   Conversations by year:")
    for year, count in temporal["by_year"].items():
        bar = "█" * (count // 50)
        print(f"      {year}: {count:4d} {bar}")

    # Theme categorization
    print(f"\n🎯 THEMATIC ANALYSIS")
    theme_matches = categorize_by_themes(all_metadata)
    print(f"   Conversations by theme (conversations may appear in multiple themes):")
    for theme, convos in sorted(theme_matches.items(), key=lambda x: len(x[1]), reverse=True):
        count = len(convos)
        bar = "█" * min(50, count // 20)
        print(f"      {theme:40s}: {count:4d} {bar}")

    # Top keywords
    print(f"\n🔑 TOP KEYWORDS IN TITLES (30 most common)")
    word_freq = extract_all_titles(all_metadata)
    for word, count in word_freq.most_common(30):
        print(f"      {word:20s}: {count:4d}")

    # Save detailed analysis
    output_file = "/home/user/chatgpt-exporter/theme_analysis.json"
    analysis_output = {
        "summary": {
            "total_conversations": len(all_metadata),
            "chatgpt_count": chatgpt_count,
            "claude_count": claude_count,
            "total_messages": total_messages,
            "date_range": {
                "earliest": min(m["date"] for m in all_metadata),
                "latest": max(m["date"] for m in all_metadata),
            },
        },
        "temporal_patterns": temporal,
        "themes": {theme: len(convos) for theme, convos in theme_matches.items()},
        "top_keywords": dict(word_freq.most_common(100)),
        "conversations_by_theme": {
            theme: [{"title": c["title"], "date": c["date"], "source": c["source"]} for c in convos[:20]]
            for theme, convos in theme_matches.items()
        },
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(analysis_output, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Detailed analysis saved to: {output_file}")
    print("=" * 80)


if __name__ == "__main__":
    main()
