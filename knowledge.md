# Superwire Codebase Patterns

## Notification & External Integration Patterns

### HTTP Request Patterns
**File: `/Users/phaedrus/Development/superwire/src/lib/openrouter.ts:90-100`**
```typescript
const response = await fetch(`${OPENROUTER_API_BASE}/chat/completions`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${this.apiKey}`,
    'HTTP-Referer': process.env.SITE_URL || 'http://localhost:3000',
    'X-Title': 'Superwire News',
  },
  body: JSON.stringify(request),
});
```
- Uses native `fetch()` API with proper headers
- Bearer token authentication pattern
- JSON body serialization
- Custom headers for API identification

**File: `/Users/phaedrus/Development/superwire/src/lib/elevenlabs.ts:438-442`**
```typescript
const response = await fetch(endpoint, {
  method: 'POST',
  headers: requestHeaders,
  body: JSON.stringify(requestBody)
});
```

### Environment Variable Patterns
**Pattern: `process.env.API_KEY_NAME`**
- `OPENROUTER_API_KEY` - OpenRouter API access
- `ELEVEN_LABS_API_KEY` - ElevenLabs TTS service  
- `NEWS_API_KEY` - News API access
- `GOOGLE_SERVICE_KEY` - Base64 encoded Firebase service account
- `NEXT_PUBLIC_CONVEX_URL` - Convex database URL
- `SITE_URL` - Application URL for referrer headers
- `CRON_SECRET` - Bearer token for cron endpoint security

**File: `/Users/phaedrus/Development/superwire/src/lib/openrouter.ts:69`**
```typescript
this.apiKey = apiKey || process.env.OPENROUTER_API_KEY || '';
```

**File: `/Users/phaedrus/Development/superwire/src/lib/elevenlabs.ts:405`**
```typescript
const apiKey = process.env.ELEVEN_LABS_API_KEY;
```

### Error Handling Patterns
**Comprehensive Error Handler: `/Users/phaedrus/Development/superwire/src/lib/error-handler.ts`**

**EnhancedError Class:**
```typescript
export class EnhancedError extends Error {
  public readonly category: ErrorCategory;
  public readonly statusCode?: number;
  public readonly attempt: number;
  public readonly context: Record<string, any>;
  public readonly originalError?: Error;
  public readonly isRetryable: boolean;
}
```

**Error Categories:**
```typescript
export enum ErrorCategory {
  TIMEOUT = 'timeout',
  RATE_LIMIT = 'rate_limit', 
  AUTHENTICATION = 'authentication',
  NETWORK = 'network',
  API_ERROR = 'api_error',
  VALIDATION = 'validation',
  QUOTA_EXCEEDED = 'quota_exceeded',
  UNKNOWN = 'unknown'
}
```

**Retry Pattern with Exponential Backoff:**
```typescript
export const DEFAULT_RETRY_OPTIONS = {
  maxAttempts: 3,
  backoffStrategy: 'exponential',
  delayMs: [1000, 2000, 4000], // 1s, 2s, 4s
  timeoutMs: 30000,
  retryIf: (error: EnhancedError) => error.isRetryable,
  onRetry: (error: EnhancedError, attempt: number) => {
    console.warn(`⚠️ Retry attempt ${attempt} after error: ${error.message}`);
  }
};
```

### Error Reporting Patterns
**File: `/Users/phaedrus/Development/superwire/pages/api/episodes.ts:134-138`**
```typescript
} catch (error: any) {
  console.error(`Error writing intro: ${error.message}`);
  retries++;
  await new Promise((resolve) => setTimeout(resolve, RETRY_DELAY));
}
```

**Consistent Error Logging:**
- `console.error()` for errors
- `console.warn()` for warnings  
- `console.log()` for info/success
- Structured error context with operation details

### Authentication Patterns
**Bearer Token Pattern:**
**File: `/Users/phaedrus/Development/superwire/src/app/api/cron/generate/route.ts:50-65`**
```typescript
function verifyBearerToken(request: Request): boolean {
  const cronSecret = process.env.CRON_SECRET;
  if (!cronSecret) {
    console.warn('CRON_SECRET not configured');
    return false;
  }
  
  const authHeader = request.headers.get('authorization');
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return false;
  }
  
  const token = authHeader.substring(7);
  return token === cronSecret;
}
```

### Cost Tracking Patterns
**File: `/Users/phaedrus/Development/superwire/src/lib/openrouter.ts:313-340`**
```typescript
export async function trackTokenUsage(
  model: string,
  inputTokens: number,
  outputTokens: number,
  options?: {
    taskType?: string;
    prompt?: string;
    costsFilePath?: string;
  }
): Promise<void> {
  // Cost tracking implementation
}
```

## Missing Notification Infrastructure

### Required for notifyFailure()
1. **SendGrid Integration** - No existing email patterns found
2. **Discord Webhook** - No existing webhook patterns found  
3. **Error Formatting** - Basic console.error() exists, needs structured formatting
4. **Notification Configuration** - Need environment variables for webhook URLs/API keys

### Existing HTTP Patterns Can Be Leveraged
- `fetch()` API calls with proper headers
- Bearer token authentication 
- JSON serialization/parsing
- Error handling with categorization
- Retry logic with exponential backoff
- Environment variable configuration

### Recommended Implementation Approach
1. **Environment Variables:**
   - `DISCORD_WEBHOOK_URL` for Discord notifications
   - `SENDGRID_API_KEY` and `SENDGRID_FROM_EMAIL` for email
   
2. **Error Context Formatting:**
   - Use existing `EnhancedError` class structure
   - Format error details with context, stack traces, and metadata
   
3. **HTTP Webhook Pattern:**
   - Follow OpenRouter/ElevenLabs fetch() pattern
   - Include proper error handling and retry logic
   - Use structured JSON payloads

4. **Integration Points:**
   - Add calls in existing catch blocks throughout codebase
   - Integrate with error-handler.ts retry wrapper
   - Include in cron job failure scenarios

## Key Architectural Insights
- **No existing notification infrastructure** - clean slate implementation needed
- **Strong error handling patterns** - can be extended for notifications
- **Consistent environment variable usage** - follow established naming conventions
- **Native fetch() preferred** - avoid additional HTTP libraries
- **Comprehensive retry logic** - leverage existing exponential backoff patterns

# Audio Processing Patterns in Superwire

## FFmpeg Integration Patterns

### Core Dependencies
- **fluent-ffmpeg**: `^2.1.2` - Main FFmpeg wrapper library
- **@types/fluent-ffmpeg**: `^2.1.20` - TypeScript definitions

### Current Audio Processing Pipeline (episodes.ts:686-788)

#### Basic Command Structure Pattern
```typescript
const ffmpegCommand = ffmpeg();

