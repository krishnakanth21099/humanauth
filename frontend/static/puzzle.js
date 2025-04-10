/**
 * Humanauth Puzzle Renderer
 * Renders different types of CAPTCHA challenges.
 */

class PuzzleRenderer {
    constructor(containerElement) {
        this.container = containerElement;
        this.challenge = null;
        this.startTime = null;
        this.responseData = {};
        this.behaviorTracker = new BehaviorTracker();
    }

    /**
     * Load and render a challenge
     * @param {Object} challenge - Challenge data from the API
     */
    loadChallenge(challenge) {
        this.challenge = challenge;
        this.startTime = Date.now();
        this.responseData = {};

        // Clear container
        this.container.innerHTML = '';

        // Start behavior tracking
        this.behaviorTracker.startTracking();

        // Render based on challenge type
        switch (challenge.type) {
            case 'drag-align':
                this.renderDragAlign();
                break;
            case 'reverse-turing':
                this.renderReverseTuring();
                break;
            case 'reaction-tap':
                this.renderReactionTap();
                break;
            case 'vibe-match':
                this.renderVibeMatch();
                break;
            case 'pattern-completion':
                this.renderPatternCompletion();
                break;
            case 'audio-captcha':
                this.renderAudioCaptcha();
                break;
            case 'semantic-grouping':
                this.renderSemanticGrouping();
                break;
            default:
                this.renderUnsupported();
        }
    }

    /**
     * Render drag-align challenge
     */
    renderDragAlign() {
        const challenge = this.challenge;

        // Create canvas
        const canvas = document.createElement('canvas');
        canvas.width = 400;
        canvas.height = 300;
        this.container.appendChild(canvas);

        // Add instruction
        const instruction = document.createElement('p');
        instruction.textContent = 'Drag the shapes to match their outlines';
        instruction.className = 'instruction';
        this.container.insertBefore(instruction, canvas);

        const ctx = canvas.getContext('2d');

        // Draw targets (outlines)
        challenge.targets.forEach(target => {
            ctx.strokeStyle = '#888';
            ctx.lineWidth = 2;
            this.drawShape(ctx, target.type, target.x, target.y, target.size, true);
        });

        // Track dragged shapes
        let draggedShape = null;
        let offsetX = 0;
        let offsetY = 0;

        // Store current positions of shapes
        const positions = {};
        challenge.shapes.forEach(shape => {
            positions[shape.id] = { x: shape.x, y: shape.y };
        });

        // Draw shapes
        const drawShapes = () => {
            // Clear canvas
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Draw targets (outlines)
            challenge.targets.forEach(target => {
                ctx.strokeStyle = '#888';
                ctx.lineWidth = 2;
                this.drawShape(ctx, target.type, target.x, target.y, target.size, true);
            });

            // Draw shapes
            challenge.shapes.forEach(shape => {
                const pos = positions[shape.id];
                ctx.fillStyle = this.getShapeColor(shape.type);
                this.drawShape(ctx, shape.type, pos.x, pos.y, shape.size);
            });
        };

        // Initial draw
        drawShapes();

        // Add event listeners for dragging
        canvas.addEventListener('mousedown', (e) => {
            const rect = canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            // Check if a shape was clicked
            for (const shape of challenge.shapes) {
                const pos = positions[shape.id];
                if (this.isPointInShape(x, y, shape.type, pos.x, pos.y, shape.size)) {
                    draggedShape = shape;
                    offsetX = x - pos.x;
                    offsetY = y - pos.y;
                    break;
                }
            }
        });

        canvas.addEventListener('mousemove', (e) => {
            if (!draggedShape) return;

            const rect = canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            // Update position
            positions[draggedShape.id] = {
                x: x - offsetX,
                y: y - offsetY
            };

            // Redraw
            drawShapes();
        });

        canvas.addEventListener('mouseup', () => {
            draggedShape = null;

            // Store positions in response data
            this.responseData.positions = positions;

            // Check if all shapes are aligned
            let allAligned = true;
            for (const shape of challenge.shapes) {
                const pos = positions[shape.id];
                const target = challenge.targets.find(t => t.type === shape.type);

                if (target) {
                    const distance = Math.sqrt(
                        Math.pow(pos.x - target.x, 2) +
                        Math.pow(pos.y - target.y, 2)
                    );

                    if (distance > 20) {
                        allAligned = false;
                        break;
                    }
                }
            }

            if (allAligned) {
                this.submitResponse();
            }
        });

        // Add submit button
        const submitButton = document.createElement('button');
        submitButton.textContent = 'Submit';
        submitButton.className = 'submit-button';
        submitButton.addEventListener('click', () => {
            this.submitResponse();
        });
        this.container.appendChild(submitButton);
    }

