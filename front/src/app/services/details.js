import { apiService } from './api';

// Legacy function for backward compatibility
export const getdetails = () => {
  return apiService.getDetails();
};

export default getdetails;