// Add multiple inputs
filenames.forEach((filename, index) => {
  ffmpegCommand.input(filename);
});

// Apply filter complex
ffmpegCommand
  .complexFilter([filterComplex])
  .map('[out]')
  .audioCodec('libmp3lame')
  .audioBitrate('128k')
  .audioFrequency(44100)
  .format('mp3')
  .on("start", (commandLine) => { console.log("FFmpeg command:", commandLine); })
  .on("end", async () => { /* completion handler */ })
  .on("error", (err) => { /* error handler */ })
  .on("progress", (progress) => { /* progress handler */ })
  .saveToFile(mergedFilename);
```

#### Filter Complex Generation Pattern
```typescript
// Build input mapping for concat filter
let inputMap = '';
filenames.forEach((filename, index) => {
  inputMap += `[${index}:a]`;
});

// Create concat filter: [0:a][1:a][2:a]concat=n=3:v=0:a=1[out]
const filterComplex = `${inputMap}concat=n=${filenames.length}:v=0:a=1[out]`;
```

### Error Handling Patterns

#### Nested Error Handling with Fallback
```typescript
.on("error", (err) => {
  console.error("Error merging files with filter_complex:", err);
  console.error("FFmpeg error details:", err.message);
  
  // Fallback to simple concatenation
  console.log("Falling back to simple concatenation...");
  ffmpeg()
    .input("concat:" + filenames.join("|"))
    .audioCodec("copy")
    .on("end", async () => { /* fallback success */ })
    .on("error", (fallbackErr) => console.error("Fallback merge also failed:", fallbackErr))
    .saveToFile(mergedFilename);
})
```

#### Progress Monitoring
```typescript
.on("progress", (progress) => {
  console.log(`Processing: ${Math.round(progress.percent || 0)}% done`);
})
```

### Temporary File Management Patterns

#### File Creation Pattern
```typescript
const timestamp = new Date().toISOString();
const filename = `${timestamp}-00-intro.mp3`;
const EPISODES_DIR = "./public/episodes";

fs.writeFile(`${EPISODES_DIR}/${filename}`, Buffer.from(audioData), (err) => {
  if (err) throw err;
  console.log("The audio file has been saved!");
});
```

#### File Cleanup Pattern (episodes.ts:738-756)
```typescript
// Delete all files in EPISODES_DIR after processing
fs.readdir(EPISODES_DIR, (err, files) => {
  if (err) {
    console.error("Error reading episodes directory for cleanup:", err);
    return;
  }

  files.forEach((file) => {
    const filePath = path.join(EPISODES_DIR, file);
    fs.unlink(filePath, (err) => {
      if (err) {
        console.error(`Error deleting file ${filePath}:`, err);
      } else {
        console.log(`Deleted file ${filePath}`);
      }
    });
  });
});
```

### Audio Quality Settings

#### Current Quality Configuration
- **Audio Codec**: `libmp3lame` (high-quality MP3 encoder)
- **Bitrate**: `128k` (podcast-quality)
- **Sample Rate**: `44100` Hz (standard)
- **Format**: `mp3`

### Advanced Audio Cache Management (elevenlabs.ts:918-1331)

#### Cache Directory Structure
```typescript
export const AUDIO_CACHE_DIR = 'tmp/audio_cache';
export const CACHE_MAX_AGE_HOURS = 24 * 7; // 1 week
export const CACHE_MAX_SIZE_MB = 100; // 100MB limit
```

#### Cache Entry Management
```typescript
interface AudioCacheEntry {
  filePath: string;
  textHash: string;
  voiceId: string;
  originalText: string;
  fileSize: number;
  createdAt: string;
  lastAccessed: string;
  hitCount: number;
  settings: {
    stability: number;
    similarityBoost: number;
  };
}
```

#### File Cleanup with Size Management
```typescript
cleanOldEntries(targetReductionMB: number = 20): void {
  // Sort by last accessed time (oldest first)
  const sortedEntries = metadata.entries.sort(
    (a, b) => new Date(a.lastAccessed).getTime() - new Date(b.lastAccessed).getTime()
  );

  let cleanedSizeBytes = 0;
  const targetBytes = targetReductionMB * 1024 * 1024;

  for (const entry of sortedEntries) {
    if (cleanedSizeBytes >= targetBytes) break;
    
    if (fs.existsSync(entry.filePath)) {
      fs.unlinkSync(entry.filePath);
    }
    cleanedSizeBytes += entry.fileSize;
  }
}
```

### Audio Validation Patterns (elevenlabs.ts:580-707)

#### Buffer Validation
```typescript
function validateAudio(buffer: Buffer, options: ValidationOptions): AudioValidationResult {
  const result: AudioValidationResult = {
    isValid: false,
    duration: null,
    format: null,
    sampleRate: null,
    channels: null,
    bitrate: null,
    issues: [],
    warnings: [],
    fileSize: buffer.length
  };

  // Basic buffer validation
  if (!buffer || buffer.length === 0) {
    result.issues.push('Empty or null audio buffer');
    return result;
  }

  if (buffer.length < 1024) {
    result.issues.push('Audio buffer too small (< 1KB), likely corrupted');
    return result;
  }

  // Format detection by magic bytes
  const formatInfo = detectAudioFormat(buffer);
  result.format = formatInfo.format;
  
  // Extract metadata and validate
  const metadata = extractAudioMetadata(buffer, formatInfo.format);
  result.duration = metadata.duration;
  result.sampleRate = metadata.sampleRate;
  result.channels = metadata.channels;
  result.bitrate = metadata.bitrate;

  result.isValid = result.issues.length === 0;
  return result;
}
```

## Integration Points for Audio Normalization

### 1. In Audio Generation Pipeline (elevenlabs.ts:324-533)
**Location**: After `generateAudioSegment()` and before caching
```typescript
// After successful audio generation
const audioBuffer = Buffer.from(await response.arrayBuffer());