    /**
     * Render reverse-turing challenge
     */
    renderReverseTuring() {
        const challenge = this.challenge;

        // Add instruction
        const instruction = document.createElement('p');
        instruction.textContent = challenge.instruction;
        instruction.className = 'instruction';
        this.container.appendChild(instruction);

        // Create text options
        const textContainer = document.createElement('div');
        textContainer.className = 'text-options';

        challenge.texts.forEach(text => {
            const textBox = document.createElement('div');
            textBox.className = 'text-box';
            textBox.dataset.id = text.id;

            const textContent = document.createElement('p');
            textContent.textContent = text.content;
            textBox.appendChild(textContent);

            textBox.addEventListener('click', () => {
                // Remove selected class from all text boxes
                document.querySelectorAll('.text-box').forEach(box => {
                    box.classList.remove('selected');
                });

                // Add selected class to clicked text box
                textBox.classList.add('selected');

                // Store selection in response data
                this.responseData.selected_id = text.id;
            });

            textContainer.appendChild(textBox);
        });

        this.container.appendChild(textContainer);

        // Add submit button
        const submitButton = document.createElement('button');
        submitButton.textContent = 'Submit';
        submitButton.className = 'submit-button';
        submitButton.addEventListener('click', () => {
            if (this.responseData.selected_id) {
                this.submitResponse();
            } else {
                alert('Please select an option');
            }
        });
        this.container.appendChild(submitButton);
    }

    /**
     * Render reaction-tap challenge
     */
    renderReactionTap() {
        const challenge = this.challenge;

        // Add instruction
        const instruction = document.createElement('p');
        instruction.textContent = challenge.instruction;
        instruction.className = 'instruction';
        this.container.appendChild(instruction);

        // Create canvas
        const canvas = document.createElement('canvas');
        canvas.width = challenge.canvas.width;
        canvas.height = challenge.canvas.height;
        this.container.appendChild(canvas);

        const ctx = canvas.getContext('2d');

        // Clear canvas
        ctx.fillStyle = '#f0f0f0';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Store tap data
        this.responseData.taps = {};

        // Track active targets
        const activeTargets = new Set();

        // Handle canvas clicks
        canvas.addEventListener('click', (e) => {
            const rect = canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            // Check if a target was clicked
            for (const targetId of activeTargets) {
                const target = challenge.targets.find(t => t.id === targetId);
                if (!target) continue;

                const distance = Math.sqrt(
                    Math.pow(x - target.x, 2) +
                    Math.pow(y - target.y, 2)
                );

                if (distance <= target.radius) {
                    // Record tap time
                    this.responseData.taps[targetId] = Date.now();

                    // Remove from active targets
                    activeTargets.delete(targetId);

                    // Draw hit effect
                    ctx.fillStyle = 'rgba(0, 255, 0, 0.5)';
                    ctx.beginPath();
                    ctx.arc(target.x, target.y, target.radius, 0, Math.PI * 2);
                    ctx.fill();

                    // Check if all targets have been tapped
                    if (activeTargets.size === 0 &&
                        Object.keys(this.responseData.taps).length === challenge.targets.length) {
                        setTimeout(() => {
                            this.submitResponse();
                        }, 500);
                    }

                    break;
                }
            }
        });

        // Schedule targets to appear
        challenge.targets.forEach(target => {
            setTimeout(() => {
                // Add to active targets
                activeTargets.add(target.id);

                // Draw target
                ctx.fillStyle = 'rgba(255, 0, 0, 0.7)';
                ctx.beginPath();
                ctx.arc(target.x, target.y, target.radius, 0, Math.PI * 2);
                ctx.fill();

                // Schedule target to disappear
                setTimeout(() => {
                    // Remove from active targets if not already tapped
                    if (activeTargets.has(target.id)) {
                        activeTargets.delete(target.id);

                        // Clear target
                        ctx.fillStyle = '#f0f0f0';
                        ctx.beginPath();
                        ctx.arc(target.x, target.y, target.radius + 2, 0, Math.PI * 2);
                        ctx.fill();
                    }

                    // Check if all targets have been shown
                    if (activeTargets.size === 0 &&
                        Object.keys(this.responseData.taps).length < challenge.targets.length) {
                        // Auto-submit after all targets have been shown
                        setTimeout(() => {
                            this.submitResponse();
                        }, 500);
                    }
                }, target.disappear_after_ms);
            }, target.appear_after_ms);
        });
    }

