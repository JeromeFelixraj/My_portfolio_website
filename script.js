// Initialize EmailJS with your credentials
(function() {
    emailjs.init("cwbAzsQNjsgSUiYsE"); // Your public key
})();

// Initialize particles.js
particlesJS('particles-js', {
    particles: {
        number: {
            value: 80,
            density: {
                enable: true,
                value_area: 800
            }
        },
        color: {
            value: ['#6c63ff', '#4a44c9', '#ff6b6b']
        },
        shape: {
            type: 'circle',
            stroke: {
                width: 0,
                color: '#000000'
            }
        },
        opacity: {
            value: 0.5,
            random: true,
            anim: {
                enable: true,
                speed: 1,
                opacity_min: 0.1,
                sync: false
            }
        },
        size: {
            value: 3,
            random: true,
            anim: {
                enable: true,
                speed: 2,
                size_min: 0.1,
                sync: false
            }
        },
        line_linked: {
            enable: true,
            distance: 150,
            color: '#6c63ff',
            opacity: 0.2,
            width: 1
        },
        move: {
            enable: true,
            speed: 1,
            direction: 'none',
            random: true,
            straight: false,
            out_mode: 'out',
            bounce: false,
            attract: {
                enable: false,
                rotateX: 600,
                rotateY: 1200
            }
        }
    },
    interactivity: {
        detect_on: 'canvas',
        events: {
            onhover: {
                enable: true,
                mode: 'grab'
            },
            onclick: {
                enable: true,
                mode: 'push'
            },
            resize: true
        },
        modes: {
            grab: {
                distance: 140,
                line_linked: {
                    opacity: 0.5
                }
            },
            push: {
                particles_nb: 4
            }
        }
    },
    retina_detect: true
});

// Mobile Navigation Toggle
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');

hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    navMenu.classList.toggle('active');
});

document.querySelectorAll('.nav-link').forEach(n => n.addEventListener('click', () => {
    hamburger.classList.remove('active');
    navMenu.classList.remove('active');
}));

// Header Scroll Effect
window.addEventListener('scroll', () => {
    const header = document.getElementById('header');
    if (window.scrollY > 50) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }

    // Back to Top Button
    const backToTop = document.querySelector('.back-to-top');
    if (window.scrollY > 300) {
        backToTop.classList.add('active');
    } else {
        backToTop.classList.remove('active');
    }
});

// Portfolio Filter
const filterButtons = document.querySelectorAll('.filter-btn');
const portfolioItems = document.querySelectorAll('.portfolio-item');

filterButtons.forEach(button => {
    button.addEventListener('click', () => {
        // Remove active class from all buttons
        filterButtons.forEach(btn => btn.classList.remove('active'));
        // Add active class to clicked button
        button.classList.add('active');
        
        const filterValue = button.getAttribute('data-filter');
        
        portfolioItems.forEach(item => {
            if (filterValue === 'all' || item.getAttribute('data-category') === filterValue) {
                item.style.display = 'block';
                setTimeout(() => {
                    item.style.opacity = '1';
                    item.style.transform = 'translateY(0)';
                }, 100);
            } else {
                item.style.opacity = '0';
                item.style.transform = 'translateY(20px)';
                setTimeout(() => {
                    item.style.display = 'none';
                }, 300);
            }
        });
    });
});

// Form Submission with EmailJS
document.getElementById('contactForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const submitBtn = this.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
    submitBtn.disabled = true;

    // Get current time for the template
    const now = new Date();
    const timeString = now.toLocaleString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });

    // Prepare template parameters
    const templateParams = {
        name: this.name.value,
        email: this.email.value,
        subject: this.subject.value,
        message: this.message.value,
        time: timeString
    };

    // Debug: Log the template parameters
    console.log('Template parameters:', templateParams);

    // Send email using EmailJS
    emailjs.send('service_01usjpk', 'template_b2hh3ti', templateParams)
        .then(function(response) {
            console.log('SUCCESS!', response.status, response.text);
            showNotification('Message sent successfully! I will get back to you soon.', 'success');
            document.getElementById('contactForm').reset();
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }, function(error) {
            console.error('FAILED...', error);
            showNotification('Failed to send message. Please try again or contact me directly at jeromefelixraj123@gmail.com', 'error');
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        });
});

// Custom notification function
function showNotification(message, type) {
    // Remove existing notification if any
    const existingNotification = document.querySelector('.custom-notification');
    if (existingNotification) {
        existingNotification.remove();
    }

    // Create notification element
    const notification = document.createElement('div');
    notification.className = `custom-notification ${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i>
            <span>${message}</span>
        </div>
        <button class="notification-close">
            <i class="fas fa-times"></i>
        </button>
    `;

    // Add close functionality
    notification.querySelector('.notification-close').addEventListener('click', () => {
        notification.style.animation = 'slideOutRight 0.5s ease-in forwards';
        setTimeout(() => notification.remove(), 500);
    });
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.style.animation = 'slideOutRight 0.5s ease-in forwards';
            setTimeout(() => notification.remove(), 500);
        }
    }, 5000);

    document.body.appendChild(notification);
}

// Animate Skill Bars on Scroll
const animateSkillBars = () => {
    const skillBars = document.querySelectorAll('.skill-progress');
    skillBars.forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0';
        setTimeout(() => {
            bar.style.width = width;
        }, 500);
    });
};

// Intersection Observer for skill bars animation
const aboutSection = document.querySelector('.about');
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            animateSkillBars();
        }
    });
}, { threshold: 0.5 });

observer.observe(aboutSection);

// Image upload functionality
document.addEventListener('DOMContentLoaded', function() {
    const profileImage = document.querySelector('.profile-image');
    
    // Create a simple placeholder image using canvas
    function createPlaceholderImage() {
        const canvas = document.createElement('canvas');
        canvas.width = 400;
        canvas.height = 400;
        const ctx = canvas.getContext('2d');
        
        // Draw background
        ctx.fillStyle = '#6c63ff';
        ctx.globalAlpha = 0.1;
        ctx.beginPath();
        ctx.arc(200, 200, 200, 0, Math.PI * 2);
        ctx.fill();
        
        // Draw head
        ctx.globalAlpha = 1;
        ctx.fillStyle = '#6c63ff';
        ctx.beginPath();
        ctx.arc(200, 150, 60, 0, Math.PI * 2);
        ctx.fill();
        
        // Draw body
        ctx.beginPath();
        ctx.moveTo(140, 210);
        ctx.quadraticCurveTo(200, 300, 260, 210);
        ctx.lineTo(260, 350);
        ctx.quadraticCurveTo(200, 380, 140, 350);
        ctx.closePath();
        ctx.fill();
        
        return canvas.toDataURL();
    }
    
    // Set placeholder image if needed
    if (profileImage && !profileImage.complete) {
        profileImage.onerror = function() {
            this.src = createPlaceholderImage();
        };
    }
});