// INTEGRATION POINT: Add normalization here
const normalizedBuffer = await normalizeAudio(audioBuffer);

// Continue with validation and caching
const validation = validateAudio(normalizedBuffer, options);
```

### 2. In Episode Recording Pipeline (episodes.ts:592-788)
**Location**: After individual segment generation, before FFmpeg concatenation
```typescript
// Process segments with normalization
for (let i = 0; i < segments.length; i++) {
  const segmentRes = await fetch(hostEndpoint, { /* TTS request */ });
  const segmentData = await segmentRes.arrayBuffer();
  
  // INTEGRATION POINT: Normalize each segment
  const normalizedSegment = await normalizeAudio(Buffer.from(segmentData));
  
  fs.writeFile(`${EPISODES_DIR}/${filename}`, normalizedSegment, callback);
}
```

### 3. During FFmpeg Processing (episodes.ts:698-787)
**Location**: In the filter complex chain, add loudnorm filter
```typescript
// Enhanced filter complex with normalization
const filterComplex = `${inputMap}concat=n=${filenames.length}:v=0:a=1[concat];[concat]loudnorm=I=-16:LRA=11:tp=-1.5[out]`;

ffmpegCommand
  .complexFilter([filterComplex])
  .map('[out]')
  // ... rest of configuration
```

## Recommended `normalizeAudio()` Implementation Pattern

### Function Signature
```typescript
export async function normalizeAudio(
  inputBuffer: Buffer,
  options: {
    targetLUFS?: number;      // Default: -16 LUFS (podcast standard)
    truePeak?: number;        // Default: -1.5 dBTP
    loudnessRange?: number;   // Default: 11 LU
    tempDir?: string;         // Default: 'tmp/audio_processing'
    cleanup?: boolean;        // Default: true
  } = {}
): Promise<Buffer>
```

### Implementation Pattern Following Existing Code Style
```typescript
export async function normalizeAudio(inputBuffer: Buffer, options = {}) {
  const {
    targetLUFS = -16,
    truePeak = -1.5, 
    loudnessRange = 11,
    tempDir = 'tmp/audio_processing',
    cleanup = true
  } = options;

  // Ensure temp directory exists (following cache pattern)
  if (!fs.existsSync(tempDir)) {
    fs.mkdirSync(tempDir, { recursive: true });
  }

  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const inputFile = path.join(tempDir, `input-${timestamp}.mp3`);
  const outputFile = path.join(tempDir, `normalized-${timestamp}.mp3`);

  try {
    // Write input buffer to temporary file
    fs.writeFileSync(inputFile, inputBuffer);

    // Two-pass loudnorm process
    return new Promise((resolve, reject) => {
      // Pass 1: Measure
      ffmpeg(inputFile)
        .audioFilters(`loudnorm=I=${targetLUFS}:LRA=${loudnessRange}:tp=${truePeak}:print_format=json`)
        .format('null')
        .on('start', (cmd) => console.log('FFmpeg loudnorm pass 1:', cmd))
        .on('stderr', (stderrLine) => {
          // Parse JSON output for measured values
          if (stderrLine.includes('"input_i"')) {
            const measured = parseLoudnormMeasurement(stderrLine);
            
            // Pass 2: Apply normalization with measured values
            ffmpeg(inputFile)
              .audioFilters(`loudnorm=I=${targetLUFS}:LRA=${loudnessRange}:tp=${truePeak}:measured_I=${measured.input_i}:measured_LRA=${measured.input_lra}:measured_tp=${measured.input_tp}:measured_thresh=${measured.input_thresh}:offset=${measured.target_offset}`)
              .audioCodec('libmp3lame')
              .audioBitrate('128k')
              .audioFrequency(44100)
              .on('end', () => {
                try {
                  const normalizedBuffer = fs.readFileSync(outputFile);
                  
                  if (cleanup) {
                    fs.unlinkSync(inputFile);
                    fs.unlinkSync(outputFile);
                  }
                  
                  resolve(normalizedBuffer);
                } catch (error) {
                  reject(error);
                }
              })
              .on('error', reject)
              .saveToFile(outputFile);
          }
        })
        .on('error', reject)
        .run();
    });

  } catch (error) {
    // Cleanup on error
    if (cleanup) {
      [inputFile, outputFile].forEach(file => {
        if (fs.existsSync(file)) fs.unlinkSync(file);
      });
    }
    throw error;
  }
}
```

This pattern follows Superwire's existing conventions for:
- Retry logic with exponential backoff
- Comprehensive error handling with fallbacks
- Progress monitoring and logging
- Temporary file management with cleanup
- TypeScript interfaces and validation
- Fluent-ffmpeg command building
- Firebase integration points

## Professional Audio Normalization Lessons (Implemented 2025-09-03)

### Implementation Success Patterns

#### Two-Pass Loudnorm Process (Critical for Professional Quality)
**Lesson**: Single-pass loudnorm is convenient but inaccurate. Professional audio requires two-pass processing:
1. **Analysis Pass**: Measure actual loudness characteristics of input audio
2. **Normalization Pass**: Apply measured values for precise normalization

```typescript
// WRONG: Single-pass (inaccurate)
.audioFilters('loudnorm=I=-16:LRA=11:tp=-1.5')

