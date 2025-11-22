#!/usr/bin/env node

/**
 * ChatGPT Insights Analyzer - CLI
 *
 * Analyzes exported ChatGPT conversations with checkpoint/resume support
 */

import fs from 'fs';
import path from 'path';
import { program } from 'commander';
import chalk from 'chalk';
import ora from 'ora';
import cliProgress from 'cli-progress';
import Anthropic from '@anthropic-ai/sdk';

const CHECKPOINT_FILE = '.analyzer-checkpoint.json';

// ============================================================================
// Helpers
// ============================================================================

function loadConversations(filePath) {
    const content = fs.readFileSync(filePath, 'utf-8');
    const data = JSON.parse(content);

    // Handle different export formats
    if (Array.isArray(data)) {
        return data;
    } else if (data.conversations) {
        return data.conversations;
    } else {
        throw new Error('Unknown conversations format');
    }
}

function loadCheckpoint() {
    if (fs.existsSync(CHECKPOINT_FILE)) {
        return JSON.parse(fs.readFileSync(CHECKPOINT_FILE, 'utf-8'));
    }
    return {
        processedIds: [],
        knowledgeBase: {
            meta: {
                version: '1.0.0',
                namespace: 'chatgpt-insights',
                last_updated: new Date().toISOString(),
                conversations_analyzed: 0,
                total_entities: 0,
                total_events: 0,
            },
            entities: {},
            relationships: [],
            temporal_chains: [],
            indexes: {
                by_type: {},
                by_conversation: {},
                by_date: {},
                by_tag: {},
                by_concept: {},
            },
        },
        totalCost: 0,
    };
}

function saveCheckpoint(checkpoint) {
    fs.writeFileSync(CHECKPOINT_FILE, JSON.stringify(checkpoint, null, 2));
}

function saveKnowledgeBase(kb, outputPath) {
    fs.writeFileSync(outputPath, JSON.stringify(kb, null, 2));
}

// ============================================================================
// Conversation Parsing (copied from chunker.ts)
// ============================================================================

function extractMessageText(message) {
    if (!message || !message.content) return '';
    const content = message.content;

    if (typeof content === 'string') return content;

    if (Array.isArray(content)) {
        return content
            .filter(part => part?.content_type === 'text')
            .map(part => part?.parts?.join('') || '')
            .join('\n');
    }

    if (content.parts) {
        return Array.isArray(content.parts) ? content.parts.join('') : String(content.parts);
    }

    return String(content);
}

function parseConversationTurns(conversation) {
    const turns = [];
    const mapping = conversation.mapping;
    const currentNodeId = conversation.current_node;

    if (!currentNodeId) return turns;

    // Build path
    const path = [];
    let nodeId = currentNodeId;
    while (nodeId) {
        path.unshift(nodeId);
        const node = mapping[nodeId];
        nodeId = node?.parent || null;
    }

    // Convert to turns
    let turnNumber = 0;
    for (const id of path) {
        const node = mapping[id];
        if (!node || !node.message) continue;

        const message = node.message;
        const content = extractMessageText(message);
        if (!content.trim()) continue;

        const role = message.author?.role;
        if (role !== 'user' && role !== 'assistant') continue;

        turns.push({
            turn_number: turnNumber,
            timestamp: message.create_time
                ? new Date(message.create_time * 1000).toISOString()
                : new Date().toISOString(),
            speaker: role,
            content,
        });

        turnNumber++;
    }

    return turns;
}

function chunkConversation(conversationId, conversationTitle, turns, turnsPerChunk = 10, overlapTurns = 2) {
    const chunks = [];
    if (turns.length === 0) return chunks;

    let chunkIndex = 0;
    let startIdx = 0;

    while (startIdx < turns.length) {
        const endIdx = Math.min(startIdx + turnsPerChunk, turns.length);
        const chunkTurns = turns.slice(startIdx, endIdx);

        chunks.push({
            conversation_id: conversationId,
            conversation_title: conversationTitle,
            chunk_index: chunkIndex,
            total_chunks: 0,
            turn_range: [chunkTurns[0].turn_number, chunkTurns[chunkTurns.length - 1].turn_number],
            turns: chunkTurns,
            has_overlap: startIdx > 0,
        });

        startIdx += turnsPerChunk - overlapTurns;
        chunkIndex++;

        if (startIdx === (startIdx + turnsPerChunk - overlapTurns)) break;
    }

    chunks.forEach(chunk => chunk.total_chunks = chunks.length);
    return chunks;
}

