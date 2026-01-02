import axios from 'axios';
import { config } from '../config';

export interface NLQueryRequest {
  query: string;
  context?: Record<string, unknown>;
}

export interface NLQueryResponse {
  sessionId: string;
  status: string;
  message: string;
}

export interface QueryResult {
  sessionId: string;
  status: string;
  reviewSummary: Record<string, unknown>;
  table: {
    columns: Array<{ id: string; label: string; type: string }>;
    rows: Array<Record<string, unknown>>;
  };
  charts: Array<{
    type: string;
    title: string;
    data: Array<Record<string, unknown>>;
  }>;
  message: string;
}

export class NLQueryClient {
  private baseUrl: string;
  private authToken: string;

  constructor(authToken: string = 'mock-token') {
    this.baseUrl = config.apiUrl;
    this.authToken = authToken;
  }

  async submitQuery(request: NLQueryRequest): Promise<NLQueryResponse> {
    const response = await axios.post<NLQueryResponse>(
      `${this.baseUrl}/api/nl-queries`,
      request,
      {
        headers: {
          Authorization: `Bearer ${this.authToken}`,
          'Content-Type': 'application/json',
        },
      }
    );
    return response.data;
  }

  async getResults(sessionId: string): Promise<QueryResult> {
    const response = await axios.get<QueryResult>(
      `${this.baseUrl}/api/nl-queries/${sessionId}`,
      {
        headers: {
          Authorization: `Bearer ${this.authToken}`,
        },
      }
    );
    return response.data;
  }

  async pollResults(
    sessionId: string,
    maxAttempts: number = 10,
    intervalMs: number = 500
  ): Promise<QueryResult> {
    for (let attempt = 0; attempt < maxAttempts; attempt++) {
      const result = await this.getResults(sessionId);
      if (result.status === 'executed' || result.status === 'rejected' || result.status === 'failed') {
        return result;
      }
      await new Promise((resolve) => setTimeout(resolve, intervalMs));
    }
    throw new Error('Polling timeout: query did not complete in time');
  }
}

export const nlQueryClient = new NLQueryClient();