    /**
     * Render vibe-match challenge
     */
    renderVibeMatch() {
        const challenge = this.challenge;

        // Add instruction
        const instruction = document.createElement('p');
        instruction.textContent = challenge.instruction;
        instruction.className = 'instruction';
        this.container.appendChild(instruction);

        // Add text
        const textElement = document.createElement('div');
        textElement.className = 'vibe-text';
        textElement.textContent = challenge.text;
        this.container.appendChild(textElement);

        // Create options
        const optionsContainer = document.createElement('div');
        optionsContainer.className = 'emotion-options';

        challenge.options.forEach(emotion => {
            const optionButton = document.createElement('button');
            optionButton.textContent = emotion;
            optionButton.className = 'emotion-option';

            optionButton.addEventListener('click', () => {
                // Remove selected class from all options
                document.querySelectorAll('.emotion-option').forEach(btn => {
                    btn.classList.remove('selected');
                });

                // Add selected class to clicked option
                optionButton.classList.add('selected');

                // Store selection in response data
                this.responseData.selected_emotion = emotion;
            });

            optionsContainer.appendChild(optionButton);
        });

        this.container.appendChild(optionsContainer);

        // Add submit button
        const submitButton = document.createElement('button');
        submitButton.textContent = 'Submit';
        submitButton.className = 'submit-button';
        submitButton.addEventListener('click', () => {
            if (this.responseData.selected_emotion) {
                this.submitResponse();
            } else {
                alert('Please select an emotion');
            }
        });
        this.container.appendChild(submitButton);
    }

