const rabbit = document.getElementById('rabbit');
let targetX = 0;
let targetY = 0;
let currentX = 0;
let currentY = 0;

// Set initial position
rabbit.style.left = '50%';
rabbit.style.top = '50%';

// Update target position on click
document.addEventListener('click', (e) => {
    targetX = e.clientX - rabbit.offsetWidth / 2;
    targetY = e.clientY - rabbit.offsetHeight / 2;
});

// Animation loop
function animate() {
    // Get current position
    currentX = parseFloat(rabbit.style.left) || window.innerWidth / 2;
    currentY = parseFloat(rabbit.style.top) || window.innerHeight / 2;

    // Calculate direction to move
    const dx = targetX - currentX;
    const dy = targetY - currentY;
    const distance = Math.sqrt(dx * dx + dy * dy);

    // Only move if we're not at the target
    if (distance > 1) {
        // Calculate movement speed (faster when further away)
        const speed = Math.min(distance * 0.1, 5);
        
        // Calculate new position
        const newX = currentX + (dx / distance) * speed;
        const newY = currentY + (dy / distance) * speed;

        // Update rabbit position
        rabbit.style.left = newX + 'px';
        rabbit.style.top = newY + 'px';

        // Flip rabbit based on movement direction
        if (dx < 0) {
            rabbit.style.transform = 'scaleX(-1)';
        } else {
            rabbit.style.transform = 'scaleX(1)';
        }
    }

    requestAnimationFrame(animate);
}

// Start animation
animate(); 