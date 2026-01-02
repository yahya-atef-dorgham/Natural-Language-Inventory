import { describe, it, expect, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { DashboardPage } from '../../src/pages/DashboardPage';
import { nlQueryClient } from '../../src/services/nlQueryClient';

// Mock the NL query client
vi.mock('../../src/services/nlQueryClient', () => ({
  nlQueryClient: {
    submitQuery: vi.fn(),
    pollResults: vi.fn(),
  },
}));

describe('Dashboard NL Query Integration', () => {
  it('should render query input and submit button', () => {
    render(<DashboardPage />);
    
    expect(screen.getByPlaceholderText(/ask a question about inventory/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /submit query/i })).toBeInTheDocument();
  });

  it('should submit query and display results', async () => {
    const mockSubmit = vi.mocked(nlQueryClient.submitQuery);
    const mockPoll = vi.mocked(nlQueryClient.pollResults);

    mockSubmit.mockResolvedValue({
      sessionId: 'test-session-1',
      status: 'executing',
      message: 'Query accepted',
    });

    mockPoll.mockResolvedValue({
      sessionId: 'test-session-1',
      status: 'executed',
      reviewSummary: {},
      table: {
        columns: [
          { id: 'name', label: 'Name', type: 'string' },
          { id: 'stock', label: 'Stock', type: 'number' },
        ],
        rows: [
          { name: 'Product A', stock: 100 },
          { name: 'Product B', stock: 50 },
        ],
      },
      charts: [],
      message: 'Query executed successfully',
    });

    render(<DashboardPage />);
    const user = userEvent.setup();

    const input = screen.getByPlaceholderText(/ask a question about inventory/i);
    const submitButton = screen.getByRole('button', { name: /submit query/i });

    await user.type(input, 'Show me top products');
    await user.click(submitButton);

    await waitFor(() => {
      expect(mockSubmit).toHaveBeenCalledWith({ query: 'Show me top products' });
    });

    await waitFor(() => {
      expect(screen.getByText(/results/i)).toBeInTheDocument();
    });
  });
});

