#!/usr/bin/env python3
"""
Deep Thematic Analysis - Multi-dimensional conversation clustering
Analyzes conversations across multiple dimensions to find coherent patterns
"""

import json
import os
from collections import defaultdict, Counter
from pathlib import Path
import re


# Multi-dimensional theme framework
THEMATIC_DIMENSIONS = {
    "Work Domains": {
        "Bloom/Social Enterprise": [
            r"\bbloom",
            r"\bsocial enterprise",
            r"\bentrepreneurship training",
            r"\baccelerator",
            r"\bimpact",
            r"\bfellows?",
            r"\bcohort",
        ],
        "Technology Projects": [
            r"\bflybrary",
            r"\bpetrichor",
            r"\baiwayway",
            r"\bgemsi",
            r"\brobotics",
            r"\bfab lab",
        ],
        "Solar/Energy Work": [r"\bsolar", r"\benergy", r"\bpv", r"\bphotovoltaic", r"\brenewable"],
        "Education/Training": [
            r"\bcurriculum",
            r"\bworkshop",
            r"\btraining",
            r"\blearning journey",
            r"\bfacilitator",
        ],
    },
    "Activity Types": {
        "Problem Solving": [r"\berror", r"\btroubleshooting", r"\bfixing", r"\bdebug", r"\bissue", r"\bproblem"],
        "Creation/Building": [r"\bbuilding", r"\bcreating", r"\bdeveloping", r"\bdesign", r"\bprototype"],
        "Analysis/Review": [r"\banalysis", r"\breview", r"\bassessment", r"\bevaluation", r"\bfeedback"],
        "Strategy/Planning": [r"\bstrategy", r"\bplanning", r"\broadmap", r"\bframework", r"\bmodel"],
        "Documentation": [r"\bdocument", r"\bguide", r"\breport", r"\bproposal", r"\bgrant"],
        "Reflection": [r"\breflection", r"\binsight", r"\blearning", r"\bgrowth"],
    },
    "Technical Stack": {
        "Web Development": [r"\breact", r"\bnode", r"\bjavascript", r"\btypescript", r"\bhtml", r"\bcss"],
        "Backend/Infrastructure": [r"\bpython", r"\bdocker", r"\bapi", r"\bdatabase", r"\bserver"],
        "Data/Viz": [r"\bd3\.js", r"\bdata", r"\bvisualization", r"\bchart", r"\bgraph"],
        "AI/ML Tools": [r"\bgpt", r"\bclaude", r"\bai", r"\bprompt", r"\bllm"],
        "Hardware": [r"\barduino", r"\biot", r"\bsensor", r"\b3d print"],
    },
    "Personal/Professional": {
        "Career Development": [r"\bvisa", r"\bresume", r"\bcv", r"\bjob", r"\bcareer", r"\bportfolio"],
        "Personal Growth": [
            r"\bwellbeing",
            r"\bstrength",
            r"\bcharacter",
            r"\bhabit",
            r"\bmindfulness",
            r"\bemotional intelligence",
        ],
        "Spiritual Practice": [r"\bprayer", r"\bthikr", r"\bismael", r"\bquran", r"\bramadan", r"\bislam"],
        "Health/Lifestyle": [r"\bhealth", r"\bfitness", r"\bnutrition", r"\bsleep"],
    },
    "Geographic/Cultural": {
        "Lebanon Context": [r"\blebanon", r"\bbeirut", r"\blebanese"],
        "MENA Region": [r"\bmena", r"\biraq", r"\begypt", r"\barab", r"\bmiddle east"],
        "UK/Immigration": [r"\buk", r"\bbritain", r"\bvisa", r"\bimmigration"],
    },
    "Communication Medium": {
        "Writing": [r"\bwriting", r"\barticle", r"\bblog", r"\bessay", r"\bpaper"],
        "Translation": [r"\btranslat", r"\barabic", r"\benglish", r"\blanguage"],
        "Visual": [r"\bmidjourney", r"\bimage", r"\billustration", r"\bdesign", r"\bart"],
        "Presentation": [r"\bslides", r"\bpresentation", r"\bpitch"],
    },
}


def deep_categorize(metadata_list):
    """Categorize conversations across multiple dimensions"""
    multi_dim_matches = defaultdict(lambda: defaultdict(list))

    for meta in metadata_list:
        title_lower = meta["title"].lower()

        # Check each dimension
        for dimension, categories in THEMATIC_DIMENSIONS.items():
            matched = False
            for category, patterns in categories.items():
                for pattern in patterns:
                    if re.search(pattern, title_lower):
                        multi_dim_matches[dimension][category].append(meta)
                        matched = True
                        break
                if matched:
                    break

    return multi_dim_matches


def find_cross_dimensional_patterns(metadata_list):
    """Find conversations that span multiple dimensions"""
    conversation_dimensions = {}

    for meta in metadata_list:
        title_lower = meta["title"].lower()
        dims = defaultdict(set)

        for dimension, categories in THEMATIC_DIMENSIONS.items():
            for category, patterns in categories.items():
                for pattern in patterns:
                    if re.search(pattern, title_lower):
                        dims[dimension].add(category)

        if dims:
            conversation_dimensions[meta["filename"]] = {
                "title": meta["title"],
                "date": meta["date"],
                "dimensions": dict(dims),
                "dimension_count": len(dims),
            }

    # Find most multi-dimensional conversations
    multi_dim = sorted(
        [(k, v) for k, v in conversation_dimensions.items()], key=lambda x: x[1]["dimension_count"], reverse=True
    )

    return multi_dim