// ============================================================================
// Analysis Functions
// ============================================================================

function formatChunkForPrompt(chunk) {
    let text = '';
    for (const turn of chunk.turns) {
        const speaker = turn.speaker.toUpperCase();
        text += `[Turn ${turn.turn_number}] ${speaker}: ${turn.content}\n\n`;
    }
    return text;
}

const SYSTEM_PROMPT = `You are an expert conversation analyst specializing in extracting structured insights from human-AI dialogues.

Your task is to analyze conversation chunks and extract specific types of events, insights, and patterns while ALWAYS providing evidence (exact quotes) from the source conversation.

Key principles:
1. Evidence-based: Every insight must be grounded in actual conversation text
2. Precise quotes: Include exact quotes with turn numbers
3. Contextual: Understand the flow and progression of ideas
4. Structured output: Always return valid JSON matching the requested schema
5. Conservative: Only extract insights you're confident about (confidence > 0.7)

Return JSON only, no markdown code blocks.`;

function createEventExtractionPrompt(chunk) {
    return `Analyze this conversation chunk and extract ALL significant events.

For each event, provide:
- type: Event type (aha_moment, question_asked, decision_made, assumption_stated, problem_identified, solution_proposed, creative_prompt, uncertainty, discovery)
- turn_number: Which turn it occurred in
- speaker: "user" or "assistant"
- content: Brief description
- quote: EXACT quote (2-3 sentences max)
- context: Why this is significant
- confidence: 0.0-1.0
- tags: Relevant tags

Return JSON: {"events": [...]}

CONVERSATION:
${formatChunkForPrompt(chunk)}`;
}

async function analyzeChunk(client, chunk) {
    const prompt = createEventExtractionPrompt(chunk);

    const response = await client.messages.create({
        model: 'claude-haiku-4-20250514',
        max_tokens: 4096,
        temperature: 0.0,
        system: SYSTEM_PROMPT,
        messages: [{ role: 'user', content: prompt }],
    });

    const text = response.content[0].text;
    const cleanText = text.replace(/```json\n?/g, '').replace(/```\n?/g, '').trim();
    const data = JSON.parse(cleanText);

    // Convert to full Event objects
    const events = (data.events || []).map((e, idx) => ({
        id: `evt_${chunk.conversation_id}_${chunk.chunk_index}_${idx}`,
        type: 'event',
        subtype: e.type,
        conversation_id: chunk.conversation_id,
        conversation_title: chunk.conversation_title,
        turn_number: e.turn_number,
        turn_timestamp: chunk.turns[e.turn_number]?.timestamp || new Date().toISOString(),
        content: e.content,
        evidence: [{
            quote: e.quote,
            speaker: e.speaker,
            turn_number: e.turn_number,
            turn_timestamp: chunk.turns[e.turn_number]?.timestamp || new Date().toISOString(),
            conversation_id: chunk.conversation_id,
        }],
        related_entities: [],
        created_at: new Date().toISOString(),
        tags: e.tags || [],
        confidence: e.confidence || 0.8,
    }));

    return {
        events,
        usage: response.usage,
    };
}

async function analyzeConversation(client, conversation, progressBar) {
    const conversationId = conversation.id || conversation.conversation_id;
    const conversationTitle = conversation.title || 'Untitled';

    const turns = parseConversationTurns(conversation);
    const chunks = chunkConversation(conversationId, conversationTitle, turns);

    if (chunks.length === 0) {
        return { events: [], cost: 0 };
    }

    const allEvents = [];
    let totalInputTokens = 0;
    let totalOutputTokens = 0;

    for (const chunk of chunks) {
        const result = await analyzeChunk(client, chunk);
        allEvents.push(...result.events);
        totalInputTokens += result.usage.input_tokens;
        totalOutputTokens += result.usage.output_tokens;

        if (progressBar) {
            progressBar.increment();
        }
    }

    // Calculate cost ($1/$5 per million tokens)
    const cost = (totalInputTokens / 1_000_000) * 1.0 + (totalOutputTokens / 1_000_000) * 5.0;

    return {
        events: allEvents,
        cost,
        chunks_processed: chunks.length,
    };
}