// RIGHT: Two-pass (professional)
// Pass 1: Measure
.audioFilters('loudnorm=I=-16:LRA=11:tp=-1.5:print_format=json')
.format('null')
// Pass 2: Apply with measured values
.audioFilters('loudnorm=I=-16:LRA=11:tp=-1.5:measured_I=...measured values...')
```

#### FFmpeg Stderr Analysis Parsing
**Critical Gotcha**: FFmpeg loudnorm outputs analysis JSON to **stderr**, not stdout
```typescript
.on('stderr', (stderrLine) => {
  // Look for JSON analysis data in stderr
  if (stderrLine.includes('"input_i"')) {
    const measured = JSON.parse(stderrLine);
    // Use measured values for pass 2
  }
})
```

#### Professional Podcast Standards
- **Podcast Standard**: -16 LUFS (NOT -23 LUFS which is broadcast standard)
- **True Peak**: -1.5 dBTP (prevents clipping)
- **Loudness Range**: 11 LU (maintains dynamic range)
- **Music Content**: -14 LUFS for podcast episodes with significant music

#### Resource Management for Batch Processing
**Pattern**: Implement delays between operations to prevent system overload
```typescript
// Process files with 500ms delays to prevent resource exhaustion
for (const file of audioFiles) {
  await normalizeAudio(file);
  await new Promise(resolve => setTimeout(resolve, 500));
}
```

### Integration Strategy Lessons

#### Multiple Integration Points Required
Professional audio processing needs different approaches at different pipeline stages:

1. **Individual File Processing**: Normalize each TTS-generated segment
2. **Batch Processing**: Normalize collections of files with resource management
3. **Final Master**: Normalize final concatenated episode with FFmpeg filter complex

#### Modular Design Benefits
**Success Pattern**: Separate audio utilities (audio.ts) from main pipeline logic
- Easier testing without actual audio files
- Reusable across different parts of application
- Clear separation of concerns

### Error Handling & Fallback Patterns

#### Comprehensive Error Recovery
```typescript
// Multi-level fallback strategy
try {
  return await twoPassNormalization(input, options);
} catch (twoPassError) {
  console.warn('Two-pass failed, trying single-pass:', twoPassError.message);
  try {
    return await singlePassNormalization(input, options);
  } catch (singlePassError) {
    console.error('All normalization failed, returning original:', singlePassError.message);
    return input; // Graceful degradation
  }
}
```

#### Temporary File Cleanup Critical
**Gotcha**: Professional audio files are large - missing cleanup causes disk space issues
```typescript
// Always cleanup in finally block or error handlers
const tempFiles = [inputFile, analysisFile, outputFile];
try {
  // processing...
} finally {
  if (cleanup) {
    tempFiles.forEach(file => {
      if (fs.existsSync(file)) fs.unlinkSync(file);
    });
  }
}
```

### Testing Strategy for Audio Processing

#### Mock-Based Testing Pattern
**Success**: Test audio processing logic without requiring actual audio files
```typescript
// Test the logic flow, not the actual audio processing
jest.mock('fluent-ffmpeg', () => ({
  __esModule: true,
  default: jest.fn().mockImplementation(() => mockFFmpegChain)
}));
```

#### Parameter Validation Testing
Focus on edge cases that could cause production issues:
- Invalid LUFS values (-70 to +5 range)
- Empty buffers and malformed audio
- File system permission errors
- FFmpeg command generation correctness

### Performance & Resource Insights

#### Time Estimates for Audio Normalization
- **Simple normalization**: 2-5 seconds per minute of audio
- **Two-pass professional**: 4-10 seconds per minute of audio
- **Batch processing**: Add 500ms delays between files
- **Implementation complexity**: Medium-High (30 minutes for complete solution)

#### Memory Management
- Process audio files individually, not in large batches
- Use streaming where possible for large files
- Monitor temp directory growth during batch operations

### Architecture Decision Outcomes

#### Why Two-Pass Over Single-Pass
**Decision**: Implement two-pass loudnorm despite complexity
**Reason**: Professional podcasting requires accurate loudness normalization. Single-pass is convenient but produces inconsistent results that fail podcast platform requirements.

#### Why Multiple Integration Points
**Decision**: Support individual file, batch, and FFmpeg filter integration
**Reason**: Different pipeline stages need different approaches. Individual processing for TTS segments, batch for collections, FFmpeg filters for final mastering.

#### Why Comprehensive Error Handling
**Decision**: Implement multi-level fallback strategy
**Reason**: Audio processing failures shouldn't break entire episode generation. Graceful degradation maintains user experience.

## React Testing & Conditional Rendering Patterns (AnyZine, 2025-09-05)

### Critical Testing Insights for Complex Components

#### Understanding Dynamic Component Architecture
**Key Insight**: Components with conditional rendering create different DOM structures that require different testing strategies.

**SubjectForm Architecture Pattern**:
```typescript
// Two completely different states with different DOM elements
return (!zineData && !loading && !error) ? (
  // Empty state: EmptyStateGrid + floating form + SubjectCarousel
  <div>
    <input data-testid="subject-input" />  // Different input element
    {/* No random button in empty state */}
  </div>
) : (
  // Standard state: regular form with input + random + create buttons  
  <div>
    <input data-testid="subject-input" />  // Different input element
    <button data-testid="random-button">Random</button>
  </div>
);
```

**Critical Testing Gotcha**: Same `data-testid` but different DOM elements require fresh queries after state transitions.

#### State-Aware Element Querying Pattern
**Problem**: Cached element references break when components re-render with different structures.

```typescript
// WRONG: Cached reference becomes stale after state change
const input = screen.getByTestId('subject-input');
fireEvent.click(randomButton);
// input is now stale - references old DOM element

