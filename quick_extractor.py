#!/usr/bin/env python3
"""
Quick conversation extractor for manual review
Extracts key information from selected conversations
"""

import json
from pathlib import Path
from datetime import datetime


def analyze_conversation(filepath):
    """Extract key information from a conversation"""

    with open(filepath, 'r') as f:
        data = json.load(f)

    # Basic info
    info = {
        'id': data.get('id', Path(filepath).stem),
        'title': data.get('title', 'Untitled'),
        'date': data.get('created_at', 'Unknown'),
        'source': data.get('source', 'Unknown'),
        'message_count': data.get('message_count', 0),
        'messages': data.get('messages', [])
    }

    # Count messages by role
    user_messages = [m for m in info['messages'] if m.get('role') == 'user']
    assistant_messages = [m for m in info['messages'] if m.get('role') == 'assistant']

    info['user_count'] = len(user_messages)
    info['assistant_count'] = len(assistant_messages)

    # Extract substantive user inputs (>100 words)
    substantive_inputs = []
    for msg in user_messages:
        content = msg.get('content', '')
        word_count = len(content.split())
        if word_count > 100:
            substantive_inputs.append({
                'content': content,
                'word_count': word_count
            })

    info['substantive_inputs'] = substantive_inputs

    # Extract user questions
    questions = []
    for msg in user_messages:
        content = msg.get('content', '')
        if '?' in content:
            # Extract sentences with questions
            sentences = content.split('.')
            for sent in sentences:
                if '?' in sent:
                    questions.append(sent.strip())

    info['questions'] = questions

    # Look for projects mentioned (common project names)
    project_keywords = ['bloom', 'gemsi', 'flybrary', 'nurcoop', 'nur', 'impact nexus',
                        'growth compass', 'beit al atlas', 'cvreport']
    projects_mentioned = []

    all_text = ' '.join([m.get('content', '') for m in info['messages']]).lower()
    for keyword in project_keywords:
        if keyword in all_text:
            projects_mentioned.append(keyword)

    info['projects_mentioned'] = projects_mentioned

    # Look for domain tags
    domains = []
    domain_keywords = {
        'education': ['education', 'learning', 'teaching', 'curriculum', 'pedagogy'],
        'entrepreneurship': ['entrepreneur', 'startup', 'business', 'enterprise'],
        'technology': ['code', 'programming', 'software', 'app', 'web', 'ai'],
        'social_impact': ['social impact', 'nonprofit', 'ngo', 'community'],
        'philosophy': ['philosophy', 'meaning', 'values', 'purpose', 'ethics']
    }

    for domain, keywords in domain_keywords.items():
        for keyword in keywords:
            if keyword in all_text:
                domains.append(domain)
                break

    info['domains'] = list(set(domains))

    return info


def main():
    # Read the batch file list
    with open('random_batch_files.txt', 'r') as f:
        files = [line.strip() for line in f.readlines()]

    print("📊 RANDOM BATCH EXTRACTION REPORT")
    print("=" * 80)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total conversations: {len(files)}")
    print("=" * 80)

    all_analyses = []

    for i, filepath in enumerate(files, 1):
        print(f"\n{'='*80}")
        print(f"CONVERSATION {i}: {Path(filepath).name}")
        print('='*80)

        try:
            analysis = analyze_conversation(filepath)
            all_analyses.append(analysis)

            print(f"Title: {analysis['title']}")
            print(f"Date: {analysis['date']}")
            print(f"Source: {analysis['source']}")
            print(f"Messages: {analysis['message_count']} (User: {analysis['user_count']}, Assistant: {analysis['assistant_count']})")
            print(f"Substantive inputs (>100 words): {len(analysis['substantive_inputs'])}")
            print(f"Questions: {len(analysis['questions'])}")
            print(f"Projects mentioned: {', '.join(analysis['projects_mentioned']) if analysis['projects_mentioned'] else 'None'}")
            print(f"Domains: {', '.join(analysis['domains']) if analysis['domains'] else 'None'}")

            # Show first substantive input
            if analysis['substantive_inputs']:
                print(f"\n📝 First substantive input ({analysis['substantive_inputs'][0]['word_count']} words):")
                print(analysis['substantive_inputs'][0]['content'][:400] + '...')

            # Show sample questions
            if analysis['questions']:
                print(f"\n❓ Sample questions:")
                for q in analysis['questions'][:3]:
                    print(f"  - {q[:150]}...")

        except Exception as e:
            print(f"❌ Error analyzing: {e}")

    # Save full analysis
    output_file = f"random_batch_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'total_conversations': len(all_analyses),
            'analyses': all_analyses
        }, f, indent=2)

    print(f"\n\n💾 Full analysis saved to: {output_file}")

    # Summary statistics
    print("\n" + "="*80)
    print("BATCH SUMMARY")
    print("="*80)
    total_substantive = sum(len(a['substantive_inputs']) for a in all_analyses)
    total_questions = sum(len(a['questions']) for a in all_analyses)
    total_user_msgs = sum(a['user_count'] for a in all_analyses)

    print(f"Total user messages: {total_user_msgs}")
    print(f"Total substantive inputs (>100 words): {total_substantive}")
    print(f"Total questions: {total_questions}")

    # Domain distribution
    all_domains = {}
    for analysis in all_analyses:
        for domain in analysis['domains']:
            all_domains[domain] = all_domains.get(domain, 0) + 1

    print(f"\nDomain distribution:")
    for domain, count in sorted(all_domains.items(), key=lambda x: x[1], reverse=True):
        print(f"  {domain}: {count}")

    # Project mentions
    all_projects = {}
    for analysis in all_analyses:
        for project in analysis['projects_mentioned']:
            all_projects[project] = all_projects.get(project, 0) + 1

    if all_projects:
        print(f"\nProject mentions:")
        for project, count in sorted(all_projects.items(), key=lambda x: x[1], reverse=True):
            print(f"  {project}: {count}")

if __name__ == '__main__':
    main()