    /**
     * Render pattern-completion challenge
     */
    renderPatternCompletion() {
        const challenge = this.challenge;

        // Add instruction
        const instruction = document.createElement('p');
        instruction.textContent = challenge.instruction;
        instruction.className = 'instruction';
        this.container.appendChild(instruction);

        if (challenge.pattern_type === 'sequence') {
            // Render sequence pattern
            const sequenceContainer = document.createElement('div');
            sequenceContainer.className = 'sequence-container';

            // Display sequence
            const sequence = document.createElement('div');
            sequence.className = 'sequence';
            sequence.textContent = challenge.sequence.join(', ') + ', ?';
            sequenceContainer.appendChild(sequence);

            this.container.appendChild(sequenceContainer);

            // Create options
            const optionsContainer = document.createElement('div');
            optionsContainer.className = 'sequence-options';

            challenge.options.forEach(option => {
                const optionButton = document.createElement('button');
                optionButton.textContent = option;
                optionButton.className = 'sequence-option';

                optionButton.addEventListener('click', () => {
                    // Remove selected class from all options
                    document.querySelectorAll('.sequence-option').forEach(btn => {
                        btn.classList.remove('selected');
                    });

                    // Add selected class to clicked option
                    optionButton.classList.add('selected');

                    // Store selection in response data
                    this.responseData.selected_answer = option;
                });

                optionsContainer.appendChild(optionButton);
            });

            this.container.appendChild(optionsContainer);
        } else if (challenge.pattern_type === 'grid') {
            // Render grid pattern
            const gridContainer = document.createElement('div');
            gridContainer.className = 'grid-container';

            // Create grid
            const grid = document.createElement('div');
            grid.className = 'pattern-grid';
            grid.style.gridTemplateColumns = `repeat(${challenge.grid[0].length}, 1fr)`;

            // Fill grid
            for (let i = 0; i < challenge.grid.length; i++) {
                for (let j = 0; j < challenge.grid[i].length; j++) {
                    const cell = document.createElement('div');
                    cell.className = 'grid-cell';

                    if (challenge.grid[i][j] === null) {
                        // This is the missing cell
                        cell.classList.add('missing-cell');
                        cell.textContent = '?';
                    } else {
                        cell.textContent = challenge.grid[i][j];
                    }

                    grid.appendChild(cell);
                }
            }

            gridContainer.appendChild(grid);
            this.container.appendChild(gridContainer);

            // Create options
            const optionsContainer = document.createElement('div');
            optionsContainer.className = 'grid-options';

            challenge.options.forEach(option => {
                const optionButton = document.createElement('button');
                optionButton.textContent = option;
                optionButton.className = 'grid-option';

                optionButton.addEventListener('click', () => {
                    // Remove selected class from all options
                    document.querySelectorAll('.grid-option').forEach(btn => {
                        btn.classList.remove('selected');
                    });

                    // Add selected class to clicked option
                    optionButton.classList.add('selected');

                    // Store selection in response data
                    this.responseData.selected_answer = option;

                    // Update missing cell
                    document.querySelector('.missing-cell').textContent = option;
                });

                optionsContainer.appendChild(optionButton);
            });

            this.container.appendChild(optionsContainer);
        }

        // Add submit button
        const submitButton = document.createElement('button');
        submitButton.textContent = 'Submit';
        submitButton.className = 'submit-button';
        submitButton.addEventListener('click', () => {
            if (this.responseData.selected_answer) {
                this.submitResponse();
            } else {
                alert('Please select an answer');
            }
        });
        this.container.appendChild(submitButton);
    }

    /**
     * Render audio-captcha challenge
     */
    renderAudioCaptcha() {
        const challenge = this.challenge;

        // Add instruction
        const instruction = document.createElement('p');
        instruction.textContent = challenge.instruction;
        instruction.className = 'instruction';
        this.container.appendChild(instruction);

        // Create audio element
        const audioContainer = document.createElement('div');
        audioContainer.className = 'audio-container';

        const audio = document.createElement('audio');
        audio.controls = true;
        audio.src = challenge.audio_file;

        const playButton = document.createElement('button');
        playButton.textContent = 'Play Audio';
        playButton.className = 'play-button';
        playButton.addEventListener('click', () => {
            audio.play();
        });

        audioContainer.appendChild(audio);
        audioContainer.appendChild(playButton);
        this.container.appendChild(audioContainer);

        // Create options
        const optionsContainer = document.createElement('div');
        optionsContainer.className = 'audio-options';

        challenge.options.forEach(option => {
            const optionButton = document.createElement('button');
            optionButton.textContent = option;
            optionButton.className = 'audio-option';

            optionButton.addEventListener('click', () => {
                // Remove selected class from all options
                document.querySelectorAll('.audio-option').forEach(btn => {
                    btn.classList.remove('selected');
                });

                // Add selected class to clicked option
                optionButton.classList.add('selected');

                // Store selection in response data
                this.responseData.selected_word = option;
            });

            optionsContainer.appendChild(optionButton);
        });

        this.container.appendChild(optionsContainer);

        // Add submit button
        const submitButton = document.createElement('button');
        submitButton.textContent = 'Submit';
        submitButton.className = 'submit-button';
        submitButton.addEventListener('click', () => {
            if (this.responseData.selected_word) {
                this.submitResponse();
            } else {
                alert('Please select a word');
            }
        });
        this.container.appendChild(submitButton);
    }

