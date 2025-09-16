class Firework {
    constructor(x, y, targetY, color) {
        this.x = x;
        this.y = y;
        this.startY = y;
        this.targetY = targetY;
        this.color = color;
        this.speed = 2 + Math.random() * 3;
        this.exploded = false;
        this.particles = [];
    }
    
    update() {
        if (!this.exploded) {
            this.y -= this.speed;
            if (this.y <= this.targetY) {
                this.explode();
            }
        } else {
            this.particles.forEach(p => p.update());
            this.particles = this.particles.filter(p => p.alpha > 0);
        }
    }
    
    explode() {
        this.exploded = true;
        const particleCount = 30 + Math.floor(Math.random() * 20);
        for (let i = 0; i < particleCount; i++) {
            const angle = (Math.PI * 2 * i) / particleCount;
            const velocity = 1 + Math.random() * 4;
            this.particles.push({
                x: this.x,
                y: this.y,
                vx: Math.cos(angle) * velocity,
                vy: Math.sin(angle) * velocity,
                alpha: 1,
                color: this.color,
                update: function() {
                    this.x += this.vx;
                    this.y += this.vy;
                    this.vy += 0.05;
                    this.alpha -= 0.015;
                }
            });
        }
    }
    
    draw(ctx) {
        if (!this.exploded) {
            ctx.fillStyle = this.color;
            ctx.fillRect(this.x - 2, this.y - 10, 4, 10);
        } else {
            this.particles.forEach(p => {
                ctx.globalAlpha = p.alpha;
                ctx.fillStyle = p.color;
                ctx.beginPath();
                ctx.arc(p.x, p.y, 2, 0, Math.PI * 2);
                ctx.fill();
            });
        }
    }
}

function startFireworks() {
    const canvas = document.getElementById('fireworksCanvas');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    canvas.style.display = 'block';
    
    const colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff', '#00ffff', '#ffa500', '#ff1493'];
    const fireworks = [];
    let animationId;
    let startTime = Date.now();
    
    function createFirework() {
        const x = Math.random() * canvas.width;
        const y = canvas.height;
        const targetY = 100 + Math.random() * (canvas.height * 0.5);
        const color = colors[Math.floor(Math.random() * colors.length)];
        fireworks.push(new Firework(x, y, targetY, color));
    }
    
    function animate() {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.globalAlpha = 1;
        
        if (Math.random() < 0.1 && Date.now() - startTime < 3000) {
            createFirework();
        }
        
        fireworks.forEach((fw, index) => {
            fw.update();
            fw.draw(ctx);
            if (fw.exploded && fw.particles.length === 0) {
                fireworks.splice(index, 1);
            }
        });
        
        if (Date.now() - startTime < 4000 || fireworks.length > 0) {
            animationId = requestAnimationFrame(animate);
        } else {
            canvas.style.display = 'none';
        }
    }
    
    for (let i = 0; i < 3; i++) {
        setTimeout(createFirework, i * 200);
    }
    
    animate();
}