#!/usr/bin/env python3
"""
Extract Your Voice - Pull substantive content from YOUR messages
Organize by theme and present as digestible blocks of your own thinking
"""

import json
import os
from pathlib import Path
from collections import defaultdict
import re
from datetime import datetime


class VoiceExtractor:
    """Extract and organize substantive content from user messages"""

    def __init__(self):
        self.your_thoughts = defaultdict(list)
        self.all_messages = []

    def is_substantive(self, text: str) -> bool:
        """Filter out short/trivial messages, keep substantive content"""

        # Skip very short messages
        if len(text) < 100:
            return False

        # Skip purely technical/command-like messages
        technical_only_patterns = [
            r"^can you\s+\w+",
            r"^please\s+\w+",
            r"^help me\s+\w+",
            r"^fix\s+\w+",
            r"^debug\s+\w+",
        ]

        text_lower = text.lower().strip()

        # If it starts with common command patterns and is short, skip
        for pattern in technical_only_patterns:
            if re.match(pattern, text_lower) and len(text) < 200:
                return False

        # Skip if mostly code (more than 50% backticks or brackets)
        code_chars = text.count('`') + text.count('{') + text.count('[') + text.count('<')
        if code_chars / max(len(text), 1) > 0.3:
            return False

        # Keep if it has narrative/reflective qualities
        reflective_indicators = [
            'i think', 'i believe', 'i want', 'i\'m trying to',
            'my goal', 'my approach', 'the way i see',
            'in my experience', 'what i\'ve learned',
            'the challenge is', 'the reason',
            'it\'s important', 'the key is'
        ]

        if any(indicator in text_lower for indicator in reflective_indicators):
            return True

        # Keep if it's long and descriptive
        if len(text) > 300:
            return True

        return False

    def extract_user_messages(self, conversation_data: dict, metadata: dict) -> list:
        """Extract substantive user messages from a conversation"""

        user_messages = []

        if "messages" in conversation_data:
            for i, msg in enumerate(conversation_data["messages"]):
                role = msg.get("role", "")

                # Only extract from user/human messages
                if role not in ["user", "human"]:
                    continue

                content = self.extract_message_content(msg)

                if self.is_substantive(content):
                    user_messages.append({
                        "content": content,
                        "sequence": i,
                        "date": metadata.get("date"),
                        "conversation_title": metadata.get("title"),
                        "conversation_id": metadata.get("filename"),
                    })

        return user_messages

    def extract_message_content(self, message: dict) -> str:
        """Extract text content from various message formats"""
        content = message.get("content", "")

        if isinstance(content, str):
            return content
        elif isinstance(content, dict):
            if "parts" in content:
                parts = content["parts"]
                if isinstance(parts, list):
                    return " ".join(str(p) for p in parts)
                return str(parts)
            elif "text" in content:
                return content["text"]
        elif isinstance(content, list):
            texts = []
            for part in content:
                if isinstance(part, dict):
                    texts.append(part.get("text", part.get("content", "")))
                else:
                    texts.append(str(part))
            return " ".join(texts)

        return str(content)

    def categorize_message(self, content: str) -> list:
        """Categorize message into themes based on content"""

        themes = []
        content_lower = content.lower()

        # Thematic patterns
        theme_patterns = {
            "Entrepreneurship & Social Impact": [
                "bloom", "social enterprise", "entrepreneur", "impact",
                "accelerator", "startup", "fellows", "cohort"
            ],
            "Education & Pedagogy": [
                "curriculum", "training", "learning", "teach", "workshop",
                "facilitator", "assessment", "student"
            ],
            "Solar & Energy": [
                "solar", "pv", "photovoltaic", "energy", "renewable",
                "battery", "inverter", "off-grid"
            ],
            "Technology & Development": [
                "code", "api", "database", "system", "architecture",
                "development", "programming"
            ],
            "AI & Automation": [
                "ai", "gpt", "claude", "llm", "prompt", "automation",
                "machine learning"
            ],
            "Personal Growth & Values": [
                "growth", "wellbeing", "character", "strength", "value",
                "reflection", "meaning", "purpose"
            ],
            "Spiritual & Islamic": [
                "prayer", "islam", "allah", "quran", "ramadan", "thikr",
                "spiritual"
            ],
            "MENA & Lebanon": [
                "lebanon", "iraq", "mena", "beirut", "arabic", "middle east"
            ],
            "Strategy & Planning": [
                "strategy", "plan", "framework", "roadmap", "vision",
                "goal", "objective"
            ],
            "Reflection & Insights": [
                "i think", "i believe", "i've learned", "realized that",
                "what i've found", "the key insight"
            ]
        }

        for theme, keywords in theme_patterns.items():
            if any(kw in content_lower for kw in keywords):
                themes.append(theme)

        if not themes:
            themes.append("General Thoughts")

        return themes

    def extract_all_conversations(self, export_dir: Path, sample_size=None):
        """Process all conversations and extract user voice"""

        conversation_files = list(export_dir.glob("*.json"))
        total = sample_size if sample_size else len(conversation_files)

        print(f"🎤 Extracting YOUR voice from {total} conversations...")
        print("=" * 80)

        for i, filepath in enumerate(conversation_files[:total], 1):
            if i % 50 == 0:
                print(f"   Progress: {i}/{total} ({i*100//total}%)")

            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    conversation_data = json.load(f)

                # Extract metadata
                filename = filepath.name
                parts = filename.split("_")
                date_str = parts[0]
                source = parts[1] if len(parts) > 1 else "unknown"
                title = conversation_data.get("title", " ".join(parts[2:-1]))

                metadata = {
                    "date": date_str,
                    "source": source,
                    "title": title,
                    "filename": filename
                }

                # Extract user messages
                user_messages = self.extract_user_messages(conversation_data, metadata)

                # Categorize and store
                for msg in user_messages:
                    themes = self.categorize_message(msg["content"])
                    for theme in themes:
                        self.your_thoughts[theme].append(msg)
                    self.all_messages.append(msg)

            except Exception as e:
                print(f"   ⚠️  Error processing {filepath.name}: {e}")

        print(f"\n✓ Extracted {len(self.all_messages)} substantive messages from you")

    def generate_digestible_output(self, output_dir: Path):
        """Create readable markdown files organized by theme"""

        output_dir.mkdir(exist_ok=True)

        # Generate index
        index_content = f"""# Your Voice: Extracted Thoughts and Insights

**Total substantive messages extracted**: {len(self.all_messages)}

**Organized by theme**:

"""

        for theme in sorted(self.your_thoughts.keys()):
            count = len(self.your_thoughts[theme])
            index_content += f"- [{theme}]({theme.replace(' ', '_').replace('&', 'and')}.md) - {count} messages\n"

        with open(output_dir / "INDEX.md", 'w', encoding='utf-8') as f:
            f.write(index_content)

        # Generate theme files
        for theme, messages in self.your_thoughts.items():
            filename = theme.replace(' ', '_').replace('&', 'and') + '.md'

            theme_content = f"""# {theme}

**{len(messages)} substantive messages**

---

"""

            # Sort by date
            sorted_messages = sorted(messages, key=lambda x: x['date'], reverse=True)

            # Group by conversation
            by_conversation = defaultdict(list)
            for msg in sorted_messages:
                by_conversation[msg['conversation_id']].append(msg)

            for conv_id, conv_messages in sorted(by_conversation.items(),
                                                 key=lambda x: x[1][0]['date'],
                                                 reverse=True):
                first_msg = conv_messages[0]

                theme_content += f"""## 📝 {first_msg['conversation_title']}
**Date**: {first_msg['date']} | **Source**: {first_msg['conversation_id'].split('_')[1]}

"""

                for msg in sorted(conv_messages, key=lambda x: x['sequence']):
                    # Clean up the content
                    content = msg['content'].strip()

                    # Add quote formatting
                    theme_content += f"> {content}\n\n"
                    theme_content += "---\n\n"

            with open(output_dir / filename, 'w', encoding='utf-8') as f:
                f.write(theme_content)

        print(f"\n✅ Generated {len(self.your_thoughts)} theme files in {output_dir}")

    def generate_highlights(self, output_dir: Path, top_n=50):
        """Generate a highlights file with the most interesting messages"""

        # Score messages by length and reflective quality
        scored_messages = []

        for msg in self.all_messages:
            score = len(msg['content']) / 100  # Base score from length

            # Boost for reflective language
            reflective_boost = sum(1 for phrase in [
                'i think', 'i believe', 'i\'ve learned', 'realized',
                'the key', 'important to', 'what matters'
            ] if phrase in msg['content'].lower())

            score += reflective_boost * 2

            scored_messages.append((score, msg))

        # Get top N
        top_messages = sorted(scored_messages, key=lambda x: x[0], reverse=True)[:top_n]

        highlights_content = f"""# Your Highlights: Top {top_n} Most Substantive Thoughts

These are your most reflective, detailed, and insightful messages.

---

"""

        for i, (score, msg) in enumerate(top_messages, 1):
            highlights_content += f"""## {i}. {msg['conversation_title']}
**Date**: {msg['date']} | **Score**: {score:.1f}

> {msg['content'].strip()}

---

"""

        with open(output_dir / "HIGHLIGHTS.md", 'w', encoding='utf-8') as f:
            f.write(highlights_content)

        print(f"✅ Generated HIGHLIGHTS.md with top {top_n} messages")

    def generate_timeline(self, output_dir: Path):
        """Generate chronological view of your thoughts"""

        timeline_content = """# Timeline: Your Thoughts Over Time

Chronological view of your most substantive messages.

---

"""

        # Sort all messages by date
        sorted_msgs = sorted(self.all_messages, key=lambda x: x['date'])

        current_month = None
        for msg in sorted_msgs:
            month = msg['date'][:7]  # YYYY-MM

            if month != current_month:
                timeline_content += f"\n## {month}\n\n"
                current_month = month

            timeline_content += f"""### {msg['conversation_title']} ({msg['date']})

> {msg['content'][:300]}{"..." if len(msg['content']) > 300 else ""}

---

"""

        with open(output_dir / "TIMELINE.md", 'w', encoding='utf-8') as f:
            f.write(timeline_content)

        print("✅ Generated TIMELINE.md")


def main():
    """Main execution"""

    export_dir = Path("/home/user/chatgpt-exporter/exported_conversations")
    output_dir = Path("/home/user/chatgpt-exporter/your_voice")

    extractor = VoiceExtractor()

    # Process conversations (all or sample)
    # Change to None to process all
    sample_size = 500  # Start with 500 for testing

    extractor.extract_all_conversations(export_dir, sample_size=sample_size)

    # Generate outputs
    print("\n📝 Generating digestible outputs...")
    print("=" * 80)

    extractor.generate_digestible_output(output_dir)
    extractor.generate_highlights(output_dir, top_n=100)
    extractor.generate_timeline(output_dir)

    print("\n" + "=" * 80)
    print("🎯 Your Voice Extraction Complete!")
    print(f"\nFiles generated in: {output_dir}/")
    print(f"- INDEX.md - Navigation to all themes")
    print(f"- {len(extractor.your_thoughts)} theme files with your messages")
    print(f"- HIGHLIGHTS.md - Top 100 most substantive messages")
    print(f"- TIMELINE.md - Chronological view")
    print("\nStart by reading: your_voice/HIGHLIGHTS.md")


if __name__ == "__main__":
    main()