    /**
     * Render semantic-grouping challenge
     */
    renderSemanticGrouping() {
        const challenge = this.challenge;

        // Add instruction
        const instruction = document.createElement('p');
        instruction.textContent = challenge.instruction;
        instruction.className = 'instruction';
        this.container.appendChild(instruction);

        // Create categories
        const categoriesContainer = document.createElement('div');
        categoriesContainer.className = 'categories-container';

        challenge.categories.forEach(category => {
            const categoryBox = document.createElement('div');
            categoryBox.className = 'category-box';
            categoryBox.dataset.category = category;

            const categoryTitle = document.createElement('h3');
            categoryTitle.textContent = category;
            categoryBox.appendChild(categoryTitle);

            // Create dropzone
            const dropzone = document.createElement('div');
            dropzone.className = 'category-dropzone';
            dropzone.dataset.category = category;
            categoryBox.appendChild(dropzone);

            // Add event listeners for drag and drop
            dropzone.addEventListener('dragover', (e) => {
                e.preventDefault();
                dropzone.classList.add('dragover');
            });

            dropzone.addEventListener('dragleave', () => {
                dropzone.classList.remove('dragover');
            });

            dropzone.addEventListener('drop', (e) => {
                e.preventDefault();
                dropzone.classList.remove('dragover');

                const itemId = e.dataTransfer.getData('text/plain');
                const item = document.getElementById(itemId);

                if (item) {
                    dropzone.appendChild(item);

                    // Update response data
                    if (!this.responseData.groupings) {
                        this.responseData.groupings = {};
                    }

                    this.responseData.groupings[itemId] = category;

                    // Log for debugging
                    console.log('Updated groupings:', this.responseData.groupings);

                    // Check if all items have been grouped
                    if (Object.keys(this.responseData.groupings).length === challenge.items.length) {
                        // Auto-submit after a short delay
                        setTimeout(() => {
                            this.submitResponse();
                        }, 500);
                    }
                }
            });

            categoriesContainer.appendChild(categoryBox);
        });

        this.container.appendChild(categoriesContainer);

        // Create items
        const itemsContainer = document.createElement('div');
        itemsContainer.className = 'items-container';

        challenge.items.forEach(item => {
            const itemElement = document.createElement('div');
            itemElement.id = item.id;
            itemElement.className = 'draggable-item';
            itemElement.textContent = item.text;
            itemElement.draggable = true;

            // Add drag event listeners
            itemElement.addEventListener('dragstart', (e) => {
                e.dataTransfer.setData('text/plain', item.id);
                itemElement.classList.add('dragging');
            });

            itemElement.addEventListener('dragend', () => {
                itemElement.classList.remove('dragging');
            });

            itemsContainer.appendChild(itemElement);
        });

        this.container.appendChild(itemsContainer);

        // Add submit button
        const submitButton = document.createElement('button');
        submitButton.textContent = 'Submit';
        submitButton.className = 'submit-button';
        submitButton.addEventListener('click', () => {
            // Ensure groupings object exists
            if (!this.responseData.groupings) {
                this.responseData.groupings = {};
            }

            // Log for debugging
            console.log('Submitting groupings:', this.responseData.groupings);

            if (Object.keys(this.responseData.groupings).length > 0) {
                this.submitResponse();
            } else {
                alert('Please group at least some items');
            }
        });
        this.container.appendChild(submitButton);
    }

    /**
     * Render unsupported challenge type
     */
    renderUnsupported() {
        const message = document.createElement('p');
        message.textContent = `Unsupported challenge type: ${this.challenge.type}`;
        message.className = 'error-message';
        this.container.appendChild(message);

        // Add refresh button
        const refreshButton = document.createElement('button');
        refreshButton.textContent = 'Try Another Challenge';
        refreshButton.className = 'refresh-button';
        refreshButton.addEventListener('click', () => {
            // Trigger refresh event
            const event = new CustomEvent('refresh-challenge');
            document.dispatchEvent(event);
        });
        this.container.appendChild(refreshButton);
    }

