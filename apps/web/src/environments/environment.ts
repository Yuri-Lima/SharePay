export const environment = {
  production: false,
  apiUrl: '/api',  // proxied or relative; for standalone use in-mem but calls simulated as /auth etc
  // For real backend integration use 'http://localhost:8000' but JWT not present; current impl uses mock responses for auth+data, calc authoritative from @sharepay/calculator
};
