import React, { useState } from 'react';
import { nlQueryClient, QueryResult } from '../services/nlQueryClient';
import { InventoryResultsTable } from '../components/InventoryResultsTable';
import { InventoryResultsChart } from '../components/InventoryResultsChart';
import { QueryFeedback } from '../components/QueryFeedback';

export const DashboardPage: React.FC = () => {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<QueryResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError(null);
    setResults(null);

    try {
      // Submit query
      const response = await nlQueryClient.submitQuery({ query });
      
      // Poll for results
      const queryResults = await nlQueryClient.pollResults(response.sessionId);
      setResults(queryResults);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to process query');
    } finally {
      setLoading(false);
    }
  };

  const handleSort = (columnId: string, direction: 'asc' | 'desc') => {
    if (!results) return;
    
    // Update results with sorted data
    const sortedRows = [...results.table.rows].sort((a, b) => {
      const aVal = a[columnId] as unknown;
      const bVal = b[columnId] as unknown;
      if (aVal === bVal) return 0;
      const comparison = (aVal as number) < (bVal as number) ? -1 : 1;
      return direction === 'asc' ? comparison : -comparison;
    });

    setResults({
      ...results,
      table: {
        ...results.table,
        rows: sortedRows,
      },
    });
  };

  return (
    <div className="dashboard-page">
      <header>
        <h1>Natural Language Inventory Dashboard</h1>
      </header>

      <main>
        <section className="query-section">
          <form onSubmit={handleSubmit}>
            <div className="query-input-group">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Ask a question about inventory, e.g., 'Show me top-selling products in electronics with low stock'"
                disabled={loading}
                className="query-input"
              />
              <button type="submit" disabled={loading || !query.trim()}>
                {loading ? (
                  <>
                    <span className="loading-spinner"></span>
                    Processing...
                  </>
                ) : (
                  'Submit Query'
                )}
              </button>
            </div>
          </form>

          {error && (
            <div className="error-message">
              <p>Error: {error}</p>
            </div>
          )}

          {results && (
            <QueryFeedback
              message={results.message}
              reviewSummary={results.reviewSummary}
              status={results.status}
            />
          )}
        </section>

        {results && (
          <section className="results-section">
            <div className="results-table-container">
              <h2>📋 Results Table</h2>
              <InventoryResultsTable
                columns={results.table.columns}
                rows={results.table.rows}
                onSort={handleSort}
              />
            </div>

            <div className="results-chart-container">
              <h2>📊 Data Visualizations</h2>
              <InventoryResultsChart charts={results.charts} />
            </div>
          </section>
        )}
      </main>
    </div>
  );
};

