#!/usr/bin/env python3
"""
Theory of Mind Builder - SAREC Edition
Processes conversations to build an evidence-based model of Bilal's knowledge, values, goals, and needs
"""

import json
import os
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Any
import hashlib


class SARECAssessment:
    """Structured Assessment with Reasoning, Evidence, and Confidence"""

    def __init__(
        self,
        belief_id: str,
        category: str,
        subcategory: str,
        claim: str,
        score: float,
        reasoning: str,
        evidence: List[Dict],
        confidence: float,
    ):
        self.belief_id = belief_id
        self.category = category
        self.subcategory = subcategory
        self.claim = claim
        self.score = score
        self.reasoning = reasoning
        self.evidence = evidence
        self.confidence = confidence
        self.first_observed = None
        self.last_updated = datetime.now().isoformat()
        self.conversation_count = len([e for e in evidence if e.get("type") == "conversation"])
        self.evolution = []

    def to_dict(self):
        return {
            "belief_id": self.belief_id,
            "category": self.category,
            "subcategory": self.subcategory,
            "claim": self.claim,
            "score": round(self.score, 3),
            "reasoning": self.reasoning,
            "evidence": self.evidence,
            "confidence": round(self.confidence, 3),
            "first_observed": self.first_observed,
            "last_updated": self.last_updated,
            "conversation_count": self.conversation_count,
            "evolution": self.evolution,
        }