// ============================================================================
// Main CLI
// ============================================================================

program
    .name('chatgpt-analyze')
    .description('Analyze ChatGPT conversation exports with Claude Haiku 4.5')
    .version('1.0.0');

program
    .command('analyze')
    .description('Analyze conversations from exported JSON file')
    .requiredOption('-i, --input <file>', 'Input JSON file (exported conversations)')
    .requiredOption('-k, --api-key <key>', 'Anthropic API key')
    .option('-o, --output <file>', 'Output knowledge base file', 'knowledge-base.json')
    .option('-b, --batch-size <number>', 'Conversations per batch', '50')
    .option('--resume', 'Resume from checkpoint')
    .option('--no-checkpoint', 'Disable checkpoints')
    .action(async (options) => {
        const spinner = ora();

        try {
            // Load conversations
            spinner.start('Loading conversations...');
            const conversations = loadConversations(options.input);
            spinner.succeed(`Loaded ${conversations.length} conversations`);

            // Load checkpoint if resuming
            let checkpoint = options.resume ? loadCheckpoint() : {
                processedIds: [],
                knowledgeBase: {
                    meta: {
                        version: '1.0.0',
                        namespace: 'chatgpt-insights',
                        last_updated: new Date().toISOString(),
                        conversations_analyzed: 0,
                        total_entities: 0,
                        total_events: 0,
                    },
                    entities: {},
                    relationships: [],
                    temporal_chains: [],
                    indexes: { by_type: {}, by_conversation: {}, by_date: {}, by_tag: {}, by_concept: {} },
                },
                totalCost: 0,
            };

            if (options.resume && checkpoint.processedIds.length > 0) {
                console.log(chalk.yellow(`Resuming from checkpoint: ${checkpoint.processedIds.length} already processed`));
            }

            // Filter out already processed
            const toProcess = conversations.filter(c => {
                const id = c.id || c.conversation_id;
                return !checkpoint.processedIds.includes(id);
            });

            if (toProcess.length === 0) {
                console.log(chalk.green('All conversations already processed!'));
                return;
            }

            console.log(chalk.blue(`\nProcessing ${toProcess.length} conversations...`));
            console.log(chalk.gray(`Batch size: ${options.batchSize}`));
            console.log(chalk.gray(`Checkpoint: ${options.checkpoint ? 'Enabled' : 'Disabled'}\n`));

            // Initialize Anthropic client
            const client = new Anthropic({ apiKey: options.apiKey });

            // Create progress bar
            const progressBar = new cliProgress.SingleBar({
                format: 'Progress |' + chalk.cyan('{bar}') + '| {percentage}% | {value}/{total} | Cost: ${cost} | ETA: {eta}s',
                barCompleteChar: '\u2588',
                barIncompleteChar: '\u2591',
                hideCursor: true,
            });

            // Estimate total chunks
            let totalChunks = 0;
            for (const conv of toProcess) {
                const turns = parseConversationTurns(conv);
                const chunks = chunkConversation(conv.id, conv.title || 'Untitled', turns);
                totalChunks += chunks.length;
            }

            progressBar.start(totalChunks, 0, { cost: checkpoint.totalCost.toFixed(4) });

            // Process conversations
            let processed = 0;
            for (const conversation of toProcess) {
                const conversationId = conversation.id || conversation.conversation_id;

                try {
                    const result = await analyzeConversation(client, conversation, progressBar);

                    // Add events to knowledge base
                    for (const event of result.events) {
                        checkpoint.knowledgeBase.entities[event.id] = event;

                        // Update indexes
                        if (!checkpoint.knowledgeBase.indexes.by_type.event) {
                            checkpoint.knowledgeBase.indexes.by_type.event = [];
                        }
                        checkpoint.knowledgeBase.indexes.by_type.event.push(event.id);
                    }

                    checkpoint.totalCost += result.cost;
                    checkpoint.processedIds.push(conversationId);
                    checkpoint.knowledgeBase.meta.conversations_analyzed++;
                    checkpoint.knowledgeBase.meta.total_events += result.events.length;
                    checkpoint.knowledgeBase.meta.total_entities = Object.keys(checkpoint.knowledgeBase.entities).length;
                    checkpoint.knowledgeBase.meta.last_updated = new Date().toISOString();

                    progressBar.update(progressBar.value, { cost: checkpoint.totalCost.toFixed(4) });

                    processed++;

                    // Save checkpoint every N conversations
                    if (options.checkpoint && processed % parseInt(options.batchSize) === 0) {
                        saveCheckpoint(checkpoint);
                    }

                } catch (error) {
                    console.error(chalk.red(`\nError processing ${conversationId}: ${error.message}`));
                    // Continue with next conversation
                }
            }

            progressBar.stop();

            // Save final knowledge base
            saveKnowledgeBase(checkpoint.knowledgeBase, options.output);

            // Clean up checkpoint
            if (options.checkpoint && fs.existsSync(CHECKPOINT_FILE)) {
                fs.unlinkSync(CHECKPOINT_FILE);
            }

            // Summary
            console.log(chalk.green('\n✓ Analysis complete!\n'));
            console.log(chalk.blue('Summary:'));
            console.log(`  Conversations analyzed: ${checkpoint.knowledgeBase.meta.conversations_analyzed}`);
            console.log(`  Total events extracted: ${checkpoint.knowledgeBase.meta.total_events}`);
            console.log(`  Total cost: $${checkpoint.totalCost.toFixed(4)}`);
            console.log(`  Output saved to: ${chalk.cyan(options.output)}\n`);

        } catch (error) {
            spinner.fail('Analysis failed');
            console.error(chalk.red(error.message));
            process.exit(1);
        }
    });

