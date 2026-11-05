<template>
  <section class="story-section">
    <div class="story-container">
      <div class="story-layout">
        <div class="story-image-wrapper">
          <div class="image-container">
            <img 
              src="@/assets/images/Gemini_Generated_Image_oen81qoen81qoen8.png" 
              alt="Our Story" 
              class="story-image"
            >
            <div class="image-overlay"></div>
          </div>
        </div>
        
        <div class="story-content">
          <div class="story-header">
            <h2 class="story-title">Our Story</h2>
            <div class="story-line"></div>
          </div>
          
          <p class="story-text">
            SkillGig IT was born from a simple observation: developers help each other every day on platforms like Stack Overflow, GitHub, and Reddit. SkillGig focuses that help around specific IT project questions and follow-up conversations.
          </p>
          
          <p class="story-text">
            In 2025, we set out to create a dedicated space where IT professionals could not only ask and answer questions, but also work together through chat, share knowledge across all IT disciplines, and build meaningful connections. We wanted to make expert help accessible to everyone, from students taking their first coding steps to experienced developers facing complex architectural decisions.
          </p>
          
          <p class="story-text story-text-highlight">
            SkillGig brings question authors and IT specialists together to share practical knowledge and support one another.
          </p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
// Компонент не требует логики
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Sofia+Sans:wght@300;400;500;600;700;800;900&display=swap');

.story-section {
  width: 100%;
  background: #FFFFFF;
  padding: 3rem 2rem;
  font-family: 'Sofia Sans', Arial, Helvetica, sans-serif;
}

.story-container {
  max-width: 1400px;
  margin: 0 auto;
}

.story-header {
  margin-bottom: 0rem;
}

.story-title {
  font-size: 3rem;
  font-weight: 700;
  color: #000000;
  margin: 0 0 1rem 0;
  line-height: 1;
  letter-spacing: -0.02em;
}

.story-line {
  width: 80px;
  height: 5px;
  background: #4CAF4F;
  margin: 0;
  border-radius: 3px;
}

.story-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
  align-items: center;
}

.story-image-wrapper {
  position: relative;
  width: 85%;
  margin-left: 4%;
}

.image-container {
  position: relative;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.image-container:hover {
  transform: translateY(-5px);
  box-shadow: 0 25px 70px rgba(76, 175, 79, 0.2);
}

.story-image {
  width: 100%;
  height: auto;
  display: block;
  border-radius: 10px;
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(76, 175, 79, 0.1) 0%, transparent 50%);
  border-radius: 20px;
  pointer-events: none;
}

.story-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.story-content .story-header {
  margin-bottom: 2rem;
}

.story-text {
  font-size: 1.2rem;
  font-weight: 400;
  color: #4D4D4D;
  line-height: 1.7;
  margin: 0;
}

.story-text-highlight {
  font-weight: 500;
  color: #000000;
  font-size: 1.2rem;
  position: relative;
  padding-left: 1.5rem;
}

.story-text-highlight::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background: #4CAF4F;
  border-radius: 2px;
}

/* Адаптивность */
@media (max-width: 968px) {
  .story-section {
    padding: 6rem 2rem;
  }

  .story-content .story-header {
    margin-bottom: 2rem;
  }

  .story-title {
    font-size: 2.5rem;
  }

  .story-layout {
    grid-template-columns: 1fr;
    gap: 4rem;
  }

  .story-text {
    font-size: 1.125rem;
    line-height: 1.8;
  }

  .story-text-highlight {
    font-size: 1.2rem;
  }
}

@media (max-width: 768px) {
  .story-section {
    padding: 5rem 1.5rem;
  }

  .story-content .story-header {
    margin-bottom: 2rem;
  }

  .story-title {
    font-size: 2rem;
    margin-bottom: 0.75rem;
  }

  .story-line {
    width: 80px;
    height: 4px;
  }

  .story-layout {
    gap: 3rem;
  }

  .image-container {
    border-radius: 16px;
  }

  .story-image {
    border-radius: 16px;
  }

  .image-overlay {
    border-radius: 16px;
  }

  .story-content {
    gap: 1.5rem;
  }

  .story-text {
    font-size: 1rem;
    line-height: 1.7;
  }

  .story-text-highlight {
    font-size: 1.1rem;
    padding-left: 1.25rem;
  }
}

@media (max-width: 480px) {
  .story-section {
    padding: 4rem 1rem;
  }

  .story-title {
    font-size: 2rem;
  }

  .story-line {
    width: 60px;
    height: 3px;
  }

  .story-text {
    font-size: 0.95rem;
    line-height: 1.6;
  }

  .story-text-highlight {
    font-size: 1rem;
    padding-left: 1rem;
  }

  .story-text-highlight::before {
    width: 3px;
  }
}
</style>

