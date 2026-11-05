<template>
  <section class="team-section">
    <div class="team-container">
      <div class="team-header">
        <h2 class="team-title">Team</h2>
      </div>
  
      <div class="team-grid">
        <!-- 1 ряд: фото — текст — фото -->
        <div class="team-card photo-card photo-nuris">
            <img :src="nurisImage" alt="Team member" class="member-photo">
        </div>
        
        <div class="team-card text-card text-bazarbai">
          <h3 class="member-name">Bazarbai Nurassyl</h3>
          <p class="member-role">Backend Developer</p>
          <p class="member-bio">Backend specialist focused on building scalable and secure 
APIs. Expert in Node.js, PostgreSQL, and system architecture. 
Ensures the platform runs smoothly behind the scenes.</p>
        </div>
        
        <div class="team-card photo-card photo-damir">
          <img :src="teamImage" alt="Team member" class="member-photo">
        </div>
        
        <!-- 2 ряд: текст — фото — текст -->
        <div class="team-card text-card text-nurislam">
          <h3 class="member-name">Nurislam Zhetpisbay</h3>
          <p class="member-role">Fullstack Developer</p>
          <p class="member-bio">Experienced fullstack developer with expertise in both frontend and backend technologies. 
Proficient in modern web frameworks and databases. Passionate about building scalable 
applications and solving complex challenges.</p>
        </div>
        
        <div class="team-card photo-card">
          <img :src="buyrabasiImage"  alt="Team member" class="member-photo">
        </div>
        
        <div class="team-card text-card text-damir">
          <h3 class="member-name">Damir Rakhymberdi</h3>
          <p class="member-role">Frontend Developer</p>
          <p class="member-bio">Passionate about creating beautiful and intuitive user experiences. 
Specializes in modern web design and frontend development with Vue.js. 
Believes great design makes technology accessible to everyone. Has 3 years of experience in frontend development.</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import teamImage from '@/assets/images/Gemini_Generated_Image_oen81qoen81qoen8.png'
import buyrabasiImage from '@/assets/images/Buyrabasi.jpg'
import nurisImage from '@/assets/images/Nuris fullstack.jpg'
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Sofia+Sans:wght@300;400;500;600;700;800;900&display=swap');

.team-section {
  width: 100%;
  background: #FFFFFF;
  padding: 7rem 2rem;
  font-family: 'Sofia Sans', Arial, Helvetica, sans-serif;
  min-height: 100vh;
}

.team-container {
  max-width: 1200px;
  margin: 0 auto;
}

.team-header {
  text-align: center;
  margin-bottom: 5rem;
}

.team-title {
  font-size: 3.6rem;
  font-weight: 700;
  color: #4CAF4F;
  margin: 0 0 2rem 0;
  line-height: 1;
}

.team-description {
  font-size: 1rem;
  color: #4D4D4D;
  line-height: 1.6;
  margin: 0 auo;
  max-width: 800px;
  text-align: start;
}

.team-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: repeat(2, 1fr);
  gap: 0;
  width: 93%;
  margin: 0 auto;
}



.photo-card {
  padding: 0;
  display: flex;
  align-items: flex-start;
  justify-content: center;
}

.member-photo {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  display: block;
  margin-top: 0;
}

.text-card {
  padding: 2rem 2.5rem;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;

}


.member-name {
  font-size: 1.2rem;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 0.75rem 0;
  letter-spacing: 0.05em;
  line-height: 1.9;
}

.member-role {
  font-size: 0.9375rem;
  font-weight: 400;
  color: #4CAF4F;
  margin: 0 0 1rem 0;
  line-height: 1.4;
}

.member-bio {
  font-size: 0.875rem;
  line-height: 1.6;
  color: #4D4D4D;
  margin: 0;
}

@media (max-width: 968px) {
  .team-grid {
    grid-template-columns: repeat(2, 1fr);
    grid-template-rows: repeat(3, 1fr);
  }

  /* 968px-де де реттеу */
  .photo-nuris {
    order: 1;
  }

  .text-nurislam {
    order: 2;
  }

  .photo-damir {
    order: 3;
  }

  .text-damir {
    order: 4;
  }

  .photo-card:not(.photo-nuris):not(.photo-damir) {
    order: 5;
  }

  .text-bazarbai {
    order: 6;
  }
}

@media (max-width: 768px) {
  .team-section {
    padding: 3rem 1rem;
  }

  .team-title {
    font-size: 2.5rem;
  }

  .team-grid {
    grid-template-columns: 1fr;
    grid-template-rows: repeat(6, auto);
  }

  .team-card {
    min-height: 350px;
  }

  /* Мобильді версияда реттеу */
  .photo-nuris {
    order: 1;
  }

  .text-nurislam {
    order: 2;
  }

  .photo-damir {
    order: 3;
  }

  .text-damir {
    order: 4;
  }

  .photo-card:not(.photo-nuris):not(.photo-damir) {
    order: 5;
  }

  .text-bazarbai {
    order: 6;
  }

  .text-card {
    padding: 2rem 1.5rem;
  }
}

@media (max-width: 480px) {
  .team-title {
    font-size: 2rem;
  }

  .team-card {
    min-height: 300px;
  }

  .text-card {
    padding: 1.5rem 1rem;
  }
}
</style>