// RIGHT: Re-query after state transitions
fireEvent.click(randomButton);
await waitFor(() => {
  const currentInput = screen.getByTestId('subject-input');
  expect(currentInput).toHaveValue('Artificial Intelligence');
});
```

#### Complex State Transition Testing
**Pattern**: Multi-step state changes require careful orchestration
```typescript
// SubjectForm random button behavior:
// 1. Click random -> 2. Populate input -> 3. Clear error -> 4. Transition to empty state

it('should handle random subject selection', async () => {
  // Start in empty state, transition to standard state
  fireEvent.change(screen.getByTestId('subject-input'), { 
    target: { value: 'test' } 
  });
  
  await waitFor(() => {
    expect(screen.getByTestId('random-button')).toBeInTheDocument();
  });
  
  // Click random button
  fireEvent.click(screen.getByTestId('random-button'));
  
  // Wait for state transition back to empty state
  await waitFor(() => {
    const currentInput = screen.getByTestId('subject-input');
    expect(currentInput.value).toBe('Artificial Intelligence'); // populated
    expect(screen.queryByTestId('random-button')).not.toBeInTheDocument(); // back to empty state
  });
});
```

### Test Pattern Discovery Strategy

#### Pattern-Scout Approach
**Success Pattern**: Mine existing codebase for testing patterns before writing new tests.

**Effective Search Strategy**:
1. Search for conditional rendering patterns: `screen.queryBy`, `not.toBeInTheDocument()`
2. Find state transition tests: `waitFor()`, `fireEvent`
3. Look for input interaction patterns: `fireEvent.change`, `fireEvent.click`
4. Identify accessibility test patterns: `toHaveAccessibleDescription`

**Grep Commands That Worked**:
```bash
# Find conditional rendering tests
grep -r "not.toBeInTheDocument" --include="*.test.*"

# Find input interaction patterns  
grep -r "fireEvent.change" --include="*.test.*"

# Find state transition patterns
grep -r "waitFor.*expect.*toBeInTheDocument" --include="*.test.*"
```

#### Systematic Test Fixing Approach
**Proven Order** (24 failures → 0 failures in 45 minutes):
1. **Fix Initial Render Tests**: Get basic component mounting working
2. **Fix Random Functionality**: Test core user interactions
3. **Fix Accessibility Tests**: Ensure proper ARIA attributes and descriptions
4. **Fix State Management**: Test complex state transitions and error handling

### Conditional Rendering Test Patterns

#### Element Absence Testing
**Pattern**: Use `queryBy*` for elements that may not exist, `getBy*` for elements that must exist.

```typescript
// Test element doesn't exist (conditional rendering)
expect(screen.queryByTestId('random-button')).not.toBeInTheDocument();

// Test element exists (required element)
expect(screen.getByTestId('subject-input')).toBeInTheDocument();
```

#### State-Dependent Accessibility Testing
**Pattern**: Accessibility attributes change based on component state.

```typescript
// Empty state: input has no accessible description
const emptyInput = screen.getByTestId('subject-input');
expect(emptyInput).not.toHaveAccessibleDescription();

// Standard state: input has error-related accessible description
fireEvent.change(emptyInput, { target: { value: 'test' } });
const standardInput = await screen.findByTestId('subject-input');  
expect(standardInput).toHaveAccessibleDescription('Enter a subject for your zine');
```

### Advanced React Testing Insights

#### When to Use Different Query Methods
- **`getBy*`**: Element must exist (test fails if not found)
- **`queryBy*`**: Element might not exist (returns null if not found) 
- **`findBy*`**: Element will exist after async operation (waits for element)

#### Handling Component Re-renders
**Key Insight**: Components with conditional rendering essentially create new component instances.
- Don't cache DOM element references across state changes
- Re-query elements after any state transition that could change DOM structure
- Use `waitFor()` to handle async state updates

#### Error State Testing Strategy
**Pattern**: Test error clearing behavior, not just error display.

```typescript
// Test error clearing on random button click
const mockError = 'Test error message';
render(<SubjectForm />);

// Simulate error state
// ... trigger error somehow ...

