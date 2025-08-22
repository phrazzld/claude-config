#!/bin/bash

# Claude Code Statusline Script
# Shows current model and time remaining in Claude Code block

# Read JSON input from Claude Code statusline system
INPUT=$(cat)

# Initialize variables
MODEL=""
TIME_REMAINING=""

# Handle empty or invalid input
if [ -z "$INPUT" ]; then
    echo "◉ no-input | ⏰ --"
    exit 0
fi

# Parse model from input JSON - try display_name first, then id, then model
if command -v jq >/dev/null 2>&1; then
    # Try display_name first (e.g. "Sonnet 4")
    MODEL=$(echo "$INPUT" | jq -r '.display_name // .id // .model // "unknown"' 2>/dev/null)
    # Validate that we got a proper model name
    if [ -z "$MODEL" ] || [ "$MODEL" = "null" ]; then
        MODEL="unknown"
    else
        # Clean up model name for display - extract key part
        case "$MODEL" in
            *"Sonnet"*) MODEL="sonnet" ;;
            *"Opus"*) MODEL="opus" ;;
            *"Haiku"*) MODEL="haiku" ;;
            *) 
                # Fallback: remove prefixes and clean up
                MODEL=$(echo "$MODEL" | sed 's/claude-//' | sed 's/-.*$//' | tr '[:upper:]' '[:lower:]')
                ;;
        esac
    fi
else
    MODEL="unknown"
fi

# Get time remaining from ccusage
if command -v ccusage >/dev/null 2>&1 && command -v jq >/dev/null 2>&1; then
    CCUSAGE_OUTPUT=$(ccusage blocks --active --json 2>/dev/null)
    if [ $? -eq 0 ] && [ -n "$CCUSAGE_OUTPUT" ]; then
        REMAINING_MINUTES=$(echo "$CCUSAGE_OUTPUT" | jq -r '.blocks[0].projection.remainingMinutes // null' 2>/dev/null)
        if [ "$REMAINING_MINUTES" != "null" ] && [ -n "$REMAINING_MINUTES" ]; then
            # Convert minutes to hours:minutes format
            HOURS=$((REMAINING_MINUTES / 60))
            MINS=$((REMAINING_MINUTES % 60))
            
            if [ $HOURS -gt 0 ]; then
                TIME_REMAINING="${HOURS}h ${MINS}m"
            else
                TIME_REMAINING="${MINS}m"
            fi
        else
            TIME_REMAINING="--"
        fi
    else
        TIME_REMAINING="--"
    fi
else
    TIME_REMAINING="--"
fi

# Format and output statusline with visual enhancements  
if [ "$TIME_REMAINING" != "--" ]; then
    TIME_DISPLAY="⏰ $TIME_REMAINING remaining"
else
    TIME_DISPLAY="⏰ --"
fi

# Output only the final statusline - nothing else
printf "◉ %s | %s\n" "$MODEL" "$TIME_DISPLAY"