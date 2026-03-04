import { reactive } from 'vue';

export function useNerisForm(initialSchema) {
  const formData = reactive({});
  
  // Initialize state based on schema
  const initData = (fields, target) => {
    fields.forEach(f => {
      if (f.type === 'Module') target[f.id] = {};
      else if (f.type.includes('Array')) target[f.id] = [];
      else target[f.id] = null;
    });
  };

  initData(initialSchema, formData);

  const isVisible = (field, currentData) => {
    if (!field.possible_if) return true;
    const condition = field.possible_if.toLowerCase();
    
    // Logic: "final incident type includes fire"
    if (condition.includes('fire')) {
      return JSON.stringify(formData.incident_final_type || []).toLowerCase().includes('fire');
    }
    return true;
  };

  return { formData, isVisible };
}
