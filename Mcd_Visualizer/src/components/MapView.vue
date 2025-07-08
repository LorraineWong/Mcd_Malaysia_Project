<template>
  <div id="map" style="width: 100%; height: 90vh; border-radius: 16px; box-shadow: 0 2px 12px #888;">
    <button
      class="reset-map-btn"
      @click="resetMapView"
      title="Reset map view"
    >
      <span class="material-icons">my_location</span>
    </button>
  </div>
</template>


<script setup>
// Import Vue core features
import { onMounted, watch } from 'vue'
import mapboxgl from 'mapbox-gl'
import axios from 'axios'

// Default center and zoom level for the map
const DEFAULT_CENTER = [101.6869, 3.1390]; // KL coordinates
const DEFAULT_ZOOM = 10;
let map = null; // (make sure map is accessible here)
let activePopup = null

function resetMapView() {
  if (map) {
    map.flyTo({ center: DEFAULT_CENTER, zoom: DEFAULT_ZOOM, speed: 1.2 })
    // Close popup if any is open
    if (activePopup) {
      activePopup.remove()
      activePopup = null
    }
  }
}

// Receive the focusedOutletId prop from the parent (App.vue)
const props = defineProps({
  focusedOutletId: String
})

// Set Mapbox API token (put yours in .env)
mapboxgl.accessToken = import.meta.env.VITE_MAPBOX_TOKEN

// Static asset icons for the popup
const phoneIcon = '/assets/phone.png'
const googleMapIcon = '/assets/google_map.png'
const wazeIcon = '/assets/waze.png'
const mcdLogo = '/assets/mcdonalds_logo.png'
const pinBlue = '/assets/place_24dp_2492FF.svg'
const pinRed = '/assets/place_24dp_FF5050.svg'
const pinOrange = '/assets/place_24dp_FFA600.svg'
import { featureIcons } from '../utils/featureIcons'

// --- Shared state for markers ---
let markersById = {}  // To store all Mapbox marker/popup objects by outlet ID
let outlets = []      // Array to store all outlet data

// Utility: Selects the marker icon depending on overlap
function getPinIcon(count) {
  if (count >= 15) return pinRed
  if (count >= 7)  return pinOrange
  return pinBlue
}
// Utility: Color for the outlet circle
function getPinColor(count) {
  if (count >= 15) return "#FF5050"
  if (count >= 7)  return "#FFA600"
  return "#2492FF"
}
// Utility: Draw a circular GeoJSON polygon (radius in km)
function createGeoCircle(center, radiusKm, points = 64) {
  const [lng, lat] = center
  const coords = []
  for (let i = 0; i < points; i++) {
    const angle = (i * 360) / points
    const dx = radiusKm * 0.009 * Math.cos((angle * Math.PI) / 180)
    const dy = radiusKm * 0.009 * Math.sin((angle * Math.PI) / 180)
    coords.push([lng + dx, lat + dy])
  }
  coords.push(coords[0])
  return { type: "Feature", geometry: { type: "Polygon", coordinates: [coords] } }
}
// Utility: Haversine distance in km between two points
function haversineDistance([lng1, lat1], [lng2, lat2]) {
  function toRad(deg) { return deg * Math.PI / 180 }
  const R = 6371
  const dLat = toRad(lat2 - lat1)
  const dLng = toRad(lng2 - lng1)
  const a = Math.sin(dLat / 2) ** 2 +
    Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLng / 2) ** 2
  return 2 * R * Math.asin(Math.sqrt(a))
}