// Random button should clear error and transition state
fireEvent.click(screen.getByTestId('random-button'));
await waitFor(() => {
  expect(screen.queryByText(mockError)).not.toBeInTheDocument();
});
```

### Time Estimation Lessons

#### React Test Complexity Assessment
**Actual vs Estimated Time**: 45 minutes vs 3-4 hours estimated
**Success Factors**:
- Pattern-scout approach saved ~2 hours of trial-and-error
- Systematic ordering prevented test interference
- Understanding component architecture upfront vs debugging incrementally

**Complexity Indicators**:
- **Low**: Single state, simple interactions (15-30 min)
- **Medium**: Conditional rendering, multiple states (45-90 min) 
- **High**: Complex state machines, async interactions (2-4 hours)

#### Key Breakthrough Moments
1. **Architecture Understanding**: Realizing empty vs standard states have different input elements
2. **Query Strategy**: Understanding when to re-query vs cache element references  
3. **State Transition Logic**: Understanding random button populates input AND clears error AND transitions state
4. **Pattern Mining**: Finding existing conditional rendering test patterns in codebase

### Debugging Strategy Patterns

#### Test-Driven Debugging Approach
1. **Identify Pattern**: What is the component supposed to do?
2. **Find Examples**: Search codebase for similar test patterns
3. **Understand State Flow**: Map out all possible component states
4. **Test State Transitions**: Focus on state changes, not static states
5. **Re-query After Changes**: Never cache DOM references across state transitions

This systematic approach reduced debugging time from hours to minutes by understanding the underlying component architecture before writing tests.

## Authentication Testing Patterns (AnyZine, 2025-09-08)

### Critical Authentication Mock Patterns

#### Complete Authentication Provider Mocking
**Key Insight**: Authentication providers require both hook mocks AND component mocks for comprehensive testing.

**Essential Mock Structure (tests/setup.ts)**:
```typescript
// Hook mocks - return predictable data
const mockUseUser = jest.fn(() => ({
  isSignedIn: true,
  user: { id: 'user_123', firstName: 'Test', lastName: 'User' },
  isLoaded: true,
}));

const mockUseAuth = jest.fn(() => ({
  isSignedIn: true,
  isLoaded: true,
  signOut: jest.fn(),
}));

// Component mocks - simple pass-through rendering
const MockSignedIn = ({ children }: { children: React.ReactNode }) => <>{children}</>;
const MockSignedOut = ({ children }: { children: React.ReactNode }) => <>{children}</>;

