// ═══════════════════════════════════════════════════════════════════════════
// P5.JS GENERATIVE ART - BEST PRACTICES TEMPLATE
// ═══════════════════════════════════════════════════════════════════════════
//
// These are TOOLS and PRINCIPLES, not a recipe.
// Your algorithmic philosophy should guide WHAT you create.
//
// ═══════════════════════════════════════════════════════════════════════════

// ─────────────────────────────────────────────────────────────────────────────
// PARAMETER ORGANIZATION
// Centralize all tunable parameters for easy UI integration and persistence
// ─────────────────────────────────────────────────────────────────────────────

const params = {
    // Seed for reproducibility
    seed: 12345,

    // System parameters (customize for your algorithm)
    particleCount: 1000,
    speed: 1.0,
    scale: 0.01,

    // Visual parameters
    opacity: 50,
    strokeWeight: 1,

    // Color palette
    colors: ['#d97757', '#6a9bcc', '#788c5d']
};

// Store defaults for reset functionality
const defaultParams = JSON.parse(JSON.stringify(params));

// ─────────────────────────────────────────────────────────────────────────────
// SEEDED RANDOMNESS
// Always use seeds for reproducibility - same seed = same output
// ─────────────────────────────────────────────────────────────────────────────

function initializeRandomness() {
    randomSeed(params.seed);
    noiseSeed(params.seed);
}