def identify_conversation_arcs(metadata_list):
    """Identify thematic arcs over time"""
    by_month = defaultdict(lambda: defaultdict(int))

    for meta in metadata_list:
        month = meta["date"][:7]  # YYYY-MM
        title_lower = meta["title"].lower()

        # Count themes per month
        for dimension, categories in THEMATIC_DIMENSIONS.items():
            for category, patterns in categories.items():
                for pattern in patterns:
                    if re.search(pattern, title_lower):
                        by_month[month][f"{dimension}::{category}"] += 1
                        break

    return dict(by_month)


def find_unique_patterns(metadata_list):
    """Find unique or unusual conversation patterns"""
    unique_concepts = Counter()

    for meta in metadata_list:
        title = meta["title"].lower()
        # Extract unique combinations of words
        words = re.findall(r"\b\w+\b", title)
        # Look for interesting 2-3 word phrases
        for i in range(len(words) - 1):
            phrase = " ".join(words[i : i + 2])
            if len(phrase) > 10:  # Filter out very short phrases
                unique_concepts[phrase] += 1

    # Find rare but interesting concepts (appear 2-5 times - not too common, not singleton)
    interesting = [(k, v) for k, v in unique_concepts.items() if 2 <= v <= 5]
    return sorted(interesting, key=lambda x: x[1], reverse=True)[:50]


def main():
    # Load previous analysis
    with open("/home/user/chatgpt-exporter/theme_analysis.json", "r") as f:
        previous_analysis = json.load(f)

    export_dir = Path("/home/user/chatgpt-exporter/exported_conversations")
    print("🔬 Deep Thematic Analysis - Multi-dimensional Clustering\n")
    print("=" * 80)

    # Re-extract metadata
    all_metadata = []
    for filepath in export_dir.glob("*.json"):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            filename = os.path.basename(filepath)
            parts = filename.split("_")
            date_str = parts[0]
            source = parts[1]
            title = data.get("title", " ".join(parts[2:-1]))
            all_metadata.append({"filename": filename, "date": date_str, "source": source, "title": title})
        except:
            pass

    print(f"Analyzing {len(all_metadata)} conversations...\n")

    # Deep categorization
    print("📊 MULTI-DIMENSIONAL ANALYSIS")
    print("=" * 80)
    multi_dim = deep_categorize(all_metadata)

    for dimension, categories in multi_dim.items():
        if categories:
            print(f"\n{dimension}:")
            sorted_cats = sorted(categories.items(), key=lambda x: len(x[1]), reverse=True)
            for category, convos in sorted_cats:
                count = len(convos)
                bar = "█" * min(30, count // 10)
                print(f"   {category:30s}: {count:4d} {bar}")

    # Cross-dimensional patterns
    print("\n\n🌐 CROSS-DIMENSIONAL CONVERSATIONS")
    print("=" * 80)
    print("Most complex conversations (spanning multiple dimensions):\n")
    cross_patterns = find_cross_dimensional_patterns(all_metadata)

    for filename, info in cross_patterns[:20]:
        print(f"\n📌 {info['title']}")
        print(f"   Date: {info['date']} | Dimensions: {info['dimension_count']}")
        for dim, cats in info["dimensions"].items():
            print(f"      • {dim}: {', '.join(cats)}")

    # Temporal arcs
    print("\n\n📈 THEMATIC EVOLUTION OVER TIME")
    print("=" * 80)
    arcs = identify_conversation_arcs(all_metadata)

    # Find themes that show growth
    theme_counts = defaultdict(list)
    for month, themes in sorted(arcs.items()):
        for theme, count in themes.items():
            theme_counts[theme].append((month, count))

    # Show top evolving themes
    print("\nTop themes with significant activity:\n")
    for theme, timeline in sorted(theme_counts.items(), key=lambda x: sum(c for _, c in x[1]), reverse=True)[:15]:
        total = sum(c for _, c in timeline)
        print(f"   {theme:50s}: {total:4d} conversations")
        recent_3 = timeline[-3:] if len(timeline) >= 3 else timeline
        print(f"      Recent: {', '.join(f'{m}({c})' for m, c in recent_3)}")

    # Unique patterns
    print("\n\n🔍 INTERESTING PHRASE PATTERNS")
    print("=" * 80)
    print("Recurring unique concepts (2-5 occurrences):\n")
    unique = find_unique_patterns(all_metadata)
    for phrase, count in unique[:30]:
        print(f"   {phrase:40s}: {count}")

    # Save comprehensive analysis
    output = {
        "multi_dimensional_analysis": {dim: {cat: len(convos) for cat, convos in cats.items()} for dim, cats in multi_dim.items()},
        "cross_dimensional_conversations": [
            {"title": info["title"], "date": info["date"], "dimensions": {k: list(v) for k, v in info["dimensions"].items()}, "dimension_count": info["dimension_count"]}
            for _, info in cross_patterns[:100]
        ],
        "temporal_arcs": {
            month: {theme: count for theme, count in themes.items()} for month, themes in sorted(arcs.items())
        },
        "unique_patterns": [{"phrase": p, "count": c} for p, c in unique],
    }

    output_file = "/home/user/chatgpt-exporter/deep_theme_analysis.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n\n💾 Deep analysis saved to: {output_file}")
    print("=" * 80)


if __name__ == "__main__":
    main()
