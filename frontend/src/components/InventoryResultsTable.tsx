import React, { useState } from 'react';

export interface TableColumn {
  id: string;
  label: string;
  type: string;
}

export interface InventoryResultsTableProps {
  columns: TableColumn[];
  rows: Array<Record<string, unknown>>;
  onSort?: (columnId: string, direction: 'asc' | 'desc') => void;
}

export const InventoryResultsTable: React.FC<InventoryResultsTableProps> = ({
  columns,
  rows,
  onSort,
}) => {
  const [sortColumn, setSortColumn] = useState<string | null>(null);
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('asc');

  const handleSort = (columnId: string) => {
    const newDirection =
      sortColumn === columnId && sortDirection === 'asc' ? 'desc' : 'asc';
    setSortColumn(columnId);
    setSortDirection(newDirection);
    if (onSort) {
      onSort(columnId, newDirection);
    }
  };

  const sortedRows = [...rows].sort((a, b) => {
    if (!sortColumn) return 0;
    const aVal = a[sortColumn];
    const bVal = b[sortColumn];
    
    // Handle numeric sorting
    if (typeof aVal === 'number' && typeof bVal === 'number') {
      return sortDirection === 'asc' ? aVal - bVal : bVal - aVal;
    }
    
    // Handle string sorting
    const aStr = String(aVal ?? '').toLowerCase();
    const bStr = String(bVal ?? '').toLowerCase();
    if (aStr === bStr) return 0;
    const comparison = aStr < bStr ? -1 : 1;
    return sortDirection === 'asc' ? comparison : -comparison;
  });

  const formatCellValue = (value: unknown, columnId: string): React.ReactNode => {
    if (value === null || value === undefined) {
      return <span style={{ color: '#94a3b8', fontStyle: 'italic' }}>—</span>;
    }

    // Format numbers
    if (typeof value === 'number') {
      // Check if it's a stock-related field
      if (columnId.toLowerCase().includes('stock') || columnId.toLowerCase().includes('volume')) {
        return <span className="number-cell">{value.toLocaleString()}</span>;
      }
      // Check if it's a threshold
      if (columnId.toLowerCase().includes('threshold')) {
        return <span className="number-cell">{value.toLocaleString()}</span>;
      }
      return <span className="number-cell">{value.toLocaleString()}</span>;
    }

    // Format dates
    if (value instanceof Date || (typeof value === 'string' && /^\d{4}-\d{2}-\d{2}/.test(value))) {
      const date = value instanceof Date ? value : new Date(value);
      if (!isNaN(date.getTime())) {
        return date.toLocaleDateString('en-US', {
          year: 'numeric',
          month: 'short',
          day: 'numeric',
        });
      }
    }

    // Format status/stock level indicators
    const strValue = String(value);
    if (columnId.toLowerCase().includes('stock') && typeof rows[0]?.[columnId] === 'number') {
      const stock = Number(value);
      const threshold = Number(rows[0]?.[columnId.replace('stock', 'threshold')] || rows[0]?.['reorderThreshold'] || 0);
      if (threshold > 0) {
        if (stock <= threshold) {
          return (
            <span>
              <span className="status-cell status-low">Low</span>
              <span style={{ marginLeft: '8px' }}>{stock.toLocaleString()}</span>
            </span>
          );
        } else if (stock <= threshold * 1.5) {
          return (
            <span>
              <span className="status-cell status-ok">OK</span>
              <span style={{ marginLeft: '8px' }}>{stock.toLocaleString()}</span>
            </span>
          );
        } else {
          return (
            <span>
              <span className="status-cell status-high">Good</span>
              <span style={{ marginLeft: '8px' }}>{stock.toLocaleString()}</span>
            </span>
          );
        }
      }
    }

    return strValue;
  };

  const getColumnClassName = (columnId: string): string => {
    if (columnId.toLowerCase().includes('stock') || 
        columnId.toLowerCase().includes('volume') || 
        columnId.toLowerCase().includes('threshold') ||
        columnId.toLowerCase().includes('count')) {
      return 'number-cell';
    }
    return '';
  };

  if (rows.length === 0) {
    return (
      <div className="results-table empty">
        <p>No results to display</p>
      </div>
    );
  }

  return (
    <div className="results-table">
      <div style={{ marginBottom: '12px', color: '#64748b', fontSize: '14px' }}>
        Showing {rows.length} {rows.length === 1 ? 'item' : 'items'}
      </div>
      <table>
        <thead>
          <tr>
            {columns.map((column) => (
              <th
                key={column.id}
                onClick={() => handleSort(column.id)}
                className={sortColumn === column.id ? `sort-${sortDirection}` : ''}
                style={{ cursor: 'pointer' }}
              >
                {column.label}
                {sortColumn === column.id && (
                  <span className="sort-indicator">
                    {sortDirection === 'asc' ? ' ↑' : ' ↓'}
                  </span>
                )}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {sortedRows.map((row, index) => (
            <tr key={index}>
              {columns.map((column) => (
                <td key={column.id} className={getColumnClassName(column.id)}>
                  {formatCellValue(row[column.id], column.id)}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

