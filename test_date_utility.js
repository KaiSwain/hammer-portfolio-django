// Test the date utility functions
function formatDateString(dateString) {
  if (!dateString) return null;
  const [year, month, day] = dateString.split('-').map(Number);
  const date = new Date(year, month - 1, day);
  return date.toLocaleDateString();
}

function formatDateStringSimple(dateString) {
  if (!dateString) return null;
  const [year, month, day] = dateString.split('-').map(Number);
  return `${month}/${day}/${year}`;
}

console.log('Testing date utility functions:');
console.log('Input: 2024-01-15');
console.log('formatDateString:', formatDateString('2024-01-15'));
console.log('formatDateStringSimple:', formatDateStringSimple('2024-01-15'));
console.log('');
console.log('Input: 2025-09-15');
console.log('formatDateString:', formatDateString('2025-09-15'));
console.log('formatDateStringSimple:', formatDateStringSimple('2025-09-15'));

// Test with problematic date that was showing as day before
console.log('');
console.log('Comparing old vs new approach for 2025-09-15:');
console.log('OLD (new Date().toLocaleDateString()):', new Date('2025-09-15').toLocaleDateString());
console.log('NEW (formatDateString):', formatDateString('2025-09-15'));
console.log('NEW (formatDateStringSimple):', formatDateStringSimple('2025-09-15'));