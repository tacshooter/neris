<template>
  <div class="unit-response">
    <h3>Responding Units</h3>
    
    <div v-for="(unit, index) in formData" :key="index" class="unit-card">
      <div class="unit-header">
        <h4>Unit #{{ index + 1 }}: {{ unit.unit_id_reported || unit.unit_id_linked || 'New Unit' }}</h4>
        <button class="remove-btn" @click="$emit('remove', index)">Remove</button>
      </div>

      <div class="row">
        <div class="col">
          <label>Unit ID (Linked)</label>
          <input type="text" v-model="unit.unit_id_linked" placeholder="e.g. E701" />
        </div>
        <div class="col">
          <label>Staffing</label>
          <input type="number" v-model.number="unit.unit_staffing_reported" />
        </div>
      </div>

      <div class="timestamps-grid">
        <div class="col">
          <label>Dispatched</label>
          <input type="datetime-local" v-model="unit.time_dispatch" />
        </div>
        <div class="col">
          <label>Enroute</label>
          <input type="datetime-local" v-model="unit.time_enroute_to_scene" />
        </div>
        <div class="col">
          <label>On Scene</label>
          <input type="datetime-local" v-model="unit.time_on_scene" />
        </div>
        <div class="col">
          <label>Cleared</label>
          <input type="datetime-local" v-model="unit.time_unit_clear" />
        </div>
      </div>

      <!-- Medical Transport Section -->
      <div v-if="isMedical" class="medical-transport">
        <h5>Medical Transport</h5>
        <div class="row">
          <div class="col">
            <label>Hospital Destination</label>
            <input type="text" v-model="unit.hospital_destination" />
          </div>
          <div class="col">
            <label>Arrived Hospital</label>
            <input type="datetime-local" v-model="unit.time_arrived_hospital" />
          </div>
        </div>
      </div>
    </div>

    <button class="add-btn" @click="$emit('add')">Add Responding Unit</button>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  formData: Array,
  isMedical: Boolean
});

defineEmits(['add', 'remove']);
</script>

<style scoped>
.unit-card { border: 1px solid #ddd; padding: 1.5rem; margin-bottom: 1.5rem; border-radius: 8px; background: white; }
.unit-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; border-bottom: 1px solid #eee; padding-bottom: 0.5rem; }
.row, .timestamps-grid { display: flex; gap: 1rem; flex-wrap: wrap; margin-bottom: 1rem; }
.col { flex: 1; min-width: 150px; }
.medical-transport { margin-top: 1rem; padding: 1rem; background: #f0f7ff; border-radius: 4px; }
.remove-btn { color: #e74c3c; border: none; background: none; cursor: pointer; }
.add-btn { background: #3498db; color: white; padding: 0.5rem 1rem; border-radius: 4px; border: none; cursor: pointer; }
</style>
