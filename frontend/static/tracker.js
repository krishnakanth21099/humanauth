/**
 * Humanauth Behavior Tracker
 * Tracks user behavior for entropy calculation and bot detection.
 */

class BehaviorTracker {
    constructor() {
        this.mouseMovements = [];
        this.keystrokes = [];
        this.scrollEvents = [];
        this.touchEvents = [];
        this.startTime = Date.now();
        this.isTracking = false;
    }

    /**
     * Start tracking user behavior
     */
    startTracking() {
        if (this.isTracking) return;
        this.isTracking = true;
        
        // Reset data
        this.mouseMovements = [];
        this.keystrokes = [];
        this.scrollEvents = [];
        this.touchEvents = [];
        this.startTime = Date.now();
        
        // Add event listeners
        document.addEventListener('mousemove', this.handleMouseMove.bind(this));
        document.addEventListener('keydown', this.handleKeyDown.bind(this));
        document.addEventListener('scroll', this.handleScroll.bind(this));
        document.addEventListener('touchstart', this.handleTouchStart.bind(this));
        document.addEventListener('touchmove', this.handleTouchMove.bind(this));
        document.addEventListener('touchend', this.handleTouchEnd.bind(this));
        
        console.log('Behavior tracking started');
    }

    /**
     * Stop tracking user behavior
     */
    stopTracking() {
        if (!this.isTracking) return;
        
        // Remove event listeners
        document.removeEventListener('mousemove', this.handleMouseMove.bind(this));
        document.removeEventListener('keydown', this.handleKeyDown.bind(this));
        document.removeEventListener('scroll', this.handleScroll.bind(this));
        document.removeEventListener('touchstart', this.handleTouchStart.bind(this));
        document.removeEventListener('touchmove', this.handleTouchMove.bind(this));
        document.removeEventListener('touchend', this.handleTouchEnd.bind(this));
        
        this.isTracking = false;
        console.log('Behavior tracking stopped');
    }

    /**
     * Handle mouse movement events
     */
    handleMouseMove(event) {
        // Throttle to avoid too many events
        if (this.mouseMovements.length > 0) {
            const lastMove = this.mouseMovements[this.mouseMovements.length - 1];
            const timeDiff = Date.now() - lastMove.timestamp;
            
            // Only record every 50ms or if moved more than 5 pixels
            const distance = Math.sqrt(
                Math.pow(event.clientX - lastMove.x, 2) + 
                Math.pow(event.clientY - lastMove.y, 2)
            );
            
            if (timeDiff < 50 && distance < 5) {
                return;
            }
        }
        
        this.mouseMovements.push({
            x: event.clientX,
            y: event.clientY,
            timestamp: Date.now()
        });
    }

    /**
     * Handle keyboard events
     */
    handleKeyDown(event) {
        // Don't record the actual keys for privacy, just the timing
        this.keystrokes.push({
            timestamp: Date.now()
        });
    }

    /**
     * Handle scroll events
     */
    handleScroll(event) {
        this.scrollEvents.push({
            scrollX: window.scrollX,
            scrollY: window.scrollY,
            timestamp: Date.now()
        });
    }

    /**
     * Handle touch start events
     */
    handleTouchStart(event) {
        if (event.touches.length > 0) {
            const touch = event.touches[0];
            this.touchEvents.push({
                type: 'start',
                x: touch.clientX,
                y: touch.clientY,
                timestamp: Date.now()
            });
        }
    }

    /**
     * Handle touch move events
     */
    handleTouchMove(event) {
        if (event.touches.length > 0) {
            const touch = event.touches[0];
            
            // Throttle to avoid too many events
            if (this.touchEvents.length > 0) {
                const lastTouch = this.touchEvents[this.touchEvents.length - 1];
                const timeDiff = Date.now() - lastTouch.timestamp;
                
                // Only record every 50ms or if moved more than 5 pixels
                if (lastTouch.type === 'move') {
                    const distance = Math.sqrt(
                        Math.pow(touch.clientX - lastTouch.x, 2) + 
                        Math.pow(touch.clientY - lastTouch.y, 2)
                    );
                    
                    if (timeDiff < 50 && distance < 5) {
                        return;
                    }
                }
            }
            
            this.touchEvents.push({
                type: 'move',
                x: touch.clientX,
                y: touch.clientY,
                timestamp: Date.now()
            });
        }
    }

    /**
     * Handle touch end events
     */
    handleTouchEnd(event) {
        this.touchEvents.push({
            type: 'end',
            timestamp: Date.now()
        });
    }

    /**
     * Calculate entropy score based on collected behavior data
     */
    calculateEntropyScore() {
        // This is a simplified entropy calculation
        // In a real implementation, this would be more sophisticated
        
        let score = 0.5; // Default neutral score
        
        // Mouse movement entropy
        if (this.mouseMovements.length > 10) {
            // Calculate variance in mouse movement speed and direction
            const speeds = [];
            const angles = [];
            
            for (let i = 1; i < this.mouseMovements.length; i++) {
                const prev = this.mouseMovements[i-1];
                const curr = this.mouseMovements[i];
                
                const dx = curr.x - prev.x;
                const dy = curr.y - prev.y;
                const dt = curr.timestamp - prev.timestamp;
                
                if (dt > 0) {
                    const speed = Math.sqrt(dx*dx + dy*dy) / dt;
                    speeds.push(speed);
                    
                    const angle = Math.atan2(dy, dx);
                    angles.push(angle);
                }
            }
            
            // Calculate variance
            if (speeds.length > 5) {
                const avgSpeed = speeds.reduce((sum, val) => sum + val, 0) / speeds.length;
                const speedVariance = speeds.reduce((sum, val) => sum + Math.pow(val - avgSpeed, 2), 0) / speeds.length;
                
                // Higher variance is more human-like (up to a point)
                const speedScore = Math.min(1.0, speedVariance / 5000);
                
                // Direction changes
                let directionChanges = 0;
                for (let i = 1; i < angles.length; i++) {
                    const angleDiff = Math.abs(angles[i] - angles[i-1]);
                    if (angleDiff > 0.3) { // About 17 degrees
                        directionChanges++;
                    }
                }
                
                const directionChangeRate = directionChanges / angles.length;
                
                // Direction changes should be in a "human" range
                const directionScore = 1.0 - Math.abs(directionChangeRate - 0.3) * 2;
                
                // Combine scores
                score = 0.7 * speedScore + 0.3 * Math.max(0, Math.min(1, directionScore));
            }
        }
        
        return score;
    }

    /**
     * Get behavior data for submission
     */
    getBehaviorData() {
        return {
            mouse_movements: this.mouseMovements,
            keystroke_timings: this.keystrokes,
            scroll_events: this.scrollEvents,
            touch_events: this.touchEvents,
            total_tracking_time_ms: Date.now() - this.startTime,
            entropy_score: this.calculateEntropyScore()
        };
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = BehaviorTracker;
} else {
    window.BehaviorTracker = BehaviorTracker;
}
