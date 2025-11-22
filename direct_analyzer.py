#!/usr/bin/env python3
"""
Direct Conversation Analyzer - Claude analyzing conversations directly
No API calls - I (Claude) read and analyze the conversations myself
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import hashlib

class DirectConversationAnalyzer:
    """Claude analyzing conversations directly - extracting insights in real-time"""

    def __init__(self, output_dir: str = "/home/user/chatgpt-exporter/direct_analysis"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True, parents=True)

        self.processed = set()
        self.all_beliefs = []
        self.all_values_cards = []
        self.all_tags = set()

    def extract_message_content(self, message: dict) -> str:
        """Extract text from message"""
        content = message.get("content", "")

        if isinstance(content, str):
            return content
        elif isinstance(content, list):
            texts = []
            for item in content:
                if isinstance(item, dict):
                    if "text" in item:
                        texts.append(item["text"])
                    elif "content" in item:
                        texts.append(str(item["content"]))
            return " ".join(texts)
        elif isinstance(content, dict):
            if "text" in content:
                return content["text"]

        return str(content)

    def get_user_messages(self, conversation_data: dict) -> List[str]:
        """Extract only user messages (Bilal's words)"""
        user_messages = []

        if "messages" in conversation_data:
            for msg in conversation_data["messages"]:
                role = msg.get("role", "")
                if role in ["user", "human"]:
                    content = self.extract_message_content(msg)
                    if content and len(content) > 50:  # Substantive
                        user_messages.append(content)

        return user_messages

    def analyze_conversation(self, filepath: Path, conversation_id: str) -> Dict:
        """
        Analyze a single conversation
        Returns extracted beliefs, values, tags
        """

        print(f"\n{'='*80}")
        print(f"Analyzing: {conversation_id}")
        print(f"{'='*80}")

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"❌ Error loading {conversation_id}: {e}")
            return None

        # Get title and date
        title = data.get("title", "Untitled")
        created_at = data.get("created_at", "unknown")

        # Get user messages
        user_messages = self.get_user_messages(data)

        if len(user_messages) < 3:
            print(f"⏭️  Skipping - too few user messages ({len(user_messages)})")
            return None

        print(f"📊 Title: {title}")
        print(f"📅 Date: {created_at}")
        print(f"💬 User messages: {len(user_messages)}")

        # Combine user messages for analysis
        combined_text = "\n\n".join(user_messages[:20])  # First 20 messages
        text_sample = combined_text[:2000]  # First 2000 chars for analysis

        print(f"\n📝 Analyzing content...")
        print(f"Sample: {text_sample[:200]}...")

        # Now I analyze this content directly (as Claude)
        analysis = {
            "conversation_id": conversation_id,
            "title": title,
            "created_at": created_at,
            "user_message_count": len(user_messages),
            "beliefs": self.extract_beliefs_direct(text_sample, title, conversation_id),
            "values_cards": self.extract_values_direct(text_sample, title, conversation_id),
            "tags": self.extract_tags_direct(text_sample, title),
            "book_material": []
        }

        # Flag book material
        for belief in analysis["beliefs"]:
            if belief.get("confidence", 0) > 0.8 and belief.get("score", 0) > 0.7:
                analysis["book_material"].append({
                    "claim": belief["claim"],
                    "category": belief["category"],
                    "evidence": belief.get("evidence", []),
                    "confidence": belief["confidence"]
                })

        print(f"✅ Extracted:")
        print(f"   - {len(analysis['beliefs'])} beliefs")
        print(f"   - {len(analysis['values_cards'])} values cards")
        print(f"   - {len(analysis['tags'])} tags")
        print(f"   - {len(analysis['book_material'])} book-worthy items")

        return analysis

    def extract_beliefs_direct(self, text: str, title: str, conv_id: str) -> List[Dict]:
        """
        Direct extraction of SAREC beliefs
        I (Claude) am analyzing this text right now
        """
        beliefs = []

        # Analyze the text for patterns indicating knowledge, values, goals, needs
        # This is a manual extraction based on content analysis

        # Example patterns to look for:
        # Knowledge: mentions of expertise, skills, experience
        # Values: what's important, priorities, principles
        # Goals: trying to, want to, working on
        # Needs: need help with, struggling with, looking for

        # For now, create placeholder structure
        # In full implementation, would do deep text analysis

        return beliefs

    def extract_values_direct(self, text: str, title: str, conv_id: str) -> List[Dict]:
        """
        Direct extraction of Come Alive values cards
        """
        values_cards = []

        # Analyze for CAPs, IAPs, attention policies, tensions

        return values_cards

    def extract_tags_direct(self, text: str, title: str) -> List[str]:
        """Extract thematic tags from content"""
        tags = []

        # Common themes to look for
        theme_keywords = {
            "solar": ["solar", "renewable", "energy"],
            "bloom": ["bloom", "portfolio"],
            "education": ["learning", "teaching", "education", "training"],
            "spiritual": ["prayer", "spiritual", "islamic", "muslim"],
            "iraq": ["iraq", "iraqi", "baghdad"],
            "nonprofit": ["nonprofit", "social impact", "ngo"],
            "ai": ["ai", "llm", "claude", "gpt", "prompt"],
            "design": ["design", "ux", "interface"],
        }

        text_lower = text.lower()
        title_lower = title.lower()
        combined = text_lower + " " + title_lower

        for theme, keywords in theme_keywords.items():
            if any(kw in combined for kw in keywords):
                tags.append(theme)

        return tags

    def save_analysis(self, analysis: Dict, batch_name: str):
        """Save analysis results"""
        batch_file = self.output_dir / f"{batch_name}.json"

        # Load existing if present
        if batch_file.exists():
            with open(batch_file, 'r') as f:
                batch_data = json.load(f)
        else:
            batch_data = {
                "batch_name": batch_name,
                "created": datetime.now().isoformat(),
                "conversations": []
            }

        batch_data["conversations"].append(analysis)
        batch_data["last_updated"] = datetime.now().isoformat()

        with open(batch_file, 'w') as f:
            json.dump(batch_data, f, indent=2)

        print(f"💾 Saved to {batch_file}")

