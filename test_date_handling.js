#!/usr/bin/env node

// Test date handling to understand timezone issues
console.log('Testing date handling behavior...\n');

// Test 1: HTML date input format
const dateString = '2024-01-15';
console.log(`1. Original date string: ${dateString}`);

// Test 2: Create Date object from string
const dateObj = new Date(dateString);
console.log(`2. Date object: ${dateObj}`);
console.log(`3. Date toISOString(): ${dateObj.toISOString()}`);
console.log(`4. Date toDateString(): ${dateObj.toDateString()}`);

// Test 3: Timezone offset
console.log(`5. Timezone offset (minutes): ${dateObj.getTimezoneOffset()}`);

// Test 4: JSON serialization
const testPayload = { start_date: dateString };
console.log(`6. JSON serialized: ${JSON.stringify(testPayload)}`);

// Test 5: Potential issue - when Date object is created and serialized
const testPayloadWithDate = { start_date: dateObj };
console.log(`7. JSON serialized with Date object: ${JSON.stringify(testPayloadWithDate)}`);

// Test 6: Proper handling - keep as string
console.log(`8. Proper handling - keep as string: ${JSON.stringify({start_date: dateString})}`);

// Test 7: What happens if we create Date and convert back to local date string
const localDateString = dateObj.getFullYear() + '-' + 
  String(dateObj.getMonth() + 1).padStart(2, '0') + '-' + 
  String(dateObj.getDate()).padStart(2, '0');
console.log(`9. Local date string: ${localDateString}`);