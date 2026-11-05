<template>
  <div class="faq-page">
    <div class="faq-container">
      <h1 class="faq-title">Frequently Asked Questions</h1>

      <div class="faq-layout">
        <!-- Левая колонка с вопросами -->
        <main class="faq-content">
          <section
            v-for="item in faqItems"
            :key="item.id"
            :id="item.id"
            class="faq-item"
          >
            <h2 class="faq-question">{{ item.question }}</h2>
            <div class="faq-answer">{{ item.answer }}</div>
          </section>

          <!-- FAQ Footer -->
          <div class="faq-footer">
            <p class="faq-footer-copyright">© {{ currentYear }} SkillGig. All rights reserved.</p>
            <div class="faq-footer-contacts">
              <p class="faq-footer-contact-item">
                <span class="faq-footer-label">Phone:</span>
                <span class="faq-footer-value">8776 603 10 92</span>
              </p>
              <p class="faq-footer-contact-item">
                <span class="faq-footer-label">Email:</span>
                <a href="mailto:damirrakhymberdi662@gmail.com" class="faq-link">damirrakhymberdi662@gmail.com</a>
              </p>
            </div>
          </div>
        </main>

        <!-- Правая колонка с содержанием - FIXED -->
        <aside class="faq-sidebar">
          <div class="sidebar-sticky">
            <h3 class="sidebar-title">СОДЕРЖАНИЕ</h3>
            <nav class="sidebar-nav">
              <a
                v-for="item in faqItems"
                :key="item.id"
                :href="`#${item.id}`"
                :class="{ 'active-question': activeId === item.id }"
                class="sidebar-link"
                @click.prevent="scrollToQuestion(item.id)"
              >
                {{ item.question }}
              </a>
            </nav>
          </div>
        </aside>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const currentYear = new Date().getFullYear()
const activeId = ref('')

