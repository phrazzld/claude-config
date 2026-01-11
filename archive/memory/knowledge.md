# Code Patterns

### SSE Parsing and Event Handling
- **useSSEChat Hook**: Generic SSE management with dual-stream support (GET/POST) and event buffering
- **SSE Event Processing**: Manual line-by-line parsing with `event:` and `data:` prefix detection
- **Tool Result Structures**: Centralized `ToolResult` interface with typed tool-specific data schemas
- **Event Bus Integration**: SSE events map to eventBus types through SSEAdapter for cross-component communication

### Tool Result Type Patterns
- **Server ToolResult Interface**: Defined in `/app/.server/ai/client.ts` with optional tool-specific data properties
- **Client Event Schemas**: Zod validation schemas in `/app/lib/voltagent/schemas.ts` for type safety
- **SSE-to-EventBus Mapping**: Structured transformation from SSE events to typed eventBus payloads
- **Multi-Tool Support**: Navigation, form updates, store updates, and content manipulation tool results

### Behavioral Analytics Schema Design
- **Progressive Enhancement Pattern**: Optional nullable fields enable gradual feature rollout without breaking changes
- **Composite Objects Pattern**: Group related metrics (confidence, deviceContext, responsePattern) to reduce schema complexity
- **Behavioral Signal Richness**: Current 7-field interaction tracking can expand to 30+ signals (hesitation, answer changes, session patterns)
- **Time-Based Learning Insights**: Performance varies significantly by time of day and session length
- **Device Context Impact**: Screen size, input method, and device type significantly affect learning performance

### Learning Analytics Implementation Insights
- **Confidence vs Correctness Gap**: Lucky guesses vs genuine knowledge require separate tracking mechanisms
- **Response Pattern Analysis**: Hesitation time, answer changes, and interaction sequences reveal cognitive uncertainty
- **Spaced Repetition Enhancement**: Behavioral data improves FSRS algorithm accuracy beyond simple correct/incorrect
- **Privacy-First Design**: Anonymize behavioral patterns while preserving learning insights

### FFmpeg Audio Processing Patterns
- **Basic Concat Protocol**: Simple `ffmpeg().input("concat:" + filenames.join("|")).audioCodec("copy")` for quick file merging
- **Filter Complex Superiority**: `filter_complex` with `concat=n=X:v=0:a=1` provides better quality than basic concat protocol
- **Fluent-FFmpeg Integration**: Uses fluent-ffmpeg v2.1.2 wrapper with method chaining for FFmpeg operations
- **Timestamp-Based File Management**: Structured naming `${timestamp}-0${i}-segment.mp3` with sequential processing
- **Audio Quality Enhancement**: libmp3lame codec with 128k bitrate for consistent output quality vs copy codec
- **Error Handling with Cleanup**: `.on("error")` and `.on("end")` event handlers with Firebase upload and file cleanup
- **Temporary File Lifecycle**: Create in `./public/episodes/`, process, upload to Firebase Storage, then cleanup
- **Sequential Audio Generation**: ElevenLabs TTS → file write → FFmpeg concatenation → cleanup pipeline pattern

### Authentication Session Debugging Patterns
- **Cross-Environment Contamination**: Sessions created in dev/preview/production environments rejected in others due to environment mismatch
- **Dual Storage Desynchronization**: localStorage and cookie session tokens can fall out of sync causing persistent stale authentication
- **Silent Authentication Failures**: Functions returning null instead of throwing expected errors mask real issues
- **Environment-Aware Validation**: Development environments need more lenient session validation than production
- **Token Format Validation**: Pre-validate token structure before expensive database lookups to catch malformed tokens
- **Client-Side Session Cleanup**: Automatically clear expired tokens from both localStorage and cookies
- **Polling Query Amplification**: Authentication failures are exacerbated by frequent polling queries hitting auth endpoints
- **Error Message Enhancement**: Include detailed expiration information and environment context in auth error messages

### Multi-Agent Debugging Effectiveness
- **Parallel Subagent Analysis**: Integration detective (88% confidence) + bug historian + process eliminator provided comprehensive coverage
- **Historical Pattern Recognition**: Recurring cross-environment issues identified through pattern analysis
- **Integration Gap Analysis**: Dual storage synchronization gaps detected through system integration lens
- **Time-to-Resolution**: 15 minutes from parallel analysis to implemented fix demonstrates technique effectiveness
- **Hypothesis Strengthening**: Process of elimination validated primary cause while ruling out red herrings