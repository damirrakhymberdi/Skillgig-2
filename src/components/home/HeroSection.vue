<template>
    <section class="hero-section">
      <div id="carouselExampleIndicators" class="carousel slide">
        <!-- Indicators -->
        <div class="carousel-indicators">
          <button
            v-for="(slide, index) in slides"
            :key="index"
            type="button"
            :class="{ active: currentSlide === index }"
            :aria-current="currentSlide === index ? 'true' : 'false'"
            :aria-label="`Slide ${index + 1}`"
            @click="goToSlide(index)"
          ></button>
        </div>
  
        <!-- Slides -->
        <div class="carousel-inner">
          <div
            v-for="(slide, index) in slides"
            :key="index"
            class="carousel-item"
            :class="{ active: currentSlide === index }"
          >
            <img :src="slide.background" class="d-block w-100" :alt="slide.title">
            <div class="carousel-caption">
              <h1 class="hero-title" :class="slide.titleClass">
                <template v-if="slide.titlePart1">
                  <span :class="slide.titlePart1Class">{{ slide.titlePart1 }}</span>
                  <span class="text-gray">{{ slide.titlePart2 }}</span>
                  <br>
                  <span class="text-gray">{{ slide.titlePart3 }}</span>
                  <span class="text-yellow" :class="slide.titlePart4Class">{{ slide.titlePart4 }}</span>
                </template>
                <template v-else>
                  {{ slide.title }}
                  <span v-if="slide.titlePart2" :class="slide.titlePart2Class">{{ slide.titlePart2 }}</span>
                </template>
              </h1>
              <p v-if="slide.subtitle" class="hero-subtitle">
                {{ slide.subtitle }}
              </p>
              <RouterLink 
                :to="slide.buttonLink" 
                class="hero-register-btn" 
                :class="slide.buttonClass"
              >
                {{ slide.buttonText }}
              </RouterLink>
            </div>
          </div>
        </div>
  
        <!-- Controls -->
        <button class="carousel-control-prev" type="button" aria-label="Previous slide" @click="prevSlide">
          <span class="carousel-control-prev-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Previous</span>
        </button>
        <button class="carousel-control-next" type="button" aria-label="Next slide" @click="nextSlide">
          <span class="carousel-control-next-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Next</span>
        </button>
      </div>
    </section>
  </template>
  
<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { RouterLink } from 'vue-router'

const currentSlide = ref(0)
let autoSlideInterval = null
  
  // Импорт изображений
  import heroImage1 from '@/assets/images/Hero Section.png'
  import heroImage2 from '@/assets/images/Hero Section2.png'
  import heroImage3 from '@/assets/images/Hero section3.png'
  
  const slides = [
    {
      title: 'Get Help with Any IT Challenge',
      subtitle: 'People quickly solve IT project issues',
      buttonText: 'Get started',
      buttonLink: '/questions',
      background: heroImage1,
      titleClass: 'text-yellow',
      buttonClass: 'btn-yellow'
    },
    {
      title: 'IT specialists gain experience and build their portfolios',
      subtitle: null,
      buttonText: 'Get started',
      buttonLink: '/questions',
      background: heroImage2,
      titleClass: 'text-white',
      buttonClass: 'btn-yellow'
    },
    {
      title: null,
      titlePart1: 'Knowledge',
      titlePart2: ' sharing and',
      titlePart3: 'mutual ',
      titlePart4: 'support',
      subtitle: null,
      buttonText: 'Get started',
      buttonLink: '/questions',
      background: heroImage3,
      titleClass: '',
      titlePart1Class: 'text-yellow',
      titlePart4Class: 'text-yellow',
      buttonClass: 'btn-yellow'
    }
  ]
  
const goToSlide = (index) => {
  currentSlide.value = index
}

const nextSlide = () => {
  currentSlide.value = (currentSlide.value + 1) % slides.length
}

const prevSlide = () => {
  currentSlide.value = currentSlide.value === 0 ? slides.length - 1 : currentSlide.value - 1
}

// Автоматты ауысу функциясы
const startAutoSlide = () => {
  autoSlideInterval = setInterval(() => {
    nextSlide()
  }, 4500) // 4.5 секунд сайын ауысады
}

// Автоматты ауысуды тоқтату
const stopAutoSlide = () => {
  if (autoSlideInterval) {
    clearInterval(autoSlideInterval)
    autoSlideInterval = null
  }
}

// Компонент монтталғанда автоматты ауысуды бастау
onMounted(() => {
  if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    startAutoSlide()
  }
})