const faqItems = ref([
  {
    id: 'what-is-skillgig-it',
    question: 'What is SkillGig IT?',
    answer: 'SkillGig IT is a comprehensive platform designed to connect people facing IT challenges with experienced professionals who can help solve them. Whether you\'re struggling with a bug in your web application, need design advice for your mobile app, or require assistance with backend optimization, our community of developers is here to assist you completely free of charge.\n\nWe support all major IT categories including Web Development, Mobile Development, UI/UX Design, Backend/Database, AI/ML, DevOps/Infrastructure, Game Development, and Security/Blockchain. The platform operates on a simple principle: knowledge sharing and mutual support within the IT community.'
  },
  {
    id: 'how-does-platform-work',
    question: 'How does the platform work?',
    answer: 'Create an account, post a question with enough detail to explain the problem, and wait for community members with expert profiles to answer. You can review the answers on the question page. If you need to discuss a solution privately, use the message button on the question or answer to open a chat. The question author can mark the question as resolved.'
  },
  {
    id: 'is-skillgig-really-free',
    question: 'Is SkillGig really free?',
    answer: 'Yes. Asking questions and sharing answers are currently free. The project does not currently offer paid consultations or subscriptions.'
  },
  {
    id: 'who-can-use-skillgig',
    question: 'Who can use SkillGig IT?',
    answer: 'Anyone can create an account and ask about an IT problem. Accounts with an expert profile can also answer questions. Keep questions and answers focused on projects where you can share context and useful details.'
  },
  {
    id: 'what-questions-can-i-ask',
    question: 'What kind of questions can I ask?',
    answer: 'You can ask questions about virtually any IT-related problem you\'re facing in your own projects. This includes website bugs like broken layouts or JavaScript errors, mobile application problems such as performance issues or navigation bugs, design questions seeking feedback on UI/UX or color schemes, backend challenges like API design or database optimization, and DevOps issues including Docker setup or CI/CD pipelines.\n\nThe key requirement is that your question should be about a real problem in a project you\'re actually working on. You should provide context, show what you\'ve tried, and be specific about where you\'re stuck. Questions about game development, AI/ML integration, and security concerns are also welcome.'
  },
  {
    id: 'what-questions-not-allowed',
    question: 'What questions are NOT allowed?',
    answer: 'We strictly prohibit questions that violate academic integrity. This means you cannot ask for help with homework assignments, laboratory work, course projects that are meant to be completed individually, exam questions, or any academic work where you\'re expected to demonstrate your own learning.\n\nFor example, asking "Please create a complete to-do app for me because it\'s my lab assignment" is not allowed. Similarly, "Write my Python exam code" or "Build my entire course project" are prohibited. The reason is simple: academic work is designed to help you learn. However, if you\'re working on your own personal project outside of academic requirements, that\'s perfectly acceptable.'
  },
  {
    id: 'how-write-good-question',
    question: 'How do I write a good question?',
    answer: 'Writing a good question significantly increases your chances of getting helpful answers quickly. Start with a specific, descriptive title that summarizes the problem, like "React mobile menu doesn\'t open in Chrome but works in Safari" rather than just "Menu broken". In the description, explain what you\'re trying to achieve, what\'s currently happening instead, and what you\'ve already tried to fix it.\n\nInclude relevant code snippets, but don\'t paste your entire codebase. Show the specific function or component where the issue occurs. If possible, provide a GitHub repository link or CodePen demo. Add screenshots or screen recordings of the error. Select the correct category and add relevant technology tags. Finally, indicate the difficulty level honestly.'
  },
  {
    id: 'how-long-answers',
    question: 'How long does it take to get answers?',
    answer: 'There is no guaranteed response time. It depends on whether community members with relevant experience are available. A clear title, useful context, and the steps you have already tried can make your question easier to answer.'
  },
  {
    id: 'what-if-multiple-answers',
    question: 'What if I get multiple answers?',
    answer: 'Review each answer and compare how clearly it explains a solution to your specific problem. You can message an answer author privately from the question page if you want to discuss their suggestion. The project does not currently provide expert ratings.'
  },
  {
    id: 'can-edit-delete-question',
    question: 'Can I edit or delete my question?',
    answer: 'The question author can edit or delete their own question from its page. Deleting a question also removes its answers and chat messages. Make sure you want to remove that discussion before confirming deletion.'
  },
  {
    id: 'how-register-as-expert',
    question: 'How do I register as an expert?',
    answer: 'Choose the IT specialist account type when registering to create an expert profile and answer questions. You can add or update your skills, experience, and other profile details from your profile settings. Existing accounts can create an expert profile there as well.'
  },
  {
    id: 'requirements-to-become-expert',
    question: 'What are the requirements to become an expert?',
    answer: 'An expert profile is required to answer questions. Choose the IT specialist account type during signup, or create an expert profile later from profile settings. There is no rating or certification system in the current version, so describe your experience honestly.'
  },
  {
    id: 'do-i-get-paid',
    question: 'Do I get paid for answering questions?',
    answer: 'No. Answering questions is currently voluntary, and the platform does not process payments or offer paid consultations.'
  },
  {
    id: 'how-many-questions-can-answer',
    question: 'How many questions can I answer?',
    answer: 'There is no fixed answer limit in the current version. Focus on questions where you can give a clear, useful response.'
  },
  {
    id: 'how-rating-calculated',
    question: 'How is my rating calculated?',
    answer: 'The current version does not have expert ratings or reviews. You can describe your experience in your profile, and question pages show whether a question has been resolved.'
  },
  {
    id: 'how-chat-works',
    question: 'How does the chat work?',
    answer: 'The question author and answer authors can open a private conversation using the message button on the question page. Chat supports text messages. New messages refresh automatically about every five seconds while the chat is open. File uploads, read receipts, and instant push notifications are not currently available.'
  },
  {
    id: 'is-my-data-safe',
    question: 'Is my data safe?',
    answer: 'Passwords are stored as bcrypt hashes, and public user profiles do not expose email addresses. The app validates external link schemes and displays question and answer text without interpreting it as HTML. HTTPS depends on the site deployment; do not share passwords or sensitive personal information in public questions.'
  }
])

let observer = null

onMounted(() => {
  // Настройка Intersection Observer
  const options = {
    root: null,
    rootMargin: '-100px 0px -60% 0px',
    threshold: 0.1
  }

  observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        activeId.value = entry.target.id
      }
    })
  }, options)

  // Наблюдаем за всеми вопросами
  faqItems.value.forEach((item) => {
    const element = document.getElementById(item.id)
    if (element) {
      observer.observe(element)
    }
  })

  // Устанавливаем первый вопрос как активный при загрузке
  if (faqItems.value.length > 0) {
    activeId.value = faqItems.value[0].id
  }
})

onUnmounted(() => {
  if (observer) {
    observer.disconnect()
  }
})

