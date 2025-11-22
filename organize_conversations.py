#!/usr/bin/env python3
"""
Organize Exported Conversations
Creates a folder for each conversation with metadata and analysis structure
"""

import json
import shutil
from pathlib import Path
from datetime import datetime
import hashlib


def extract_message_content(message: dict) -> str:
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
            str(part.get("text", part.get("content", "")))
            for part in content if isinstance(part, dict)
        )
    return str(content)


def calculate_conversation_hash(conversation_data: dict) -> str:
    """Generate unique hash for conversation content"""
    content = json.dumps(conversation_data, sort_keys=True)
    return hashlib.sha256(content.encode()).hexdigest()[:16]


def extract_metadata(conversation_file: Path, conversation_data: dict) -> dict:
    """Extract comprehensive metadata from conversation"""

    filename = conversation_file.name
    parts = filename.split("_")

    # Parse filename
    date_str = parts[0]
    source = parts[1] if len(parts) > 1 else "unknown"
    title = conversation_data.get("title", " ".join(parts[2:-1]))

    # Count messages by role
    user_messages = 0
    assistant_messages = 0
    user_chars = 0
    assistant_chars = 0

    if "messages" in conversation_data:
        for msg in conversation_data["messages"]:
            role = msg.get("role", "")
            content = extract_message_content(msg)

            if role in ["user", "human"]:
                user_messages += 1
                user_chars += len(content)
            elif role == "assistant":
                assistant_messages += 1
                assistant_chars += len(content)

    # Calculate conversation metrics
    total_messages = user_messages + assistant_messages
    avg_user_length = user_chars / max(user_messages, 1)
    avg_assistant_length = assistant_chars / max(assistant_messages, 1)
    depth_score = total_messages / 10  # Normalized depth

    return {
        "id": filename.replace(".json", ""),
        "filename": filename,
        "title": title,
        "date": date_str,
        "source": source,
        "created_at": conversation_data.get("created_at"),
        "updated_at": conversation_data.get("updated_at"),
        "hash": calculate_conversation_hash(conversation_data),
        "statistics": {
            "total_messages": total_messages,
            "user_messages": user_messages,
            "assistant_messages": assistant_messages,
            "user_chars": user_chars,
            "assistant_chars": assistant_chars,
            "avg_user_length": round(avg_user_length, 1),
            "avg_assistant_length": round(avg_assistant_length, 1),
            "depth_score": round(depth_score, 2),
        },
        "file_info": {
            "size_bytes": conversation_file.stat().st_size,
            "created": datetime.fromtimestamp(conversation_file.stat().st_ctime).isoformat(),
            "modified": datetime.fromtimestamp(conversation_file.stat().st_mtime).isoformat(),
        },
        "processing": {
            "organized_at": datetime.now().isoformat(),
            "version": "1.0",
            "status": "pending_analysis",
        }
    }


def create_conversation_folder(conversation_file: Path, output_base: Path) -> Path:
    """Create organized folder structure for a conversation"""

    # Read conversation
    with open(conversation_file, 'r', encoding='utf-8') as f:
        conversation_data = json.load(f)

    # Create folder name (use filename without .json)
    folder_name = conversation_file.stem
    conversation_folder = output_base / folder_name
    conversation_folder.mkdir(exist_ok=True)

    # 1. Copy original conversation
    shutil.copy(conversation_file, conversation_folder / "conversation.json")

    # 2. Generate metadata
    metadata = extract_metadata(conversation_file, conversation_data)
    with open(conversation_folder / "metadata.json", 'w') as f:
        json.dump(metadata, f, indent=2)

    # 3. Create placeholder files for analysis

    # Theory of Mind (to be populated by LLM)
    tom_structure = {
        "conversation_id": metadata["id"],
        "beliefs": {
            "knowledge": [],
            "values": [],
            "goals": [],
            "needs": []
        },
        "status": "pending",
        "analyzed_at": None
    }
    with open(conversation_folder / "theory_of_mind.json", 'w') as f:
        json.dump(tom_structure, f, indent=2)

    # Highlights (to be populated)
    highlights_structure = {
        "conversation_id": metadata["id"],
        "highlights": [],
        "status": "pending",
        "extracted_at": None
    }
    with open(conversation_folder / "highlights.json", 'w') as f:
        json.dump(highlights_structure, f, indent=2)

    # Transitions (to be populated)
    transitions_structure = {
        "conversation_id": metadata["id"],
        "transitions": [],
        "status": "pending",
        "analyzed_at": None
    }
    with open(conversation_folder / "transitions.json", 'w') as f:
        json.dump(transitions_structure, f, indent=2)

    # Themes (to be populated)
    themes_structure = {
        "conversation_id": metadata["id"],
        "primary_themes": [],
        "secondary_themes": [],
        "cross_cutting_themes": [],
        "status": "pending",
        "analyzed_at": None
    }
    with open(conversation_folder / "themes.json", 'w') as f:
        json.dump(themes_structure, f, indent=2)

    # Create README for the conversation
    readme_content = f"""# {metadata['title']}

**ID**: {metadata['id']}
**Date**: {metadata['date']}
**Source**: {metadata['source']}

## Statistics
- Total messages: {metadata['statistics']['total_messages']}
- User messages: {metadata['statistics']['user_messages']}
- Assistant messages: {metadata['statistics']['assistant_messages']}
- Depth score: {metadata['statistics']['depth_score']}

## Files in this folder

- `conversation.json` - Original exported conversation
- `metadata.json` - Comprehensive metadata and statistics
- `theory_of_mind.json` - Beliefs extracted from this conversation (knowledge, values, goals, needs)
- `highlights.json` - Key insights and quotes from user
- `transitions.json` - Shifts in thinking or approach during conversation
- `themes.json` - Core themes and topics covered

## Status

Processing status: {metadata['processing']['status']}
Organized at: {metadata['processing']['organized_at']}
"""

    with open(conversation_folder / "README.md", 'w') as f:
        f.write(readme_content)

    return conversation_folder