// Mock the entire module
jest.mock('@clerk/nextjs', () => ({
  useUser: mockUseUser,
  useAuth: mockUseAuth, 
  SignedIn: MockSignedIn,
  SignedOut: MockSignedOut,
}));
```

**Critical Pattern**: Mock components should render children directly - no complex conditional logic needed for testing.

#### Provider Dependency Chain Mocking
**Problem**: Authentication components often depend on multiple provider contexts (Clerk + Convex + others).

**Solution Pattern**: Mock all provider dependencies in global test setup:
```typescript
// Mock Convex provider to prevent context errors
jest.mock('convex/react', () => ({
  useConvex: () => ({}),
  ConvexProvider: ({ children }: { children: React.ReactNode }) => <>{children}</>,
}));
```

**Lesson**: Provider errors cascade - mock all providers, not just the primary authentication one.

### Authentication-Aware Component Testing

#### State-Based Authentication Testing
**Pattern**: Test different authentication states by updating mock return values:

```typescript
describe('Authentication States', () => {
  beforeEach(() => {
    // Reset to default authenticated state
    mockUseUser.mockReturnValue({
      isSignedIn: true,
      user: { id: 'user_123', firstName: 'Test', lastName: 'User' },
      isLoaded: true,
    });
  });

  it('should handle unauthenticated state', async () => {
    // Override for this test
    mockUseUser.mockReturnValue({
      isSignedIn: false,
      user: null,
      isLoaded: true,
    });

    render(<AuthenticatedComponent />);
    expect(screen.getByTestId('login-prompt')).toBeInTheDocument();
  });

  it('should handle loading state', async () => {
    mockUseUser.mockReturnValue({
      isSignedIn: false,
      user: null,
      isLoaded: false, // Still loading
    });

    render(<AuthenticatedComponent />);
    expect(screen.getByTestId('loading-spinner')).toBeInTheDocument();
  });
});
```

#### Rate Limiting & Session Testing
**Advanced Pattern**: Test authentication edge cases like rate limiting and session expiration:

```typescript
it('should handle rate limiting with authentication', async () => {
  // Mock authenticated user
  mockUseUser.mockReturnValue({
    isSignedIn: true,
    user: { id: 'rate_limited_user' },
    isLoaded: true,
  });

  // Mock API response for rate limiting
  global.fetch = jest.fn()
    .mockResolvedValueOnce({
      ok: false,
      status: 429,
      json: async () => ({ error: 'Rate limited' }),
    });

  render(<Component />);
  fireEvent.click(screen.getByTestId('submit-button'));

  await waitFor(() => {
    expect(screen.getByTestId('rate-limit-message')).toBeInTheDocument();
  });
});
```

### Authentication Mock Anti-Patterns

#### Avoid Complex Mock Logic
**Anti-Pattern**: Adding complex conditional logic to mock components:
```typescript
// WRONG - Overcomplicating mocks
const MockSignedIn = ({ children }: { children: React.ReactNode }) => {
  const [isVisible, setIsVisible] = useState(false);
  useEffect(() => {
    // Complex logic...
  }, []);
  return isVisible ? <>{children}</> : null;
};
```

**Better Pattern**: Keep mocks simple and predictable:
```typescript
// RIGHT - Simple pass-through
const MockSignedIn = ({ children }: { children: React.ReactNode }) => <>{children}</>;
```

#### Avoid Incomplete Mock Coverage
**Anti-Pattern**: Mocking only hooks, forgetting component dependencies:
```typescript
// INCOMPLETE - Missing component mocks
jest.mock('@clerk/nextjs', () => ({
  useUser: mockUseUser,
  // Missing: SignedIn, SignedOut components
}));
```

**Complete Pattern**: Mock all exported items that components use:
```typescript
jest.mock('@clerk/nextjs', () => ({
  useUser: mockUseUser,
  useAuth: mockUseAuth,
  SignedIn: MockSignedIn,
  SignedOut: MockSignedOut,
  // Include any other components/hooks used
}));
```

### Test Organization Patterns for Authentication

#### Global vs Component-Specific Mocks
**Strategy**: Use global mocks in `tests/setup.ts` for consistent authentication state across all tests.

**Benefits**:
- Eliminates "useUser can only be used within <ClerkProvider />" errors
- Provides predictable authentication state for all components
- Reduces boilerplate mock code in individual test files

#### Mock Reset Patterns
**Pattern**: Reset authentication mocks between tests to prevent state leakage:
```typescript
describe('Component Tests', () => {
  beforeEach(() => {
    // Reset to default state
    mockUseUser.mockReturnValue(DEFAULT_AUTH_STATE);
    mockUseAuth.mockReturnValue(DEFAULT_AUTH_STATE);
    jest.clearAllMocks(); // Clear call history
  });
});
```

### Authentication Integration Test Patterns

#### End-to-End Authentication Flow Testing
**Pattern**: Test complete authentication workflows with proper state transitions:

```typescript
it('should handle complete authentication workflow', async () => {
  // Start unauthenticated
  mockUseUser.mockReturnValue({ isSignedIn: false, user: null, isLoaded: true });
  
  render(<App />);
  expect(screen.getByTestId('login-button')).toBeInTheDocument();

  // Simulate sign-in
  mockUseUser.mockReturnValue({ 
    isSignedIn: true, 
    user: { id: 'user_123' }, 
    isLoaded: true 
  });
  
  // Trigger re-render
  rerender(<App />);
  
  await waitFor(() => {
    expect(screen.getByTestId('authenticated-content')).toBeInTheDocument();
    expect(screen.queryByTestId('login-button')).not.toBeInTheDocument();
  });
});
```

### Time & Efficiency Lessons

#### Systematic Test Fixing Strategy
**Actual Time**: 15 minutes for 31 tests (20 failing → 11 new + 20 fixed)
**Estimated Time**: 1-2 hours

**Success Factors**:
1. **Global Mock Strategy**: Set up comprehensive mocks once, benefit everywhere
2. **Error Message Analysis**: "useUser can only be used within <ClerkProvider />" immediately pointed to missing provider mocks
3. **Incremental Approach**: Fix provider errors first, then component-specific issues

#### Authentication Test Complexity Assessment
- **Simple**: Basic authenticated/unauthenticated states (5-10 minutes)
- **Medium**: Multiple auth states + provider mocking (15-30 minutes) ← This case
- **Complex**: Custom auth flows, session management, token refresh (1-2 hours)

#### Key Breakthrough Insights
1. **Provider Dependency Chain**: Authentication failures often cascade from missing provider context, not just hook mocks
2. **Simple Mock Philosophy**: Complex mock logic creates more test complexity than value
3. **Global Setup Power**: Comprehensive global mocks eliminate repetitive setup and prevent provider errors across entire test suite
4. **Mock Component Pattern**: Authentication components in mocks should just render children - the business logic testing happens in the component being tested, not the mock

### Debugging Authentication Test Failures

#### Error Pattern Recognition
- **"useUser can only be used within <ClerkProvider />"** → Missing component provider mock
- **"Cannot read properties of undefined"** → Missing hook mock or incomplete return object
- **"Element not found"** → Authentication state affecting component rendering structure

#### Systematic Debugging Approach
1. **Check Provider Chain**: Ensure all authentication providers are mocked
2. **Verify Mock Completeness**: All hooks and components used by test components
3. **Test State Consistency**: Ensure mock states match component expectations
4. **Reset Between Tests**: Clear mock state to prevent test interference

This authentication testing approach created a robust, maintainable test suite that accurately validates authentication behavior while remaining simple and fast to execute.

## Cache Infrastructure Discovery & Configuration Patterns (Superwire, 2025-09-12)

### Critical Discovery: Multi-Layer Cache Architecture Already Built

#### Infrastructure-First Investigation Pattern
**Key Insight**: Before implementing new caching, search for existing cache infrastructure patterns in the codebase.

**Pattern-Scout Approach That Worked**:
```bash
# Search for existing cache strategies
grep -r "cache" --include="*.ts" --include="*.js"
grep -r "CacheStrategy" --include="*.ts" 
grep -r "stale-while-revalidate" --include="*.ts"
```

**Discovery**: Sophisticated multi-layer cache system already implemented but not configured at framework level:

1. **CDN Layer** (Cloudflare) - External caching
2. **Storage Layer** (Vercel Blob) - Asset caching  
3. **Runtime Layer** (Service Worker) - Client-side caching
4. **Framework Layer** (Next.js) - Missing configuration ← Implementation target

#### Existing Cache Constants Pattern (src/lib/cdn.ts)
**Found Well-Defined Cache Strategies**:
```typescript
export const CacheStrategies = {
  AUDIO: {
    maxAge: 86400,        // 1 day
    staleWhileRevalidate: 604800,  // 7 days
    browserCache: 3600,   // 1 hour
  },
  STATIC: {
    maxAge: 31536000,     // 1 year
    immutable: true,
    browserCache: 31536000, // 1 year
  },
  DYNAMIC: {
    maxAge: 300,          // 5 minutes
    staleWhileRevalidate: 600,   // 10 minutes
    browserCache: 60,     // 1 minute
  }
} as const;
```

**Critical Pattern**: Use existing constants for consistency across all caching layers.

#### Next.js Headers Configuration Pattern
**Implementation Strategy**: Align framework caching with existing infrastructure:

```typescript
// next.config.js - Following existing cache strategies
module.exports = {
  async headers() {
    return [
      {
        // Audio files - Use CacheStrategies.AUDIO
        source: '/episodes/:path*.mp3',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=86400, stale-while-revalidate=604800'
          }
        ]
      },
      {
        // Static assets - Use CacheStrategies.STATIC  
        source: '/images/:path*',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable'
          }
        ]
      }
    ];
  }
};
```

### Cache Strategy Alignment Lessons

#### Consistency Across Layers Critical
**Key Insight**: Cache headers must align with existing CDN, storage, and service worker configurations for optimal performance.

**Alignment Pattern Found**:
- **Service Worker** (`sw.ts`): Runtime cache strategies for offline support
- **CDN Configuration** (`cdn.ts`): Server-side cache strategies  
- **Next.js Headers**: Framework-level cache headers ← Missing piece

**Anti-Pattern**: Implementing cache headers without understanding existing infrastructure creates cache conflicts and unpredictable behavior.

#### Cache Duration Strategy Hierarchy
**Discovered Pattern**: Different content types need different cache strategies based on update frequency:

1. **Immutable Content** (images, compiled assets): 1 year + immutable flag
2. **Semi-Static Content** (audio episodes): 1 day fresh, 7 days stale
3. **Dynamic Content** (API responses): 5 minutes fresh, 10 minutes stale

**Implementation Insight**: Use constants from existing cache infrastructure rather than hardcoding durations.

### Multi-Layer Cache Integration Patterns

#### Service Worker Cache Integration
**Found Existing Pattern** (`sw.ts`):
```typescript
// Runtime caching already implemented
self.addEventListener('fetch', (event) => {
  // Audio files cached with custom strategy
  if (event.request.url.includes('/episodes/')) {
    event.respondWith(audioCacheStrategy(event.request));
  }
  // Static files cached differently
  if (event.request.url.includes('/images/')) {
    event.respondWith(staticCacheStrategy(event.request));
  }
});
```

**Next.js Integration**: Framework headers provide first layer, service worker provides runtime caching layer.

#### CDN Cache Integration  
**Existing CDN Configuration** (`cdn.ts`):
```typescript
// Cloudflare integration patterns already built
export async function setCDNHeaders(response: Response, cacheStrategy: CacheStrategy) {
  response.headers.set('CF-Cache-Status', 'HIT');
  response.headers.set('Cache-Control', buildCacheControlHeader(cacheStrategy));
}
```

**Framework Alignment**: Next.js headers should match CDN expectations for consistent cache behavior.

### Configuration Discovery Time Efficiency

#### Pattern-Scout vs Implementation-First
**Time Comparison**:
- **Implementation-First Approach** (estimated): 10-15 minutes
- **Pattern-Scout Approach** (actual): ~5 minutes

**Efficiency Gains**:
1. **No Configuration Conflicts**: Using existing constants prevented cache misalignment
2. **No Trial-and-Error**: Understanding existing infrastructure upfront
3. **Consistent Implementation**: Following established patterns  

#### Codebase Architecture Understanding
**Critical Insight**: 5 minutes of codebase exploration saved potential hours of debugging cache conflicts.

**Architecture Discovery Process**:
1. Search for existing cache patterns
2. Identify cache constants and strategies  
3. Map multi-layer cache architecture
4. Align new configuration with existing patterns

### Cache Configuration Best Practices Discovered

#### Use Framework-Agnostic Constants
**Pattern**: Define cache strategies in separate utility files, import in framework configuration:

```typescript
// Cache strategies defined once, used everywhere
import { CacheStrategies } from '../src/lib/cdn';