const scrollToQuestion = (id) => {
  const element = document.getElementById(id)
  if (element) {
    const yOffset = -100
    const y = element.getBoundingClientRect().top + window.pageYOffset + yOffset
    window.scrollTo({ top: y, behavior: 'smooth' })
    
    // Обновляем активный ID
    setTimeout(() => {
      activeId.value = id
    }, 500)
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Sofia+Sans:wght@300;400;500;600;700;800;900&display=swap');

.faq-page {
  min-height: 100vh;
  background: #F5F7FA;
  color: #ffffff;
  font-family: 'Sofia Sans', Arial, Helvetica, sans-serif;
  padding: 9rem 5rem;
}

.faq-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
}

.faq-title {
  font-size: 3rem;
  font-weight: 700;
  color: #000000;
  margin: 0 0 4rem 0;
  line-height: 1.2;
  border-bottom: 1px solid rgba(15, 174, 31, 0.982);
  padding-bottom: 2rem;
  width: 68.8%;
}

.faq-layout {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 3rem;
  align-items: start;
  position: relative;
}

/* Левая колонка - Контент (СКРОЛЛИТСЯ) */
.faq-content {
  max-width: 900px;
}

.faq-item {
  margin-bottom: 4rem;
  scroll-margin-top: 120px;
  padding-bottom: 2rem;
  border-bottom: 1px solid rgba(15, 174, 31, 0.982);
}


.faq-item:last-of-type {
  border-bottom: none;
  padding-bottom: 0;
}

.faq-question {
  font-size: 2rem;
  font-weight: 600;
  color: #000000;
  margin: 0 0 1.5rem 0;
  line-height: 1.3;
}

.faq-answer {
  font-size: 1.125rem;
  line-height: 1.3;
  color: #4D4D4D;
  white-space: pre-line;
}

/* FAQ Footer */
.faq-footer {
  margin-top: 4rem;
  padding-top: 2rem;
  border-top: 1px solid rgba(0, 83, 23, 0.477);
}

.faq-footer-copyright {
  font-size: 0.9rem;
  color: #888888;
  margin: 0 0 1rem 0;
}

.faq-footer-contacts {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.faq-footer-contact-item {
  font-size: 0.9rem;
  color: #000000;
  margin: 0;
  display: flex;
  gap: 0.5rem;
}

.faq-footer-label {
  font-weight: 500;
  color: #000000;
}

.faq-footer-value {
  color: #4D4D4D;
}

.faq-footer-contact-item .faq-link {
  color: #42b883;
  text-decoration: none;
  transition: color 0.3s ease;
}

.faq-footer-contact-item .faq-link:hover {
  color: #35a372;
  text-decoration: underline;
}

/* Правая колонка - Содержание (НЕ СКРОЛЛИТСЯ - FIXED) */
.faq-sidebar {
  width: 300px;
  position: relative;
}

.sidebar-sticky {
  position: fixed;
  top: 120px;
  width: 300px;
  max-height: calc(100vh - 160px);
  overflow-y: auto;
  padding-right: 1rem;
}

/* Кастомный скроллбар для sidebar */
.sidebar-sticky::-webkit-scrollbar {
  width: 4px;
}

.sidebar-sticky::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 4px;
}

.sidebar-sticky::-webkit-scrollbar-thumb {
  background: rgba(66, 184, 131, 0.3);
  border-radius: 4px;
}

.sidebar-sticky::-webkit-scrollbar-thumb:hover {
  background: rgba(66, 184, 131, 0.5);
}

.sidebar-title {
  font-size: 0.875rem;
  font-weight: 700;
  color: #000000;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin: 0 0 1.5rem 0;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 0rem;
}

.sidebar-link {
  font-size: 0.85rem;
  color: #4D4D4D;
  text-decoration: none;
  padding: 0.2rem 0;
  padding-left: 0;
  border-left: 3px solid transparent;
  transition: all 0.3s ease;
  line-height: 1.3;
  cursor: pointer;
  display: block;
  font-weight: 600;
}

.sidebar-link:hover {
  color: #4D4D4D;
  padding-left: 8px;
}

.sidebar-link.active-question {
  border-left-color: #42b883;
  padding-left: 10px;
  color: #000000;
  font-weight: 500;
  border-radius: 2px;
}

/* Адаптивность */
@media (max-width: 1200px) {
  .faq-layout {
    grid-template-columns: 1fr 260px;
    gap: 3rem;
  }

  .faq-sidebar {
    width: 260px;
  }
}

@media (max-width: 968px) {
  .faq-layout {
    grid-template-columns: 1fr;
    gap: 0;
  }

  .faq-sidebar {
    width: 100%;
    order: -1;
    margin-bottom: 3rem;
  }

  .sidebar-sticky {
    position: relative;
    top: 0;
    max-height: none;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    padding-bottom: 2rem;
    padding-right: 0;
  }

  .sidebar-nav {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0.5rem;
  }

  .sidebar-link {
    border-left: none;
    border-bottom: 2px solid transparent;
    padding-left: 0;
  }

  .sidebar-link:hover {
    padding-left: 0;
  }

  .sidebar-link.active-question {
    border-left: none;
    border-bottom-color: #42b883;
    padding-left: 0;
    padding-bottom: 0.5rem;
  }
}

@media (max-width: 768px) {
  .faq-page {
    padding: 2rem 0;
  }

  .faq-container {
    padding: 0 1.5rem;
  }

  .faq-title {
    font-size: 2.5rem;
    margin-bottom: 2rem;
  }

  .faq-item {
    margin-bottom: 3rem;
    scroll-margin-top: 80px;
  }

  .faq-question {
    font-size: 1.5rem;
  }

  .faq-answer {
    font-size: 1rem;
  }

  .sidebar-nav {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .faq-container {
    padding: 0 1rem;
  }

  .faq-title {
    font-size: 2rem;
  }

  .faq-question {
    font-size: 1.375rem;
  }

  .faq-answer {
    font-size: 0.9375rem;
  }
}
</style>