onMounted(async () => {
  // 1. Initialize the Mapbox map
  map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11',
    center: [101.6869, 3.1390],
    zoom: 10,
  })

  let activePopup = null
  let popupHover = false
  let markerHover = false

  // Function: Tries to close the popup if not hovered
  function tryClosePopup() {
    setTimeout(() => {
      if (!markerHover && !popupHover && activePopup) {
        activePopup.remove()
        activePopup = null
      }
    }, 50)
  }

  try {
    // 2. Fetch all outlets from your backend API
    const response = await axios.get('http://127.0.0.1:8000/outlets')
    outlets = response.data

    // 3. Build overlap map: which outlets overlap in their 5km radius
    const overlapMap = {}
    for (let i = 0; i < outlets.length; i++) {
      overlapMap[outlets[i].id] = []
      for (let j = 0; j < outlets.length; j++) {
        if (i !== j) {
          const a = outlets[i], b = outlets[j]
          if (
            a.longitude && a.latitude &&
            b.longitude && b.latitude &&
            haversineDistance([a.longitude, a.latitude], [b.longitude, b.latitude]) < 10
          ) {
            overlapMap[a.id].push(b.id)
          }
        }
      }
    }

    // 4. Draw all outlets, catchment circles and popup info
    map.on('load', () => {
      outlets.forEach((outlet) => {
        if (outlet.longitude && outlet.latitude) {
          const overlapCount = overlapMap[outlet.id].length

          // Draw 5km catchment circle
          const circleId = `circle-${outlet.id}`
          map.addSource(circleId, {
            type: "geojson",
            data: createGeoCircle([outlet.longitude, outlet.latitude], 5)
          })
          map.addLayer({
            id: circleId,
            type: "fill",
            source: circleId,
            paint: {
              "fill-color": getPinColor(overlapCount),
              "fill-opacity": overlapCount > 0 ? 0.09 : 0.05
            }
          })

          // Marker with custom SVG
          const el = document.createElement('div')
          el.className = 'custom-marker'
          el.style.width = '42px'
          el.style.height = '42px'
          el.style.display = 'flex'
          el.style.alignItems = 'center'
          el.style.justifyContent = 'center'
          el.style.cursor = 'pointer'
          el.style.filter = 'drop-shadow(0 0 3px #fff) drop-shadow(0 1px 6px rgba(0,0,0,0.15))'
          const img = document.createElement('img')
          img.src = getPinIcon(overlapCount)
          img.alt = 'Location Pin'
          img.style.width = '36px'
          img.style.height = '36px'
          el.appendChild(img)

          // Compose outlet popup HTML
          const tel = outlet.telephone && outlet.telephone.trim() ? outlet.telephone : '-'
          const telHTML = tel !== '-' ? `<a href="tel:${tel}"><img src="${phoneIcon}" alt="Tel" width="18" style="vertical-align:middle;"/> ${tel}</a>` : `<img src="${phoneIcon}" alt="Tel" width="18" style="vertical-align:middle;opacity:.5"/> -`
          const googleMapHTML = outlet.google_map_link ? `<a href="${outlet.google_map_link}" target="_blank" style="margin-right:12px;"><img src="${googleMapIcon}" alt="Google Maps" width="20" style="vertical-align:middle;margin-right:2px"/>Google Maps</a>` : ''
          const wazeHTML = outlet.waze_link ? `<a href="${outlet.waze_link}" target="_blank"><img src="${wazeIcon}" alt="Waze" width="20" style="vertical-align:middle;margin-right:2px"/>Waze</a>` : ''
          const featureArr = outlet.features
            ? Object.entries(outlet.features).filter(([_, v]) => v === true).map(([k, _]) => k)
            : []
          let featuresHTML = ""
          if (featureArr.length > 0) {
            featuresHTML = `
              <div style="margin-bottom:8px;display:flex;gap:8px;flex-wrap:wrap;">
                ${featureArr.map(f =>
                  featureIcons[f]
                    ? `<img src="${featureIcons[f].icon}" alt="${featureIcons[f].name}" title="${featureIcons[f].name}" width="28" height="28"/>`
                    : ''
                ).join('')}
              </div>
            `
          }
          // Overlap tip with up to 8 names
          let overlapTip = ''
          if (overlapCount > 0) {
            const overlappedNames = overlapMap[outlet.id]
              .map(id => (outlets.find(x => x.id === id)?.name || ''))
              .filter(Boolean)
            const shownNames = overlappedNames.slice(0, 8).map(n => `<div>${n}</div>`).join('')
            const moreCount = overlappedNames.length - 8
            overlapTip = `
              <div style="color:#FF5050;font-size:13px;margin:4px 0 0 0;">
                Overlaps with <b>${overlapCount}</b> outlet(s):<br>
                ${shownNames}
                ${moreCount > 0 ? `<span style="font-size:12px;color:#555;">...and ${moreCount} more</span>` : ''}
              </div>
            `
          } else {
            overlapTip = `<div style="color:#2492FF;font-size:13px;margin:4px 0 0 0;">No overlap</div>`
          }

          const popupHTML = `
            <div class="popup-content">
              <div style="display:flex;align-items:center;margin-bottom:4px;">
                <img src="${mcdLogo}" alt="logo" width="30" style="margin-right:8px;" />
                <strong>${outlet.name}</strong>
              </div>
              <div style="margin-bottom:4px;">${outlet.address}</div>
              ${featuresHTML}
              <div style="margin-bottom:8px;">${telHTML}</div>
              <div>${googleMapHTML}${wazeHTML}</div>
              ${overlapTip}
            </div>
          `

          const popup = new mapboxgl.Popup({
            closeButton: false,
            closeOnClick: false,
            offset: 28,
            maxWidth: "340px",
          }).setHTML(popupHTML)

          // Marker hover logic for showing popups
          el.addEventListener('mouseenter', () => {
            markerHover = true
            if (activePopup) activePopup.remove()
            popup.addTo(map)
            popup.setLngLat([outlet.longitude, outlet.latitude])
            activePopup = popup
          })
          el.addEventListener('mouseleave', () => {
            markerHover = false
            tryClosePopup()
          })
          popup.on('open', () => {
            const popupElm = document.querySelector('.mapboxgl-popup')
            if (popupElm) {
              popupElm.addEventListener('mouseenter', () => { popupHover = true })
              popupElm.addEventListener('mouseleave', () => {
                popupHover = false
                tryClosePopup()
              })
            }
          })

          // Add marker to map and save for later reference
          const marker = new mapboxgl.Marker(el)
            .setLngLat([outlet.longitude, outlet.latitude])
            .addTo(map)
          markersById[outlet.id] = { marker, popup }
        }
      })
    })
    map.on('click', function (e) {
      // Only close popup if click is not on a marker (no feature at point)
      // If you only use custom HTML markers, you may need to check event.target
      if (activePopup) {
        activePopup.remove()
        activePopup = null
      }
    })

  } catch (error) {
    console.error('Error fetching outlets:', error)
  }
})

