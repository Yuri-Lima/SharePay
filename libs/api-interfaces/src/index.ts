// Shared API request/response contracts
export interface HouseDto {
  id: number;
  house_name: string;
  user_id: number;
}

export interface CalculateRequest {
  houseId: number;
}

export interface CalculateResponse {
  calc1: any; // shape from BillCalculator
  calc2: any;
  generatedAt: string;
}
