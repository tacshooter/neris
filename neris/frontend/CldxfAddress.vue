<template>
  <div class="cldxf-address">
    <h3>Incident Location (CLDXF)</h3>
    
    <!-- Primary Address Info -->
    <div class="form-section">
      <div class="row">
        <div class="col">
          <label>Number</label>
          <input type="number" v-model="formData.an_number" placeholder="123" />
        </div>
        <div class="col">
          <label>Pre-Dir</label>
          <select v-model="formData.sn_pre_directional">
            <option value="">None</option>
            <option v-for="dir in directions" :key="dir" :value="dir">{{ dir }}</option>
          </select>
        </div>
        <div class="col">
          <label>Street Name</label>
          <input type="text" v-model="formData.sn_street_name" placeholder="Main" />
        </div>
        <div class="col">
          <label>Post-Type</label>
          <input type="text" v-model="formData.sn_post_type" placeholder="St" />
        </div>
      </div>
    </div>

    <!-- Building / Level Detail -->
    <div class="form-section building-details">
      <div class="row">
        <div class="col">
          <label>Floor</label>
          <input type="text" v-model="formData.nl_floor" placeholder="5" />
        </div>
        <div class="col">
          <label>Unit/Apt</label>
          <input type="text" v-model="formData.nl_unit_value" placeholder="4B" />
        </div>
        <div class="col">
          <label>Room</label>
          <input type="text" v-model="formData.nl_room" placeholder="Conf Room A" />
        </div>
      </div>
    </div>

    <!-- City / State / Zip -->
    <div class="form-section">
      <div class="row">
        <div class="col">
          <label>City (Muni)</label>
          <input type="text" v-model="formData.csop_incorporated_muni" />
        </div>
        <div class="col">
          <label>State</label>
          <input type="text" v-model="formData.csop_state" maxlength="2" />
        </div>
        <div class="col">
          <label>ZIP Code</label>
          <input type="text" v-model="formData.csop_postal_code" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  formData: Object
});

const directions = ['North', 'South', 'East', 'West', 'Northeast', 'Northwest', 'Southeast', 'Southwest'];
</script>

<style scoped>
.cldxf-address { border: 1px solid #ddd; padding: 1.5rem; border-radius: 8px; background: #f9f9f9; }
.form-section { margin-bottom: 1.5rem; }
.row { display: flex; gap: 1rem; flex-wrap: wrap; }
.col { flex: 1; min-width: 120px; }
label { display: block; font-size: 0.8rem; color: #666; margin-bottom: 0.25rem; }
input, select { width: 100%; padding: 0.5rem; border: 1px solid #ccc; border-radius: 4px; }
h3 { margin-top: 0; color: #2c3e50; }
</style>
