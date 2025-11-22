#!/usr/bin/env python3
"""
Break conversations into readable chunks for Claude to analyze directly
"""

import json
from pathlib import Path
import sys

def extract_message_content(message):
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
        return " ".join(texts)
    return str(content)

def chunk_conversation(filepath, max_chunk_chars=50000):
    """Break conversation into analyzable chunks"""

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    title = data.get("title", "Untitled")
    created_at = data.get("created_at", "unknown")
    conv_id = filepath.stem

    # Extract messages
    messages = []
    if "messages" in data:
        for msg in data["messages"]:
            role = msg.get("role", "unknown")
            content = extract_message_content(msg)
            speaker = "BILAL" if role in ["user", "human"] else "AI"
            if content:
                messages.append(f"[{speaker}]: {content}")

    # Create chunks
    chunks = []
    current_chunk = []
    current_size = 0

    for msg in messages:
        msg_size = len(msg)

        if current_size + msg_size > max_chunk_chars and current_chunk:
            chunks.append("\n\n".join(current_chunk))
            current_chunk = []
            current_size = 0

        current_chunk.append(msg)
        current_size += msg_size

    if current_chunk:
        chunks.append("\n\n".join(current_chunk))

    return {
        "conversation_id": conv_id,
        "title": title,
        "created_at": created_at,
        "total_messages": len(messages),
        "chunks": chunks
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 chunk_for_analysis.py <conversation_file>")
        sys.exit(1)

    filepath = Path(sys.argv[1])

    result = chunk_conversation(filepath)

    print(f"Conversation: {result['title']}")
    print(f"ID: {result['conversation_id']}")
    print(f"Date: {result['created_at']}")
    print(f"Messages: {result['total_messages']}")
    print(f"Chunks: {len(result['chunks'])}")
    print()

    # Save chunks
    output_dir = Path("/home/user/chatgpt-exporter/analysis_chunks")
    output_dir.mkdir(exist_ok=True, parents=True)

    conv_dir = output_dir / result['conversation_id']
    conv_dir.mkdir(exist_ok=True)

    # Save metadata
    with open(conv_dir / "metadata.json", 'w') as f:
        json.dump({
            "conversation_id": result['conversation_id'],
            "title": result['title'],
            "created_at": result['created_at'],
            "total_messages": result['total_messages'],
            "total_chunks": len(result['chunks'])
        }, f, indent=2)

    # Save each chunk
    for i, chunk in enumerate(result['chunks'], 1):
        chunk_file = conv_dir / f"chunk_{i:02d}.txt"
        with open(chunk_file, 'w') as f:
            f.write(chunk)

    print(f"✅ Saved to: {conv_dir}")
    print(f"\nTo analyze, read:")
    for i in range(1, len(result['chunks']) + 1):
        print(f"  {conv_dir}/chunk_{i:02d}.txt")
