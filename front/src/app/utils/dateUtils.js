// Utility function to format date strings without timezone conversion
// Input: "2024-01-15" (YYYY-MM-DD format)
// Output: "1/15/2024" (localized date format)

export function formatDateString(dateString) {
  if (!dateString) return null;
  
  // Parse the date string manually to avoid timezone issues
  const [year, month, day] = dateString.split('-').map(Number);
  
  // Create Date object using local timezone (not UTC)
  // month - 1 because Date constructor expects 0-based month
  const date = new Date(year, month - 1, day);
  
  // Return formatted date string
  return date.toLocaleDateString();
}

// Alternative: Simple formatting without Date object creation
export function formatDateStringSimple(dateString) {
  if (!dateString) return null;
  
  const [year, month, day] = dateString.split('-').map(Number);
  
  // Return MM/DD/YYYY format manually
  return `${month}/${day}/${year}`;
}