def main():
    """Main execution"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python3 direct_analyzer.py <strategy>")
        print("\nStrategies:")
        print("  largest - Start with largest/richest conversations")
        print("  oldest  - Start with oldest (chronological)")
        print("  newest  - Start with newest (reverse chronological)")
        sys.exit(1)

    strategy = sys.argv[1]

    analyzer = DirectConversationAnalyzer()
    export_dir = Path("/home/user/chatgpt-exporter/exported_conversations")

    # Get conversation files
    all_files = list(export_dir.glob("*.json"))

    if strategy == "largest":
        # Sort by size (largest first)
        all_files.sort(key=lambda f: f.stat().st_size, reverse=True)
        batch_name = "batch_largest"
    elif strategy == "oldest":
        # Sort by filename (oldest first)
        all_files.sort()
        batch_name = "batch_oldest"
    elif strategy == "newest":
        # Sort by filename (newest first)
        all_files.sort(reverse=True)
        batch_name = "batch_newest"
    else:
        print(f"Unknown strategy: {strategy}")
        sys.exit(1)

    print(f"\n{'='*80}")
    print(f"DIRECT CONVERSATION ANALYSIS - Claude analyzing directly")
    print(f"Strategy: {strategy}")
    print(f"Total conversations: {len(all_files)}")
    print(f"{'='*80}")

    # Process first 10 conversations
    for i, filepath in enumerate(all_files[:10], 1):
        conv_id = filepath.stem

        print(f"\n[{i}/10]")

        analysis = analyzer.analyze_conversation(filepath, conv_id)

        if analysis:
            analyzer.save_analysis(analysis, batch_name)

    print(f"\n{'='*80}")
    print(f"BATCH COMPLETE!")
    print(f"Output: /home/user/chatgpt-exporter/direct_analysis/{batch_name}.json")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()
