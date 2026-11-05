document.addEventListener("DOMContentLoaded", function () {
    const section = document.querySelector(".cleaning-section");
    const cleaner1 = document.getElementById("cleaner1");
    const cleaner2 = document.getElementById("cleaner2");
    const bgImage = document.querySelector(".bg-image"); 

    let isWorking = false; 

    window.addEventListener("scroll", function () {
        const rect = section.getBoundingClientRect();
        const sectionPosition = rect.top;
        const screenPosition = window.innerHeight / 1.25;

        let offset = sectionPosition * 0.15; 
        bgImage.style.transform = `translateY(${offset}px) scale(1.3)`; 

        if (sectionPosition < screenPosition) {
            cleaner1.classList.add("active");
            cleaner2.classList.add("active");
            
            if (!isWorking) {
                isWorking = true;
                startWorking(); 
            }
        } else {
            cleaner1.classList.remove("active");
            cleaner2.classList.remove("active");
            
            if (isWorking) {
                isWorking = false;
                setTimeout(() => {
                    stopWorking();
                }, 800); 
            }
        }
    });

    function startWorking() {
        cleaner1.animate([
            { transform: 'translateY(0) rotate(0deg)' },
            { transform: 'translateY(0) rotate(-5deg)' },
            { transform: 'translateY(0) rotate(0deg)' }
        ], {
            duration: 800,
            iterations: Infinity,
            direction: 'alternate',
            easing: 'ease-in-out'
        });

        cleaner2.animate([
            { transform: 'translateY(0) translateX(0)' },
            { transform: 'translateY(0) translateX(15px)' },
            { transform: 'translateY(0) translateX(0)' }
        ], {
            duration: 1200,
            iterations: Infinity,
            direction: 'alternate',
            easing: 'ease-in-out'
        });
    }

    function stopWorking() {
        cleaner1.getAnimations().forEach(anim => anim.cancel());
        cleaner2.getAnimations().forEach(anim => anim.cancel());
    }
});