<template>
  <div class="incident-wizard">
    <nav class="tabs">
      <button 
        v-for="tab in tabs" 
        :key="tab.id" 
        @click="currentTab = tab.id"
        :class="{ active: currentTab === tab.id }"
      >
        {{ tab.name }}
      </button>
    </nav>

    <main class="tab-content">
      <!-- Tab 1: Core & Timeline -->
      <section v-if="currentTab === 'core'">
        <IncidentTimeline :formData="formData" :incidentType="formData.incident_final_type" />
        <div class="field-group">
          <label>Internal ID</label>
          <input type="text" v-model="formData.internal_id" />
        </div>
      </section>

      <!-- Tab 2: Location -->
      <section v-if="currentTab === 'location'">
        <CldxfAddress :formData="formData.location" />
      </section>

      <!-- Tab 3: Details (Dynamic) -->
      <section v-if="currentTab === 'details'">
        <div v-if="isFire">
          <h4>Fire Details</h4>
          <NerisModule :schema="schemas.fire" :formData="formData.modules.fire" />
        </div>
        
        <div v-if="isMedical">
          <h4>Medical / Patient Records</h4>
          <div v-for="(patient, index) in formData.modules.medical" :key="index" class="patient-card">
             <h5>Patient #{{ index + 1 }}</h5>
             <NerisModule :schema="schemas.medical" :formData="formData.modules.medical[index]" />
             <button @click="removePatient(index)">Remove Patient</button>
          </div>
          <button @click="addPatient">Add Patient</button>
        </div>
      </section>

      <!-- Tab 4: Narrative -->
      <section v-if="currentTab === 'narrative'">
        <label>Incident Outcome</label>
        <textarea v-model="formData.narrative.outcome" rows="10"></textarea>
      </section>
    </main>

    <footer class="controls">
      <button @click="saveDraft">Save Draft</button>
      <button class="submit" @click="submitReport">Submit to NERIS</button>
    </footer>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue';
import IncidentTimeline from './IncidentTimeline.vue';
import CldxfAddress from './CldxfAddress.vue';
import NerisModule from './NerisModule.vue';

const currentTab = ref('core');
const tabs = [
  { id: 'core', name: '1. Basics' },
  { id: 'location', name: '2. Location' },
  { id: 'details', name: '3. Details' },
  { id: 'narrative', name: '4. Narrative' }
];

const formData = reactive({
  internal_id: '',
  incident_final_type: [],
  location: {},
  modules: {
    fire: {},
    medical: []
  },
  narrative: { outcome: '' }
});

// Mock schemas (in production, loaded via fetchSchema)
const schemas = reactive({
  fire: [], 
  medical: []
});

const isFire = computed(() => formData.incident_final_type.includes('FIRE'));
const isMedical = computed(() => formData.incident_final_type.includes('MEDICAL'));

const addPatient = () => formData.modules.medical.push({});
const removePatient = (index) => formData.modules.medical.splice(index, 1);

const saveDraft = async () => {
  // Call Django POST /api/incidents/
  console.log("Saving...", formData);
};
</script>

<style scoped>
.incident-wizard { max-width: 900px; margin: 0 auto; }
.tabs { display: flex; border-bottom: 2px solid #eee; margin-bottom: 2rem; }
.tabs button { padding: 1rem 2rem; border: none; background: none; cursor: pointer; }
.tabs button.active { border-bottom: 2px solid #3498db; font-weight: bold; color: #3498db; }
.patient-card { border: 1px solid #ddd; padding: 1rem; margin-bottom: 1rem; border-radius: 8px; }
.controls { margin-top: 2rem; display: flex; gap: 1rem; justify-content: flex-end; }
.submit { background: #27ae60; color: white; padding: 0.5rem 1.5rem; border-radius: 4px; }
</style>