def organize_all_conversations(export_dir: Path, output_dir: Path, limit: int = None):
    """Organize all exported conversations into structured folders"""

    output_dir.mkdir(exist_ok=True)

    conversation_files = list(export_dir.glob("*.json"))
    total = limit if limit else len(conversation_files)

    print(f"📁 Organizing {total} conversations into structured folders")
    print("=" * 80)

    organized = []

    for i, conversation_file in enumerate(conversation_files[:total], 1):
        if i % 50 == 0:
            print(f"   Progress: {i}/{total} ({i*100//total}%)")

        try:
            folder = create_conversation_folder(conversation_file, output_dir)
            organized.append({
                "filename": conversation_file.name,
                "folder": folder.name,
                "status": "organized"
            })
        except Exception as e:
            print(f"   ⚠️  Error organizing {conversation_file.name}: {e}")
            organized.append({
                "filename": conversation_file.name,
                "folder": None,
                "status": "error",
                "error": str(e)
            })

    print(f"\n✓ Organized {len([o for o in organized if o['status'] == 'organized'])} conversations")

    # Create index
    index = {
        "total_conversations": total,
        "organized_at": datetime.now().isoformat(),
        "conversations": organized
    }

    with open(output_dir / "INDEX.json", 'w') as f:
        json.dump(index, f, indent=2)

    # Create master README
    readme = f"""# Organized Conversations

**Total conversations**: {total}
**Organized**: {len([o for o in organized if o['status'] == 'organized'])}
**Errors**: {len([o for o in organized if o['status'] == 'error'])}

## Structure

Each conversation is in its own folder with:

```
<conversation_id>/
├── conversation.json      # Original export
├── metadata.json          # Stats and info
├── theory_of_mind.json    # Beliefs extracted (to be populated by LLM)
├── highlights.json        # Key insights (to be populated)
├── transitions.json       # Thinking shifts (to be populated)
├── themes.json           # Core themes (to be populated)
└── README.md             # Human-readable summary
```

## Files

- `INDEX.json` - List of all organized conversations
- `README.md` - This file

## Next Steps

1. Run LLM analysis to populate theory_of_mind.json for each conversation
2. Extract highlights from user messages
3. Identify transitions and theme evolution
4. Generate aggregate analysis across all conversations

## Usage

```bash
# List all conversations
cat INDEX.json | jq '.conversations[] | .folder'

# Read a specific conversation
cat 2023-03-21_claude_Bilal_s_strengths_8f6f6926/README.md

# Check metadata
cat 2023-03-21_claude_Bilal_s_strengths_8f6f6926/metadata.json
```
"""

    with open(output_dir / "README.md", 'w') as f:
        f.write(readme)

    print(f"\n✅ Index and README created")
    print(f"   Output directory: {output_dir}")
    print(f"   See {output_dir}/README.md for usage")


def main():
    """Main execution"""

    import sys

    export_dir = Path("/home/user/chatgpt-exporter/exported_conversations")
    output_dir = Path("/home/user/chatgpt-exporter/conversations")

    # Optional: limit number of conversations to organize
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else None

    if limit:
        print(f"Processing first {limit} conversations (for testing)")
    else:
        print("Processing ALL conversations")

    organize_all_conversations(export_dir, output_dir, limit=limit)

    print("\n" + "=" * 80)
    print("🎯 Organization complete!")
    print(f"\nConversations organized in: {output_dir}/")
    print("\nEach conversation now has:")
    print("  ✓ Original JSON")
    print("  ✓ Metadata with statistics")
    print("  ✓ Placeholder for Theory of Mind")
    print("  ✓ Placeholder for Highlights")
    print("  ✓ Placeholder for Transitions")
    print("  ✓ Placeholder for Themes")
    print("\nNext: Run LLM analysis to populate the placeholders")


if __name__ == "__main__":
    main()