    /**
     * Submit challenge response
     */
    submitResponse() {
        // Stop behavior tracking
        this.behaviorTracker.stopTracking();

        // Calculate time taken
        const timeTaken = Date.now() - this.startTime;

        // Get behavior data
        const behaviorData = this.behaviorTracker.getBehaviorData();

        // Create complete response
        const response = {
            challenge_type: this.challenge.type,
            response_data: this.responseData,
            behavior_data: behaviorData,
            time_taken_ms: timeTaken
        };

        // Trigger submit event
        const event = new CustomEvent('challenge-submitted', {
            detail: response
        });
        document.dispatchEvent(event);
    }

    /**
     * Helper method to draw a shape on canvas
     */
    drawShape(ctx, type, x, y, size, isOutline = false) {
        if (isOutline) {
            ctx.beginPath();
        }

        switch (type) {
            case 'circle':
                ctx.beginPath();
                ctx.arc(x, y, size / 2, 0, Math.PI * 2);
                break;
            case 'square':
                if (isOutline) {
                    ctx.rect(x - size / 2, y - size / 2, size, size);
                } else {
                    ctx.fillRect(x - size / 2, y - size / 2, size, size);
                }
                break;
            case 'triangle':
                ctx.beginPath();
                ctx.moveTo(x, y - size / 2);
                ctx.lineTo(x + size / 2, y + size / 2);
                ctx.lineTo(x - size / 2, y + size / 2);
                ctx.closePath();
                break;
            case 'star':
                this.drawStar(ctx, x, y, 5, size / 2, size / 4);
                break;
            case 'hexagon':
                this.drawPolygon(ctx, x, y, 6, size / 2);
                break;
        }

        if (isOutline) {
            ctx.stroke();
        } else {
            ctx.fill();
        }
    }

    /**
     * Helper method to draw a star
     */
    drawStar(ctx, x, y, spikes, outerRadius, innerRadius) {
        let rot = Math.PI / 2 * 3;
        let step = Math.PI / spikes;

        ctx.beginPath();
        ctx.moveTo(x, y - outerRadius);

        for (let i = 0; i < spikes; i++) {
            ctx.lineTo(x + Math.cos(rot) * outerRadius, y + Math.sin(rot) * outerRadius);
            rot += step;

            ctx.lineTo(x + Math.cos(rot) * innerRadius, y + Math.sin(rot) * innerRadius);
            rot += step;
        }

        ctx.lineTo(x, y - outerRadius);
        ctx.closePath();
    }

    /**
     * Helper method to draw a regular polygon
     */
    drawPolygon(ctx, x, y, sides, radius) {
        ctx.beginPath();
        ctx.moveTo(x + radius * Math.cos(0), y + radius * Math.sin(0));

        for (let i = 1; i <= sides; i++) {
            const angle = i * 2 * Math.PI / sides;
            ctx.lineTo(x + radius * Math.cos(angle), y + radius * Math.sin(angle));
        }

        ctx.closePath();
    }

    /**
     * Helper method to check if a point is inside a shape
     */
    isPointInShape(x, y, type, shapeX, shapeY, size) {
        switch (type) {
            case 'circle':
                const distance = Math.sqrt(Math.pow(x - shapeX, 2) + Math.pow(y - shapeY, 2));
                return distance <= size / 2;
            case 'square':
                return x >= shapeX - size / 2 && x <= shapeX + size / 2 &&
                       y >= shapeY - size / 2 && y <= shapeY + size / 2;
            case 'triangle':
                // Simple bounding box check for simplicity
                return x >= shapeX - size / 2 && x <= shapeX + size / 2 &&
                       y >= shapeY - size / 2 && y <= shapeY + size / 2;
            case 'star':
            case 'hexagon':
                // Simple radius check for simplicity
                const dist = Math.sqrt(Math.pow(x - shapeX, 2) + Math.pow(y - shapeY, 2));
                return dist <= size / 2;
            default:
                return false;
        }
    }

    /**
     * Helper method to get a color for a shape
     */
    getShapeColor(type) {
        const colors = {
            'circle': '#FF5733',
            'square': '#33A8FF',
            'triangle': '#33FF57',
            'star': '#FF33A8',
            'hexagon': '#A833FF'
        };

        return colors[type] || '#888888';
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PuzzleRenderer;
} else {
    window.PuzzleRenderer = PuzzleRenderer;
}