program
    .command('resume')
    .description('Resume from last checkpoint')
    .requiredOption('-i, --input <file>', 'Input JSON file')
    .requiredOption('-k, --api-key <key>', 'Anthropic API key')
    .option('-o, --output <file>', 'Output file', 'knowledge-base.json')
    .action((options) => {
        if (!fs.existsSync(CHECKPOINT_FILE)) {
            console.log(chalk.yellow('No checkpoint found. Use "analyze" command instead.'));
            process.exit(1);
        }

        // Run analyze with --resume flag
        program.parse(['node', 'cli.js', 'analyze', '-i', options.input, '-k', options.apiKey, '-o', options.output, '--resume']);
    });

program
    .command('stats')
    .description('Show statistics from checkpoint or knowledge base')
    .argument('[file]', 'Knowledge base JSON file', 'knowledge-base.json')
    .action((file) => {
        if (fs.existsSync(CHECKPOINT_FILE)) {
            const checkpoint = loadCheckpoint();
            console.log(chalk.blue('\nCheckpoint Statistics:\n'));
            console.log(`  Processed: ${checkpoint.processedIds.length} conversations`);
            console.log(`  Total events: ${checkpoint.knowledgeBase.meta.total_events}`);
            console.log(`  Total cost: $${checkpoint.totalCost.toFixed(4)}\n`);
        } else if (fs.existsSync(file)) {
            const kb = JSON.parse(fs.readFileSync(file, 'utf-8'));
            console.log(chalk.blue('\nKnowledge Base Statistics:\n'));
            console.log(`  Conversations: ${kb.meta.conversations_analyzed}`);
            console.log(`  Total entities: ${kb.meta.total_entities}`);
            console.log(`  Total events: ${kb.meta.total_events}`);
            console.log(`  Last updated: ${new Date(kb.meta.last_updated).toLocaleString()}\n`);
        } else {
            console.log(chalk.yellow('No checkpoint or knowledge base found.'));
        }
    });

program.parse();
