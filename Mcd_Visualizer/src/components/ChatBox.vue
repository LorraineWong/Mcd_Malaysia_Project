<template>
  <div>
    <!-- Chatbox -->
    <transition name="chatbox-fade">
      <div
        v-if="isOpen"
        class="chatbox-container"
        :style="{ bottom: '120px', right: '40px' }"
      >
        <div class="chatbox-header">
          <span class="material-icons icon-awesome">auto_awesome</span>
          <span class="chatbox-title">Ask Chatbot</span>
          <button class="close-btn" @click="toggleChat" title="Close">
            <span class="material-icons">close</span>
          </button>
        </div>
        <div class="chat-messages" ref="messagesEnd">
          <div v-for="(msg, idx) in messages" :key="idx" :class="msg.sender">
            <template v-if="msg.sender === 'bot'">
              <span class="material-icons msg-bot-icon">auto_awesome</span>
              <span v-html="msg.text"></span>
            </template>
            <template v-else>
              <span class="msg-user-text">{{ msg.text }}</span>
            </template>
          </div>
          <!-- Loading indicator shows while waiting for API -->
          <div v-if="loading" class="bot loading-bot-msg">
            <span class="material-icons msg-bot-icon">auto_awesome</span>
            <span class="loading-dots">
              <span>.</span><span>.</span><span>.</span>
            </span>
            <!-- <span class="loading-tip">Bot is thinking...</span> -->
          </div>
        </div>
        <form class="chat-input-row" @submit.prevent="sendMessage">
          <input
            v-model="userInput"
            type="text"
            placeholder="Type your question here..."
            autocomplete="off"
            :disabled="loading"
          />
          <button :disabled="loading || !userInput.trim()">
        <span class="material-icons" style="font-size: 1.5em; color: #2492FF; vertical-align: middle;">
            send
        </span>
        </button>
        </form>
      </div>
    </transition>

    <!-- Floating Button, always visible, never covered -->
    <button class="chatbox-toggle" @click="toggleChat" title="Chat">
      <span class="material-icons">auto_awesome</span>
    </button>
  </div>
</template>

<script setup>
import { ref, nextTick } from "vue";
import axios from "axios";
import { API_URL } from '../apiConfig'

const isOpen = ref(false);
const messages = ref([
  {
    sender: "bot",
    text:
      "Hello! Ask me about McDonald's outlets in Kuala Lumpur (e.g., features, birthday parties, 24 hours, etc.)",
  },
]);
const userInput = ref("");
const loading = ref(false);
const messagesEnd = ref(null);

function toggleChat() {
  isOpen.value = !isOpen.value;
  nextTick(scrollToBottom);
}

function scrollToBottom() {
  nextTick(() => {
    if (messagesEnd.value) {
      messagesEnd.value.scrollTop = messagesEnd.value.scrollHeight;
    }
  });
}

async function sendMessage() {
  const question = userInput.value.trim();
  if (!question) return;
  messages.value.push({ sender: "user", text: question });
  userInput.value = "";
  loading.value = true;
  scrollToBottom();

  try {
    const response = await axios.post(`${API_URL}/ask`, { question });
    const data = response.data;
    let reply = "";
    if (data.outlets && data.outlets.length > 0) {
      reply =
        `<b>Found ${data.outlets.length} outlets in Kuala Lumpur with <span style="color:#2492ff">${data.feature_desc}</span><br>Matching outlets:</b><ul style="margin:0;padding-left:16px;">` +
        data.outlets.map((name) => `<li>${name}</li>`).join("") +
        "</ul>";
    } else {
      reply = data.msg || "Sorry, I couldn't find a relevant answer.";
    }
    messages.value.push({ sender: "bot", text: reply });
  } catch (err) {
    messages.value.push({
      sender: "bot",
      text: "Sorry, there was an error processing your request.",
    });
  } finally {
    loading.value = false;
    scrollToBottom();
  }
}
</script>

<style scoped>
@import url("https://fonts.googleapis.com/icon?family=Material+Icons");

