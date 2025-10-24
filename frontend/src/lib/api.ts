import ky from 'ky';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

export const api = ky.create({
  prefixUrl: API_URL,
  hooks: {
    beforeRequest: [
      (request) => {
        // Add auth token if available
        const token = localStorage.getItem('auth_token');
        if (token) {
          request.headers.set('Authorization', `Bearer ${token}`);
        }
      },
    ],
    afterResponse: [
      async (request, options, response) => {
        // Handle 401 Unauthorized
        if (response.status === 401) {
          localStorage.removeItem('auth_token');
          window.location.href = '/login';
        }
        return response;
      },
    ],
  },
});

// API Client Types
export interface ApiError {
  detail: string;
}

// Helper function for handling API errors
export const handleApiError = (error: unknown): string => {
  if (error instanceof Error) {
    return error.message;
  }
  return 'An unexpected error occurred';
};
