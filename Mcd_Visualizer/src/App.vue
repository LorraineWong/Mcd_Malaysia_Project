<template>
  <div>
    <h1 style="text-align:center; margin-top:24px;">
      🍔 McDonald's Outlets in Kuala Lumpur, Malaysia
    </h1>
    <!-- Centered searchbox under title -->
    <div style="display: flex; justify-content: center; margin-bottom: 6px;">
      <OutletSearchBox @search="handleSearch" />
    </div>
    <ChatBox />
    <MapView :focusedOutletId="focusedOutletId" />
    <footer style="text-align:center; margin-top:24px; color:gray;">
      Outlets in Kuala Lumpur • Powered by FastAPI & Mapbox
    </footer>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import ChatBox from './components/ChatBox.vue'
import MapView from './components/MapView.vue'
import OutletSearchBox from './components/OutletSearchBox.vue'
import { API_URL } from './apiConfig'

// KEY: Declare the focused outlet id as a reactive ref
const focusedOutletId = ref(null)

// Util: Set to null, then to ID, to force MapView watcher to always trigger
function focusOutlet(id) {
  focusedOutletId.value = null
  nextTick(() => {
    focusedOutletId.value = id
  })
}

// Handles search and finds the matching outlet's ID
async function handleSearch(name) {
  const res = await fetch(`${API_URL}/outlets`)
  const outlets = await res.json()
  // Case-insensitive partial match
  const found = outlets.find(
    o => o.name.toLowerCase().includes(name.toLowerCase())
  )
  if (found) {
    focusOutlet(found.id)
  } else {
    alert("No matching outlet found!")
    focusOutlet(null)
  }
}
</script>