.chatbox-toggle {
  position: fixed;
  right: 40px;
  bottom: 32px;
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: linear-gradient(135deg, #2492ff 20%, #ffe76a 90%);
  color: #fff;
  border: none;
  box-shadow: 0 4px 24px #2492ff33;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.1rem;
  cursor: pointer;
  transition: background 0.2s;
  z-index: 10002;
}

.chatbox-container {
  position: fixed;
  height: 600px;
  right: 40px;
  bottom: 120px; /* Adjusted to avoid covering the button */
  width: 430px;
  max-height: 90vh;
  min-height: 340px;
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 6px 32px #0002;
  display: flex;
  flex-direction: column;
  z-index: 10001;
  animation: fadeInUp 0.18s;
  resize: both;
  overflow: auto;
}

@keyframes fadeInUp {
  0% {
    opacity: 0;
    transform: translateY(80px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

.chatbox-header {
  position: relative;
  padding: 18px 46px 12px 16px;
  font-size: 1.12em;
  font-weight: 600;
  border-bottom: 1.5px solid #f2f2f2;
  background: #f7faff;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 50px;
}
.icon-awesome {
  background: linear-gradient(135deg, #2492ff 20%, #ffe76a 90%);
  color: transparent;
  -webkit-background-clip: text;
  background-clip: text;
  font-size: 1.5em;
  margin-right: 7px;
  vertical-align: middle;
}
.chatbox-title {
  flex: 1;
  text-align: center;
  font-weight: 600;
  font-size: 1.07em;
  color: #1c293b;
  letter-spacing: 0.01em;
  padding-right: 16px;
}
.close-btn {
  position: absolute;
  right: 14px;
  top: 14px;
  background: none;
  border: none;
  color: #888;
  font-size: 1.42em;
  cursor: pointer;
  transition: color 0.18s;
  padding: 2px;
  line-height: 1;
  z-index: 2;
}
.close-btn:hover {
  color: #2492ff;
}

/* Messages area */
.chat-messages {
  min-height: 430px;
  max-height: 500px;
  overflow-y: auto;
  background: #f7f8fa;
  padding: 12px 10px 12px 10px;
  border-radius: 0 0 10px 10px;
  display: flex;
  flex-direction: column;
  gap: 7px;
}
.user {
  align-self: flex-end;
  background: #e6f0fa;
  color: #3260a8;
  border-radius: 16px 16px 0 16px;
  padding: 8px 15px;
  margin: 2px 0;
  max-width: 80%;
  word-break: break-word;
}
.bot {
  align-self: flex-start;
  background: #fff8de;
  color: #a87900;
  border-radius: 16px 16px 16px 0;
  padding: 8px 15px;
  margin: 2px 0;
  max-width: 94%;
  word-break: break-word;
  display: flex;
  align-items: flex-start;
  gap: 5px;
}
.msg-bot-icon {
  color: #2492ff;
  font-size: 1.2em;
  margin-right: 5px;
  margin-top: 1.5px;
}

.msg-user-text {
  display: block;
  color: #14498c;
  background: #e6f0fa;
  border-radius: 16px 16px 0 16px;
  padding: 7px 13px;
  font-size: 1em;
}

/* Input row */
.chat-input-row {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-top: 10px;
  padding-bottom: 7px;
}
input[type="text"] {
  width: 300px;
  min-width: 120px;
  max-width: 340px;
  flex: none;
  padding: 9px 14px;
  border-radius: 18px;
  border: 1px solid #e0e0e0;
  outline: none;
  font-size: 1rem;
  transition: border 0.2s;
  background: #f8f8f8;
  margin-right: 0;
}
input[type="text"]:focus {
  border: 1.5px solid #2492ff;
  background: #fffde9;
}
button {
  width: 56px;
  min-width: 50px;
  background: #ffd952;
  color: #222;
  border: none;
  border-radius: 18px;
  font-weight: 600;
  font-size: 1rem;
  padding: 0 0;
  cursor: pointer;
  transition: background 0.18s;
}
button[disabled] {
  opacity: 0.6;
  cursor: not-allowed;
}
.loading-bot-msg {
  align-self: flex-start;
  background: #fff8de;
  color: #2492ff;
  border-radius: 16px 16px 16px 0;
  padding: 8px 15px;
  margin: 2px 0;
  max-width: 70%;
  word-break: break-word;
  display: flex;
  align-items: center;
  gap: 9px;
  font-weight: 500;
  font-size: 1em;
  letter-spacing: .01em;
  opacity: 0.9;
}
.loading-dots span {
  animation: dots-blink 1.1s infinite;
  font-size: 1.4em;
  margin-right: 1px;
}
.loading-dots span:nth-child(2) { animation-delay: 0.2s; }
.loading-dots span:nth-child(3) { animation-delay: 0.4s; }
@keyframes dots-blink {
  0%, 80%, 100% { opacity: 0.3; }
  30% { opacity: 1; }
}
.loading-tip {
  color: #8ba7cb;
  margin-left: 8px;
  font-size: 0.95em;
}
</style>
