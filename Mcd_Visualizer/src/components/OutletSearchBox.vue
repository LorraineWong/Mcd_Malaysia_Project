<template>
  <div class="outlet-searchbox" @click.stop>
    <div class="search-row">
      <input
        ref="inputEl"
        type="text"
        v-model="query"
        placeholder="Search outlet by name..."
        @input="onInput"
        @keydown.down.prevent="onArrowDown"
        @keydown.up.prevent="onArrowUp"
        @keydown.enter.prevent="onEnter"
        @focus="showDropdown = true"
        @blur="onBlur"
        autocomplete="off"
      />
      <button class="search-btn" @click="doSearch" :disabled="query.trim() === ''">
        <span class="material-icons">search</span>
      </button>
    </div>
    <ul v-if="showDropdown" class="dropdown">
      <li v-for="(item, i) in filtered" :key="item.id"
          :class="{ active: i === highlightedIdx }"
          @mousedown.prevent="select(item)"
      >
        {{ item.name }}
      </li>
      <li v-if="filtered.length === 0" class="no-result">No Results found</li>
    </ul>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'

const emit = defineEmits(['search'])
const inputEl = ref(null)
const query = ref('')
const showDropdown = ref(false)
const allOutlets = ref([])
const filtered = ref([])
const highlightedIdx = ref(-1)

// Fetch all outlets on mount
onMounted(async () => {
  const res = await fetch('http://127.0.0.1:8000/outlets')
  allOutlets.value = await res.json()
})

// Whenever query changes, filter results
watch(query, (val) => {
  if (!val.trim()) {
    filtered.value = []
    highlightedIdx.value = -1
    return
  }
  const q = val.toLowerCase()
  filtered.value = allOutlets.value.filter(
    o => o.name.toLowerCase().includes(q)
  )
  highlightedIdx.value = filtered.value.length ? 0 : -1
})

function onInput() {
  showDropdown.value = true
}

function onBlur() {
  setTimeout(() => { showDropdown.value = false }, 140)
}

// Keyboard: arrow down
function onArrowDown() {
  if (filtered.value.length === 0) return
  highlightedIdx.value = (highlightedIdx.value + 1) % filtered.value.length
}
// Keyboard: arrow up
function onArrowUp() {
  if (filtered.value.length === 0) return
  highlightedIdx.value = (highlightedIdx.value - 1 + filtered.value.length) % filtered.value.length
}
// Keyboard: enter
function onEnter() {
  if (filtered.value.length && highlightedIdx.value >= 0) {
    select(filtered.value[highlightedIdx.value])
  } else {
    doSearch()
  }
}
// Click/enter search
function doSearch() {
  if (filtered.value.length === 1) {
    select(filtered.value[0])
  } else if (query.value.trim() !== '') {
    // Try to find closest
    const q = query.value.toLowerCase()
    const found = allOutlets.value.find(o => o.name.toLowerCase() === q)
    if (found) {
      select(found)
    } else {
      emit('search', query.value)
    }
  }
}
// When user clicks on suggestion
function select(item) {
  query.value = item.name
  showDropdown.value = false
  emit('search', item.name)
}
</script>

<style scoped>
.outlet-searchbox {
  position: relative;
  width: 410px;
  margin: 0 auto;
}
.search-row {
  display: flex;
  align-items: center;
}
input[type="text"] {
  width: 330px;
  border-radius: 30px 0 0 30px;
  border: 1.5px solid #d7e6fb;
  font-size: 1.12em;
  padding: 12px 20px;
  outline: none;
  transition: border 0.2s;
  background: #f9fbfd;
  box-shadow: none;
}
input[type="text"]:focus {
  border-color: #2492ff;
  background: #fff;
}
.search-btn {
  width: 64px;
  height: 47px;
  border-radius: 0 30px 30px 0;
  border: none;
  background: #2492ff;
  color: #fff;
  font-size: 1.2em;
  cursor: pointer;
  outline: none;
  margin-left: -1px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.search-btn:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}
.dropdown {
  position: absolute;
  left: 0;
  top: 54px;
  width: 100%;
  background: #fff;
  box-shadow: 0 8px 32px #2492ff17;
  border-radius: 0 0 16px 16px;
  list-style: none;
  margin: 0;
  padding: 6px 0 6px 0;
  z-index: 2000;
  max-height: 240px;
  overflow-y: auto;
}
.dropdown li {
  padding: 11px 22px;
  font-size: 1.05em;
  color: #22478a;
  cursor: pointer;
  transition: background 0.13s;
  border: none;
  background: none;
}
.dropdown li.active,
.dropdown li:hover {
  background: #2492ff17;
  color: #2492ff;
}
.no-result {
  color: #e33;
  background: none;
  cursor: default;
  text-align: left;
  padding-left: 22px;
}
</style>