// Custom seeded random using mulberry32 for additional control
function seededRandom(seed) {
    return function() {
        let t = seed += 0x6D2B79F5;
        t = Math.imul(t ^ t >>> 15, t | 1);
        t ^= t + Math.imul(t ^ t >>> 7, t | 61);
        return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
}

// ─────────────────────────────────────────────────────────────────────────────
// P5.JS LIFECYCLE PATTERNS
// Choose the approach that matches your algorithm
// ─────────────────────────────────────────────────────────────────────────────

// Pattern A: Static generation (setup only)
function setupStatic() {
    createCanvas(1200, 1200);
    initializeRandomness();
    generateArt();
    noLoop(); // Stop draw loop
}

// Pattern B: Continuous animation
function setupAnimated() {
    createCanvas(1200, 1200);
    initializeRandomness();
    initializeSystem();
}

function drawAnimated() {
    updateSystem();
    renderSystem();
}

// Pattern C: User-triggered regeneration
function regenerate() {
    initializeRandomness();
    clear();
    background(250, 249, 245);
    generateArt();
}

// ─────────────────────────────────────────────────────────────────────────────
// CLASS STRUCTURE FOR ENTITIES
// When algorithms involve multiple entities, organize with classes
// ─────────────────────────────────────────────────────────────────────────────

class Entity {
    constructor(x, y) {
        this.pos = createVector(x, y);
        this.vel = createVector(0, 0);
        this.acc = createVector(0, 0);
        this.history = [];
    }

    applyForce(force) {
        this.acc.add(force);
    }

    update() {
        this.vel.add(this.acc);
        this.vel.limit(params.speed);
        this.pos.add(this.vel);
        this.acc.mult(0);

        // Store history for trails
        this.history.push(this.pos.copy());
        if (this.history.length > 50) {
            this.history.shift();
        }
    }

    display() {
        // Override in subclass
    }

    edges() {
        // Wrap around edges
        if (this.pos.x > width) this.pos.x = 0;
        if (this.pos.x < 0) this.pos.x = width;
        if (this.pos.y > height) this.pos.y = 0;
        if (this.pos.y < 0) this.pos.y = height;
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// PERFORMANCE STRATEGIES
// Maintain 60fps with these techniques
// ─────────────────────────────────────────────────────────────────────────────

// Pre-calculate values that don't change
let precomputed = {
    sinTable: [],
    cosTable: [],
    noiseField: []
};

function precomputeValues() {
    // Sin/cos lookup tables
    for (let i = 0; i < 360; i++) {
        precomputed.sinTable[i] = Math.sin(radians(i));
        precomputed.cosTable[i] = Math.cos(radians(i));
    }

    // Pre-generate noise field
    const cols = Math.ceil(width / 10);
    const rows = Math.ceil(height / 10);
    for (let y = 0; y < rows; y++) {
        for (let x = 0; x < cols; x++) {
            precomputed.noiseField.push(
                noise(x * params.scale, y * params.scale)
            );
        }
    }
}

// Spatial hashing for collision detection
class SpatialHash {
    constructor(cellSize) {
        this.cellSize = cellSize;
        this.cells = new Map();
    }

    clear() {
        this.cells.clear();
    }

    hash(x, y) {
        return `${Math.floor(x / this.cellSize)},${Math.floor(y / this.cellSize)}`;
    }

    insert(entity) {
        const key = this.hash(entity.pos.x, entity.pos.y);
        if (!this.cells.has(key)) {
            this.cells.set(key, []);
        }
        this.cells.get(key).push(entity);
    }

    query(x, y, radius) {
        const results = [];
        const cellRadius = Math.ceil(radius / this.cellSize);
        const cx = Math.floor(x / this.cellSize);
        const cy = Math.floor(y / this.cellSize);

        for (let i = -cellRadius; i <= cellRadius; i++) {
            for (let j = -cellRadius; j <= cellRadius; j++) {
                const key = `${cx + i},${cy + j}`;
                if (this.cells.has(key)) {
                    results.push(...this.cells.get(key));
                }
            }
        }
        return results;
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// UTILITY FUNCTIONS
// Common operations for generative art
// ─────────────────────────────────────────────────────────────────────────────

// Convert hex to RGB
function hexToRgb(hex) {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : null;
}

// Get random color from palette
function randomPaletteColor() {
    return params.colors[floor(random(params.colors.length))];
}

// Lerp between two colors
function lerpColor(c1, c2, amt) {
    const rgb1 = hexToRgb(c1);
    const rgb2 = hexToRgb(c2);
    return color(
        lerp(rgb1.r, rgb2.r, amt),
        lerp(rgb1.g, rgb2.g, amt),
        lerp(rgb1.b, rgb2.b, amt)
    );
}

// Map value with easing
function easeMap(value, start1, stop1, start2, stop2, easingFn) {
    const t = map(value, start1, stop1, 0, 1);
    const easedT = easingFn(t);
    return lerp(start2, stop2, easedT);
}

// Common easing functions
const easing = {
    linear: t => t,
    easeInQuad: t => t * t,
    easeOutQuad: t => t * (2 - t),
    easeInOutQuad: t => t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t,
    easeInCubic: t => t * t * t,
    easeOutCubic: t => (--t) * t * t + 1,
    easeInOutCubic: t => t < 0.5 ? 4 * t * t * t : (t - 1) * (2 * t - 2) * (2 * t - 2) + 1,
    easeInExpo: t => t === 0 ? 0 : Math.pow(2, 10 * (t - 1)),
    easeOutExpo: t => t === 1 ? 1 : 1 - Math.pow(2, -10 * t)
};

// Wrap value within bounds
function wrap(value, min, max) {
    const range = max - min;
    return ((value - min) % range + range) % range + min;
}

// ─────────────────────────────────────────────────────────────────────────────
// FLOW FIELD UTILITIES
// Common patterns for flow-based generative art
// ─────────────────────────────────────────────────────────────────────────────

function createFlowField(cols, rows, scale) {
    const field = [];
    let yoff = 0;

    for (let y = 0; y < rows; y++) {
        let xoff = 0;
        for (let x = 0; x < cols; x++) {
            const angle = noise(xoff, yoff) * TWO_PI * 2;
            const v = p5.Vector.fromAngle(angle);
            v.setMag(1);
            field.push(v);
            xoff += scale;
        }
        yoff += scale;
    }

    return field;
}

function getFlowVector(field, x, y, cols, scl) {
    const col = Math.floor(x / scl);
    const row = Math.floor(y / scl);
    const index = col + row * cols;
    return field[index] ? field[index].copy() : createVector(0, 0);
}

// ─────────────────────────────────────────────────────────────────────────────
// REMEMBER
// ─────────────────────────────────────────────────────────────────────────────
//
// 1. Always seed your randomness
// 2. Pre-calculate expensive operations
// 3. Use spatial hashing for many entities
// 4. Parameters should reveal different facets of your system
// 5. Let your philosophy guide the implementation
//
// ═══════════════════════════════════════════════════════════════════════════