// next.config.js
const audioHeaders = buildCacheHeaders(CacheStrategies.AUDIO);
const staticHeaders = buildCacheHeaders(CacheStrategies.STATIC);
```

**Benefits**: 
- Consistency across all caching layers
- Single source of truth for cache durations
- Easy to update cache policies globally

#### Content-Type Specific Caching
**Discovered Granular Strategies**:
- **Audio Content**: Long cache with stale-while-revalidate for smooth playback
- **Static Images**: Maximum cache with immutable flag
- **API Routes**: Short cache with quick revalidation
- **HTML Pages**: Dynamic with stale-while-revalidate

#### Development vs Production Cache Alignment
**Found Pattern**: Development and production cache configurations should use same strategies but different durations:

```typescript
const isDev = process.env.NODE_ENV === 'development';

export const getCacheStrategy = (baseStrategy: CacheStrategy) => ({
  ...baseStrategy,
  maxAge: isDev ? 0 : baseStrategy.maxAge,        // Disable in dev
  staleWhileRevalidate: isDev ? 0 : baseStrategy.staleWhileRevalidate
});
```

### Key Architectural Insights

#### Cache Infrastructure Sophistication
**Discovery**: Many codebases have more sophisticated caching than initially apparent. Always search for existing patterns before implementing new cache strategies.

#### Multi-Layer Cache Coordination  
**Insight**: Modern applications often have 4+ cache layers that must be coordinated:
1. CDN (Cloudflare/CloudFront)
2. Framework (Next.js headers)
3. Storage Layer (Vercel Blob)
4. Client Runtime (Service Worker)

#### Configuration Time Estimation
**Actual Experience**: Cache configuration complexity depends more on existing infrastructure integration than implementation difficulty.

- **Simple** (no existing cache): 10-15 minutes
- **Integration** (existing infrastructure): 5 minutes ← This case  
- **Complex** (conflicting cache layers): 1-2 hours

### Cache Discovery Debugging Strategy

#### Systematic Infrastructure Mapping
1. **Search Cache Keywords**: Look for "cache", "Cache-Control", "stale-while-revalidate"
2. **Identify Constants**: Find cache duration definitions and strategies
3. **Map Cache Layers**: CDN, framework, storage, client-side
4. **Check Integration Points**: Service workers, API routes, static file handling

#### Red Flags for Cache Conflicts
- Hardcoded cache durations without constants
- Different cache strategies for same content type
- Missing cache headers on critical content types
- Development cache conflicts with production CDN

**Success Pattern**: Understanding existing cache architecture before configuration prevents conflicts and ensures optimal performance across all layers.