class TheoryOfMindBuilder:
    """Builds comprehensive Theory of Mind from conversation analysis"""

    def __init__(self, output_dir="/home/user/chatgpt-exporter/theory_of_mind"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Theory of Mind state
        self.knowledge = {}  # What Bilal knows
        self.values = {}  # What Bilal cares about
        self.goals = {}  # What Bilal is trying to do
        self.needs = {}  # What Bilal needs
        self.contributions = {}  # How each conversation helped

        # Signal patterns for detection
        self.init_signal_patterns()

    def init_signal_patterns(self):
        """Define patterns for detecting ToM signals in conversations"""

        # KNOWLEDGE signals - technical terminology, explanations, teaching
        self.knowledge_patterns = {
            "solar_energy": {
                "keywords": [
                    r"\bpv\b",
                    r"\bphotovoltaic",
                    r"\bsolar panel",
                    r"\binverter",
                    r"\bbattery",
                    r"\bcharge controller",
                    r"\boff-grid",
                    r"\bload calculation",
                ],
                "expertise_indicators": ["teach", "train", "explain", "design", "size", "calculate"],
            },
            "web_development": {
                "keywords": [r"\breact", r"\bnode", r"\bjavascript", r"\btypescript", r"\bapi", r"\bcomponent"],
                "expertise_indicators": ["debug", "refactor", "optimize", "implement"],
            },
            "ai_ml": {
                "keywords": [r"\bgpt", r"\bclaude", r"\bprompt", r"\bllm", r"\bai\b", r"\bmachine learning"],
                "expertise_indicators": ["prompt engineering", "fine-tun", "model", "inference"],
            },
            "data_visualization": {
                "keywords": [r"\bd3\.js", r"\bchart", r"\bvisualization", r"\bgraph", r"\bdata viz"],
                "expertise_indicators": ["visualize", "plot", "dashboard", "interactive"],
            },
            "education_pedagogy": {
                "keywords": [
                    r"\bcurriculum",
                    r"\blearning",
                    r"\bworkshop",
                    r"\btraining",
                    r"\bfacilitat",
                    r"\bpedagogy",
                ],
                "expertise_indicators": ["design", "develop", "teach", "assess", "evaluate"],
            },
        }

        # VALUES signals - emotional language, priorities, decisions
        self.value_patterns = {
            "impact_over_profit": ["impact", "social good", "change", "empower", "capacity building"],
            "spiritual_integration": ["prayer", "islam", "allah", "quran", "thikr", "ramadan", "spiritual"],
            "education_empowerment": ["learning", "growth", "develop", "empower", "enable", "support"],
            "quality_excellence": ["quality", "excellence", "best practice", "thorough", "rigorous"],
            "cultural_sensitivity": ["context", "culture", "adapt", "localize", "arabic", "mena"],
        }

        # GOALS signals - future tense, planning, aspirations
        self.goal_patterns = {
            "project_keywords": ["working on", "building", "developing", "creating", "launching"],
            "aspirational": ["want to", "hope to", "trying to", "goal is", "aiming to"],
            "planning": ["plan", "roadmap", "next step", "will", "going to"],
        }

        # NEEDS signals - questions, problems, challenges
        self.need_patterns = {
            "knowledge_gap": ["how do i", "don't know", "not sure", "help me understand", "confused"],
            "resource_need": ["need", "looking for", "require", "searching"],
            "problem": ["error", "issue", "problem", "challenge", "stuck", "not working"],
            "support": ["help", "advice", "feedback", "review", "suggest"],
        }

    def extract_conversation_signals(self, conversation_data: Dict, metadata: Dict) -> Dict:
        """Extract knowledge, value, goal, and need signals from a conversation"""

        signals = {"knowledge": [], "values": [], "goals": [], "needs": [], "meta": {}}

        # Combine all message content
        full_text = ""
        user_messages = []
        assistant_messages = []

        if "messages" in conversation_data:
            for msg in conversation_data["messages"]:
                content = self.extract_message_content(msg)
                full_text += content + "\n"
                if msg.get("role") == "user" or msg.get("role") == "human":
                    user_messages.append(content)
                elif msg.get("role") == "assistant":
                    assistant_messages.append(content)

        full_text_lower = full_text.lower()

        # Extract KNOWLEDGE signals
        for domain, patterns in self.knowledge_patterns.items():
            keyword_matches = sum(1 for kw in patterns["keywords"] if re.search(kw, full_text_lower))
            expertise_matches = sum(
                1 for ind in patterns["expertise_indicators"] if ind.lower() in full_text_lower
            )

            if keyword_matches >= 2 or expertise_matches >= 1:
                # Calculate confidence based on depth of engagement
                confidence = min(0.95, (keyword_matches * 0.1 + expertise_matches * 0.15))

                signals["knowledge"].append(
                    {
                        "domain": domain,
                        "keyword_matches": keyword_matches,
                        "expertise_indicators": expertise_matches,
                        "confidence": confidence,
                        "evidence_snippets": self.extract_relevant_snippets(
                            full_text, patterns["keywords"][:3]
                        ),
                    }
                )

        # Extract VALUES signals
        for value, keywords in self.value_patterns.items():
            matches = sum(1 for kw in keywords if kw.lower() in full_text_lower)
            if matches >= 1:
                # Check if Bilal (user) is expressing the value vs just discussing it
                user_text = " ".join(user_messages).lower()
                user_mentions = sum(1 for kw in keywords if kw.lower() in user_text)

                confidence = min(0.9, matches * 0.2)
                if user_mentions > 0:
                    confidence += 0.1  # Higher confidence if user (Bilal) mentions it

                signals["values"].append(
                    {"value": value, "mentions": matches, "user_mentions": user_mentions, "confidence": confidence}
                )

        # Extract GOALS signals
        goals_found = []
        for pattern_type, keywords in self.goal_patterns.items():
            for kw in keywords:
                if kw in full_text_lower:
                    # Extract sentences containing goal language
                    sentences = [s for s in full_text.split(".") if kw in s.lower()]
                    goals_found.extend(sentences[:2])  # Top 2 relevant sentences

        if goals_found:
            signals["goals"] = goals_found

        # Extract NEEDS signals
        for need_type, keywords in self.need_patterns.items():
            matches = []
            for kw in keywords:
                if kw in " ".join(user_messages).lower():  # Only from user (Bilal)
                    sentences = [s for s in user_messages if kw in s.lower()]
                    matches.extend(sentences[:1])

            if matches:
                signals["needs"].append({"type": need_type, "evidence": matches})

        # Meta-analysis
        signals["meta"] = {
            "message_count": len(conversation_data.get("messages", [])),
            "user_message_count": len(user_messages),
            "assistant_message_count": len(assistant_messages),
            "user_avg_length": sum(len(m) for m in user_messages) / max(len(user_messages), 1),
            "depth_score": len(conversation_data.get("messages", [])) / 10,  # Normalize
        }

        return signals

    def extract_message_content(self, message: Dict) -> str:
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
            return " ".join(
                str(part.get("text", part.get("content", ""))) for part in content if isinstance(part, dict)
            )

        return str(content)

    def extract_relevant_snippets(self, text: str, patterns: List[str], max_snippets=2) -> List[str]:
        """Extract short snippets around pattern matches"""
        snippets = []
        for pattern in patterns:
            matches = list(re.finditer(pattern, text, re.IGNORECASE))
            for match in matches[:max_snippets]:
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                snippet = text[start:end].strip()
                snippets.append(f"...{snippet}...")
                if len(snippets) >= max_snippets:
                    break
            if len(snippets) >= max_snippets:
                break
        return snippets

    def update_theory_of_mind(self, conversation_id: str, signals: Dict, metadata: Dict):
        """Update ToM beliefs based on conversation signals"""

        date = metadata.get("date", "unknown")

        # Update KNOWLEDGE beliefs
        for knowledge_signal in signals.get("knowledge", []):
            domain = knowledge_signal["domain"]
            belief_id = f"bilal.knowledge.{domain}"

            if belief_id not in self.knowledge:
                # Create new knowledge belief
                self.knowledge[belief_id] = {
                    "belief_id": belief_id,
                    "category": "knowledge",
                    "subcategory": domain,
                    "claim": f"Bilal has expertise in {domain.replace('_', ' ')}",
                    "score": knowledge_signal["confidence"],
                    "reasoning": f"Demonstrated through technical terminology and expertise indicators",
                    "evidence": [],
                    "confidence": knowledge_signal["confidence"],
                    "first_observed": date,
                    "last_updated": date,
                    "conversation_count": 1,
                    "evolution": [],
                }
            else:
                # Update existing belief
                old_score = self.knowledge[belief_id]["score"]
                # Weighted average with recency bias
                new_score = (old_score * 0.7 + knowledge_signal["confidence"] * 0.3)
                self.knowledge[belief_id]["score"] = min(0.95, new_score)
                self.knowledge[belief_id]["last_updated"] = date
                self.knowledge[belief_id]["conversation_count"] += 1

            # Add evidence
            evidence_entry = {
                "type": "conversation",
                "id": conversation_id,
                "date": date,
                "weight": knowledge_signal["confidence"],
                "snippets": knowledge_signal.get("evidence_snippets", []),
            }
            self.knowledge[belief_id]["evidence"].append(evidence_entry)

        # Update VALUES beliefs (similar pattern)
        for value_signal in signals.get("values", []):
            value = value_signal["value"]
            belief_id = f"bilal.values.{value}"

            if belief_id not in self.values:
                self.values[belief_id] = {
                    "belief_id": belief_id,
                    "category": "values",
                    "subcategory": value,
                    "claim": f"Bilal values {value.replace('_', ' ')}",
                    "score": value_signal["confidence"],
                    "reasoning": f"Mentioned {value_signal['mentions']} times, {value_signal['user_mentions']} by user",
                    "evidence": [],
                    "confidence": value_signal["confidence"],
                    "first_observed": date,
                    "last_updated": date,
                    "conversation_count": 1,
                }
            else:
                old_score = self.values[belief_id]["score"]
                new_score = (old_score * 0.8 + value_signal["confidence"] * 0.2)
                self.values[belief_id]["score"] = min(0.95, new_score)
                self.values[belief_id]["last_updated"] = date
                self.values[belief_id]["conversation_count"] += 1

            self.values[belief_id]["evidence"].append(
                {
                    "type": "conversation",
                    "id": conversation_id,
                    "date": date,
                    "mentions": value_signal["mentions"],
                }
            )

        # Track contribution of this conversation
        self.contributions[conversation_id] = {
            "conversation_id": conversation_id,
            "title": metadata.get("title", "Untitled"),
            "date": date,
            "knowledge_domains": [s["domain"] for s in signals.get("knowledge", [])],
            "values_expressed": [s["value"] for s in signals.get("values", [])],
            "goals_mentioned": len(signals.get("goals", [])),
            "needs_identified": [n["type"] for n in signals.get("needs", [])],
            "depth_score": signals.get("meta", {}).get("depth_score", 0),
        }

    def save_theory_of_mind(self):
        """Save all ToM beliefs to organized folder structure"""

        # Save knowledge beliefs
        knowledge_dir = self.output_dir / "knowledge"
        knowledge_dir.mkdir(exist_ok=True)
        with open(knowledge_dir / "all_knowledge.json", "w") as f:
            json.dump(self.knowledge, f, indent=2)

        # Save values beliefs
        values_dir = self.output_dir / "values"
        values_dir.mkdir(exist_ok=True)
        with open(values_dir / "all_values.json", "w") as f:
            json.dump(self.values, f, indent=2)

        # Save contributions
        contrib_dir = self.output_dir / "contributions"
        contrib_dir.mkdir(exist_ok=True)
        with open(contrib_dir / "all_contributions.json", "w") as f:
            json.dump(self.contributions, f, indent=2)

        # Generate summary README
        self.generate_summary_readme()

        print(f"\n✅ Theory of Mind saved to: {self.output_dir}")

    def generate_summary_readme(self):
        """Generate human-readable summary of ToM"""

        readme_content = f"""# Theory of Mind: Bilal Ghalib
## Generated from {len(self.contributions)} conversations

### Top Knowledge Domains (by confidence)

"""

        # Sort knowledge by score
        sorted_knowledge = sorted(self.knowledge.values(), key=lambda x: x["score"], reverse=True)
        for belief in sorted_knowledge[:15]:
            readme_content += f"- **{belief['claim']}** (confidence: {belief['confidence']:.2f}, {belief['conversation_count']} conversations)\n"

        readme_content += f"\n### Core Values (by confidence)\n\n"

        sorted_values = sorted(self.values.values(), key=lambda x: x["score"], reverse=True)
        for belief in sorted_values[:10]:
            readme_content += f"- **{belief['claim']}** (confidence: {belief['confidence']:.2f}, {belief['conversation_count']} conversations)\n"

        readme_content += f"\n### Most Valuable Conversations (by depth)\n\n"

        sorted_contribs = sorted(self.contributions.values(), key=lambda x: x["depth_score"], reverse=True)
        for contrib in sorted_contribs[:10]:
            readme_content += f"- **{contrib['title']}** ({contrib['date']}) - Depth: {contrib['depth_score']:.1f}\n"
            readme_content += f"  - Knowledge: {', '.join(contrib['knowledge_domains'])}\n"

        with open(self.output_dir / "README.md", "w") as f:
            f.write(readme_content)


def main():
    """Process conversations and build Theory of Mind"""

    export_dir = Path("/home/user/chatgpt-exporter/exported_conversations")
    tom_builder = TheoryOfMindBuilder()

    print("🧠 Building Theory of Mind from conversations...")
    print("=" * 80)

    conversation_files = list(export_dir.glob("*.json"))
    total = len(conversation_files)

    # Process a sample first (for testing)
    sample_size = 100  # Process first 100 for initial analysis

    for i, filepath in enumerate(conversation_files[:sample_size], 1):
        if i % 10 == 0:
            print(f"   Progress: {i}/{sample_size} ({i*100//sample_size}%)")

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                conversation_data = json.load(f)

            # Extract metadata
            filename = filepath.name
            parts = filename.split("_")
            date_str = parts[0]
            source = parts[1] if len(parts) > 1 else "unknown"
            title = conversation_data.get("title", " ".join(parts[2:-1]))

            metadata = {"date": date_str, "source": source, "title": title, "filename": filename}

            # Extract signals
            signals = tom_builder.extract_conversation_signals(conversation_data, metadata)

            # Update Theory of Mind
            conversation_id = filename.replace(".json", "")
            tom_builder.update_theory_of_mind(conversation_id, signals, metadata)

        except Exception as e:
            print(f"   ⚠️  Error processing {filepath.name}: {e}")

    print(f"\n✓ Processed {sample_size} conversations")

    # Save results
    tom_builder.save_theory_of_mind()

    print("\n" + "=" * 80)
    print(f"📊 Theory of Mind Summary:")
    print(f"   Knowledge domains identified: {len(tom_builder.knowledge)}")
    print(f"   Values identified: {len(tom_builder.values)}")
    print(f"   Conversations analyzed: {len(tom_builder.contributions)}")


if __name__ == "__main__":
    main()