// React to parent prop: focus/fly to specific outlet when focusedOutletId changes
watch(
  () => props.focusedOutletId,
  (newId) => {
    // Close previous popup before opening new one
    if (activePopup) {
      activePopup.remove()
      activePopup = null
    }
    if (!newId || !markersById[newId]) return
    const { marker, popup } = markersById[newId]
    marker._map.flyTo({ center: marker.getLngLat(), zoom: 16, speed: 1.2 })
    popup.addTo(marker._map)
    popup.setLngLat(marker.getLngLat())
    activePopup = popup // <--- Update reference
  }
)
</script>

<style scoped>
#map {
  margin: 24px auto;
  max-width: 1100px;
  min-height: 70vh;
  border: 2px solid #e1e1e1;
}
.custom-marker {
  border-radius: 50%;
  pointer-events: auto;
  display: flex;
  align-items: center;
  justify-content: center;
}
.popup-content {
  min-width: 220px;
  max-width: 340px;
  font-size: 15px;
  word-break: break-word;
}
.popup-content a {
  color: #222;
  text-decoration: none;
  margin-right: 4px;
  font-size: 15px;
}
.popup-content a:hover {
  text-decoration: none;
  color: #222;
}
.reset-map-btn {
  position: absolute;
  top: 16px;
  right: 16px;
  z-index: 10;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: #fff;
  box-shadow: 0 2px 8px #0002;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.15s;
  font-size: 1.6em;
}
.reset-map-btn:hover {
  background: #2492ff;
  color: #fff;
}
.reset-map-btn .material-icons {
  font-size: 1.8em;
  color: #2492ff;
}
.reset-map-btn:hover .material-icons {
  color: #fff;
}
</style>
