<template>
  <div class="dashboard">
    <header>
      <h1>Lobster Cove Fire & Rescue Dashboard</h1>
      <div class="status-bar">Connected to NERIS V1 API</div>
    </header>

    <div class="main-layout">
      <!-- Left Column: Reports -->
      <div class="reports-column">
        
        <!-- Section: Pending from CAD -->
        <section class="card">
          <h2>Pending Reports (CAD Feed)</h2>
          <div v-for="event in cadFeed" :key="event.cad_id" class="feed-item">
            <div class="info">
              <span class="type">{{ event.type_hierarchy.join(' > ') }}</span>
              <span class="address">{{ event.address }}</span>
              <span class="time">{{ formatTime(event.dispatched_at) }}</span>
            </div>
            <button class="primary" @click="startReport(event)">Start Report</button>
          </div>
        </section>

        <!-- Section: Drafts -->
        <section class="card">
          <h2>Active Drafts</h2>
          <table v-if="drafts.length">
            <thead>
              <tr>
                <th>Incident ID</th>
                <th>Status</th>
                <th>Last Modified</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="draft in drafts" :key="draft.neris_id">
                <td>{{ draft.internal_id }}</td>
                <td><span class="badge" :class="draft.status">{{ draft.status }}</span></td>
                <td>{{ formatTime(draft.created_at) }}</td>
                <td><button @click="editDraft(draft)">Edit</button></td>
              </tr>
            </tbody>
          </table>
          <p v-else>No active drafts found.</p>
        </section>
      </div>

      <!-- Right Column: Resources -->
      <aside class="resources-column">
        <section class="card">
          <h3>Unit Status</h3>
          <div v-for="unit in units" :key="unit.unit_id" class="unit-status">
            <strong>{{ unit.unit_id }}</strong> - {{ unit.type }}
            <span class="staffing">Staff: {{ unit.staffing }}</span>
          </div>
        </section>

        <section class="card">
          <h3>Personnel On Duty</h3>
          <div v-for="person in personnel" :key="person.id" class="person-tag">
            {{ person.rank }} {{ person.name }}
          </div>
        </section>
      </aside>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const cadFeed = ref([]);
const drafts = ref([]);
const units = ref([]);
const personnel = ref([]);

const fetchData = async () => {
  // Mocking the API calls for the dashboard data
  const resCad = await fetch('/api/cad-feed/');
  cadFeed.value = await resCad.json();

  const resDrafts = await fetch('/api/incidents/');
  drafts.value = await resDrafts.json();

  const resUnits = await fetch('/api/units/');
  units.value = await resUnits.json();

  const resPeople = await fetch('/api/personnel/');
  personnel.value = await resPeople.json();
};

const formatTime = (iso) => new Date(iso).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

const startReport = (event) => {
  console.log("Starting report for:", event.cad_id);
  // Transition to IncidentWizard.vue with pre-filled data
};

const editDraft = (draft) => {
  console.log("Editing draft:", draft.neris_id);
};

onMounted(fetchData);
</script>

<style scoped>
.dashboard { padding: 2rem; background: #f4f7f6; min-height: 100vh; }
.main-layout { display: grid; grid-template-columns: 1fr 300px; gap: 2rem; margin-top: 2rem; }
.card { background: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 2rem; }
.feed-item { display: flex; justify-content: space-between; align-items: center; padding: 1rem 0; border-bottom: 1px solid #eee; }
.feed-item:last-child { border-bottom: none; }
.info span { display: block; margin-bottom: 0.25rem; }
.type { font-weight: bold; color: #e67e22; font-size: 0.9rem; }
.address { font-size: 1.1rem; }
.time { color: #999; font-size: 0.8rem; }
.badge { padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.75rem; text-transform: uppercase; }
.badge.draft { background: #dbeafe; color: #1e40af; }
.unit-status { padding: 0.5rem 0; border-bottom: 1px solid #eee; font-size: 0.9rem; }
.staffing { float: right; color: #666; }
.person-tag { font-size: 0.85rem; margin-bottom: 0.25rem; }
</style>
