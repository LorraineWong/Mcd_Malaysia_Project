<template>
  <div>
    <h1 style="text-align:center; margin-top:24px;">
      🍔 McDonald's Outlets in Kuala Lumpur, Malaysia
    </h1>
    <ChatBox />
    <MapView />
    <footer style="text-align:center; margin-top:24px; color:gray;">
      Outlets in Kuala Lumpur • Powered by FastAPI & Mapbox
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ChatBox from './components/ChatBox.vue'
import MapView from './components/MapView.vue'

</script>

<style>
.mapboxgl-popup-content a {
  color: #222 !important;
  text-decoration: none !important;
  font-size: 12px;
}
.mapboxgl-popup-content a:hover {
  color: #555 !important;
  text-decoration: none !important;
}
</style>
