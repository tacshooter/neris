<template>
  <div class="neris-module" :class="{ 'nested': isNested }">
    <div v-for="field in schema" :key="field.id" class="field-wrapper">
      <!-- Visibility logic from composable -->
      <div v-if="isVisible(field, formData)" class="field-group">
        <label :for="field.id">
          {{ field.label }}
          <span v-if="field.required" class="required">*</span>
        </label>

        <!-- Standard Text Input -->
        <input 
          v-if="field.type === 'Text' && !field.value_set" 
          type="text" 
          v-model="formData[field.id]" 
          :placeholder="field.example"
        />

        <!-- Number Input -->
        <input 
          v-if="(field.type === 'Integer' || field.type === 'Float') && !field.value_set" 
          type="number" 
          v-model.number="formData[field.id]" 
          :step="field.type === 'Float' ? '0.1' : '1'"
        />

        <!-- Boolean / Checkbox -->
        <input 
          v-if="field.type === 'Boolean'" 
          type="checkbox" 
          v-model="formData[field.id]" 
        />

        <!-- Value Set Dropdowns -->
        <select 
          v-if="field.value_set" 
          v-model="formData[field.id]"
          :multiple="field.cardinality === 'Multi'"
        >
          <option disabled value="">Please select one</option>
          <!-- Lookups would be injected via a global store/provide -->
          <option v-for="opt in getOptions(field.id)" :key="opt.code" :value="opt.code">
            {{ opt.description }}
          </option>
        </select>

        <!-- RECURSIVE STEP: If field is a nested Module -->
        <div v-if="field.type === 'Module'" class="module-container">
          <NerisModule 
            :schema="fetchSchemaForModule(field.id)" 
            :formData="formData[field.id]" 
            :isNested="true"
          />
        </div>

        <!-- RECURSIVE STEP: If field is an Array of Modules (e.g. Medical Patients) -->
        <div v-if="field.type === 'Array[Module]'" class="module-array">
          <div v-for="(item, index) in formData[field.id]" :key="index" class="module-array-item">
            <NerisModule 
              :schema="fetchSchemaForModule(field.id)" 
              :formData="formData[field.id][index]" 
              :isNested="true"
            />
            <button @click="removeItem(field.id, index)">Remove</button>
          </div>
          <button @click="addItem(field.id)">Add {{ field.label }}</button>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, inject } from 'vue';

const props = defineProps({
  schema: Array,
  formData: Object,
  isNested: { type: Boolean, default: false }
});

// Injected from parent useNerisForm
const isVisible = inject('isVisible');
const getOptions = inject('getOptions');
const fetchSchemaForModule = inject('fetchSchemaForModule');

const addItem = (fieldId) => {
  props.formData[fieldId].push({});
};

const removeItem = (fieldId, index) => {
  props.formData[fieldId].splice(index, 1);
};
</script>

<style scoped>
.neris-module { display: flex; flex-direction: column; gap: 1rem; }
.nested { border-left: 2px solid #3498db; padding-left: 1.5rem; margin: 1rem 0; }
.field-wrapper { margin-bottom: 0.5rem; }
.field-group label { display: block; font-weight: bold; margin-bottom: 0.25rem; }
.required { color: #e74c3c; }
.module-array-item { border: 1px dashed #ccc; padding: 1rem; margin-bottom: 1rem; }
</style>
