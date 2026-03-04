import { computed } from 'vue';

export function useValidation(schema, formData) {
  const errors = computed(() => {
    const list = [];
    
    // Safety check for empty schema
    if (!schema || !schema.length) return list;

    schema.forEach(field => {
      const value = formData[field.id];
      const isMissing = value === null || value === '' || (Array.isArray(value) && value.length === 0);
      
      // We only validate if the field is actually supposed to be visible
      // (This requires passing the isVisible check here too, or keeping this simple for now)
      
      if (isMissing) {
        if (field.required) {
          list.push({ id: field.id, label: field.label, level: 'error', message: 'Mandatory field' });
        } else if (field.core) {
          list.push({ id: field.id, label: field.label, level: 'warning', message: 'NERIS Core field' });
        }
      }
    });
    
    return list;
  });

  const scrollToField = (fieldId) => {
    const el = document.getElementById(`field-${fieldId}`);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'center' });
      el.classList.add('highlight-error');
      setTimeout(() => el.classList.remove('highlight-error'), 2000);
    }
  };

  return { errors, scrollToField };
}