// Компонент демонтталғанда автоматты ауысуды тоқтату
onUnmounted(() => {
  stopAutoSlide()
})
  </script>
  
  <style scoped>
  /* Hero Section */
  .hero-section {
    width: 100%;
    position: relative;
    overflow: hidden;
  }
  
  /* Carousel */
  .carousel {
    position: relative;
    width: 100%;
    height: 94vh;
    min-height: 600px;
  }
  
  .carousel-inner {
    position: relative;
    width: 100%;
    height: 100%;
    overflow: hidden;
  }
  
  /* Carousel Item */
  .carousel-item {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    opacity: 0;
    transition: opacity 0.6s ease-in-out;
    display: block;
  }
  
  .carousel-item.active {
    opacity: 1;
    position: relative;
  }
  
  .carousel-item img {
    width: 100%;
    height: 100%;
    object-fit: cover;  
    opacity: 2;
  }
  
  /* Carousel Caption */
  .carousel-caption {
    position: absolute;
    top: 50%;
    left: 10%;
    transform: translateY(-50%);
    text-align: left;
    z-index: 20;
    max-width: 1000px;
    padding: 0;
    
  }
  
  /* Hero Title */
  .hero-title {
    font-size: 4.1rem;
    font-weight: 600;
    line-height: 1.2;
    margin-bottom: 2rem;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
    font-family: Arial, Helvetica, sans-serif;   
  }
  
  .hero-title.text-yellow {
    color: #4CAF4F;
    margin-bottom: -1rem;
  }
  
  .hero-title.text-white {
    color: #FFFFFF;
  }
  
  .hero-title.text-gray {
    color: #E0E0E0; /* Бело-серый цвет */
  }
  
  .hero-title .text-yellow-green {
    color: #4CAF4F;
  }
  
  .hero-title span {
    display: inline;
    font-size: inherit;
    font-weight: inherit;
    line-height: inherit;
  }
  
  .hero-title .text-gray {
    color: #E0E0E0;
    font-weight: 600; /* Бело-серый цвет */
  }
  
  .hero-title .text-yellow {
    color: #4CAF4F;
  }
  
  /* Hero Subtitle */
  .hero-subtitle {
    font-size: 2rem;
    color: #FFFFFF;
    margin-bottom: 2rem;
    text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.5);
    font-family: Arial, Helvetica, sans-serif;
  }
  
  /* Register Button */
  .hero-register-btn {
    display: inline-block;
    padding: 0.75rem 2.5rem;
    font-size: 1.25rem;
    font-weight: 600;
    border-radius: 8px;
    text-decoration: none;
    transition: all 0.3s ease;
    border: none;
    cursor: pointer;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    position: relative;
    z-index: 21;
    font-family: Arial, Helvetica, sans-serif;
  }
  
  .hero-register-btn.btn-yellow {
    background-color: #4CAF4F;
    color: #FFFFFF;
  }
  
  .hero-register-btn.btn-yellow:hover {
    background-color: #45a049;
    transform: translateY(-2px);
    box-shadow: 0 6px 8px rgba(0, 0, 0, 0.4);
  }
  
  .hero-register-btn.btn-brown {
    background-color: #4CAF4F;
    color: #FFFFFF;
  }
  
  .hero-register-btn.btn-brown:hover {
    background-color: #45a049;
    transform: translateY(-2px);
    box-shadow: 0 6px 8px rgba(0, 0, 0, 0.4);
  }
  
  /* Carousel Indicators */
  .carousel-indicators {
    position: absolute;
    bottom: 30px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    gap: 12px;
    z-index: 15;
    margin: 0;
    padding: 0;
    list-style: none;
  }
  
  .carousel-indicators button {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    border: none;
    background-color: rgba(255, 255, 255, 0.5);
    cursor: pointer;
    transition: all 0.3s ease;
    padding: 0;
    text-indent: -999px;
    overflow: hidden;
  }
  
  .carousel-indicators button:hover {
    background-color: rgba(255, 255, 255, 0.7);
    transform: scale(1.2);
  }
  
  .carousel-indicators button.active {
    background-color: #4CAF4F;
    width: 32px;
    border-radius: 6px;
  }
  
  /* Carousel Controls */
  .carousel-control-prev,
  .carousel-control-next {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    z-index: 15;
    width: 50px;
    height: 50px;
    background-color: rgba(0, 0, 0, 0.5);
    border: none;
    border-radius: 50%;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .carousel-control-prev {
    left: 20px;
  }
  
  .carousel-control-next {
    right: 20px;
  }
  
  .carousel-control-prev:hover,
  .carousel-control-next:hover {
    background-color: rgba(0, 0, 0, 0.7);
  }
  
  .carousel-control-prev-icon,
  .carousel-control-next-icon {
    width: 20px;
    height: 20px;
    background-size: 100% 100%;
    background-repeat: no-repeat;
    display: inline-block;
  }
  
  .carousel-control-prev-icon {
    background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16' fill='%23fff'%3e%3cpath d='M11.354 1.646a.5.5 0 0 1 0 .708L5.707 8l5.647 5.646a.5.5 0 0 1-.708.708l-6-6a.5.5 0 0 1 0-.708l6-6a.5.5 0 0 1 .708 0z'/%3e%3c/svg%3e");
  }
  
  .carousel-control-next-icon {
    background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16' fill='%23fff'%3e%3cpath d='M4.646 1.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1 0 .708l-6 6a.5.5 0 0 1-.708-.708L10.293 8 4.646 2.354a.5.5 0 0 1 0-.708z'/%3e%3c/svg%3e");
  }
  
  .visually-hidden {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
  }
  
  /* Responsive Design */
  @media (max-width: 768px) {
    .carousel-caption {
      left: 10%;
      right: 10%;
      max-width: 90%;
    }
  
    .hero-title {
      font-size: 2.5rem;
    }
  
    .hero-subtitle {
      font-size: 1.2rem;
    }
  
    .hero-register-btn {
      padding: 0.875rem 2rem;
      font-size: 1.1rem;
    }
  
    .carousel-control-prev,
    .carousel-control-next {
      width: 40px;
      height: 40px;
    }
  }
  
  @media (max-width: 480px) {
    .carousel-caption {
      left: 8%;
      right: 8%;
      max-width: none;
      text-align: left;
    }

    .hero-title {
      font-size: clamp(2.25rem, 10vw, 3rem);
      line-height: 1.12;
      margin-bottom: 1.5rem;
    }

    .hero-subtitle {
      font-size: 1.15rem;
    }

    .carousel {
      min-height: 500px;
    }

    /* Кнопкиларды жасыру */
    .carousel-control-prev,
    .carousel-control-next {
      display: none !important;
    }

    /* Register батырмасын ортаға туралау */
    .hero-register-btn {
      margin: 0 auto;
      display: block;
      width: fit-content;
    }
  }

  @media (prefers-reduced-motion: reduce) {
    .carousel-item {
      transition: none;
    }
  }
  </style>
