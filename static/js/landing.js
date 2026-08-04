document.addEventListener('DOMContentLoaded', () => {
    // ===============================
    // 1. Mobile Menu Toggle
    // ===============================
    const mobileToggle = document.getElementById('mobile-toggle');
    const navMenu = document.getElementById('nav-menu');
    if (mobileToggle && navMenu) {
        mobileToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
            const icon = mobileToggle.querySelector('i');
            icon.classList.toggle('fa-bars');
            icon.classList.toggle('fa-xmark');
        });
    }
    // ===============================
    // 2. Close Mobile Menu On Link Click
    // ===============================
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if(navMenu.classList.contains('active')) {
                navMenu.classList.remove('active');
                const icon = mobileToggle.querySelector('i');
                icon.classList.add('fa-bars');
                icon.classList.remove('fa-xmark');
            }
        });
    });
    // ===============================
    // 3. FAQ Accordion
    // ===============================
    const faqQuestions = document.querySelectorAll('.faq-question');
    faqQuestions.forEach(question => {
        question.addEventListener('click', () => {
            const faqItem = question.parentElement;
            document.querySelectorAll('.faq-item')
            .forEach(item => {
                if(item !== faqItem) {
                    item.classList.remove('active');
                }
            });
            faqItem.classList.toggle('active');
        });
    });
    // ===============================
    // 4. Navbar Shadow On Scroll
    // ===============================
    const navbar = document.getElementById('navbar');
    window.addEventListener('scroll', () => {
        if(window.scrollY > 50) {
            navbar.style.boxShadow =
            '0 4px 20px rgba(0,0,0,0.08)';
        }
        else {
            navbar.style.boxShadow = 'none';
        }
    });
});